import json
import time
from typing import List, Dict
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.cache.redis_client import redis_client

MAX_TURNS = 5
KEEP_AFTER_SUMMARY = 2
SUMMARY_TRIGGER = 5
TTL_SECONDS = 300  

SYSTEM_PROMPT = "You are a helpful AI assistant."


def _turns_key(session_id: str) -> str:
    return f"chat:{session_id}:turns"


def _summary_key(session_id: str) -> str:
    return f"chat:{session_id}:summary"


def get_turns(session_id: str) -> List[Dict]:
    if redis_client is None:
        return []

    raw = redis_client.lrange(_turns_key(session_id), 0, -1)
    return [json.loads(t) for t in raw]


def get_summary(session_id: str) -> str:
    if redis_client is None:
        return ""

    return redis_client.get(_summary_key(session_id)) or ""


def store_turn(session_id: str, turn: Dict):
    if redis_client is None:
        return

    key = _turns_key(session_id)
    redis_client.rpush(key, json.dumps(turn))
    redis_client.expire(key, TTL_SECONDS)
    redis_client.expire(_summary_key(session_id), TTL_SECONDS)


def update_summary_batch(
    llm,
    existing_summary: str,
    turns_to_summarize: List[Dict]
) -> str:
    convo_lines = []

    for t in turns_to_summarize:
        convo_lines.append(f"User: {t['user']}")
        convo_lines.append(f"Assistant: {t['assistant']}")

    conversation_text = "\n".join(convo_lines)

    prompt = f"""
You are maintaining a long-term memory summary of a conversation.

CRITICAL RULES:
- MERGE the existing summary with the new conversation turns into ONE unified summary.
- DO NOT append or list summaries separately.
- REMOVE redundancy.
- If new information contradicts old summary, KEEP THE MOST RECENT information.
- Preserve important decisions, preferences, constraints.
- Ignore small talk.
- Keep the result concise and factual.

Existing summary:
{existing_summary}

New conversation turns:
{conversation_text}

Return a single updated summary only.
""".strip()

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()


def build_memory_context(
    session_id: str,
) -> List:
    """
    Returns list of LangChain messages representing memory context.
    """
    messages = [SystemMessage(content=SYSTEM_PROMPT)]

    summary = get_summary(session_id)
    if summary:
        messages.append(
            SystemMessage(content=f"Conversation summary:\n{summary}")
        )

    for t in get_turns(session_id):
        messages.append(HumanMessage(content=t["user"]))
        messages.append(AIMessage(content=t["assistant"]))

    return messages



def maybe_summarize(
    session_id: str,
    llm
):
    if redis_client is None:
        return

    turns = get_turns(session_id)

    if len(turns) <= SUMMARY_TRIGGER:
        return

    num_to_summarize = len(turns) - KEEP_AFTER_SUMMARY
    turns_to_summarize = turns[:num_to_summarize]

    updated_summary = update_summary_batch(
        llm,
        get_summary(session_id),
        turns_to_summarize
    )

    redis_client.set(_summary_key(session_id), updated_summary)

    redis_client.ltrim(
        _turns_key(session_id),
        num_to_summarize,
        -1
    )
