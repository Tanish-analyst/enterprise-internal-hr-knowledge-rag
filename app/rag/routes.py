import time
from fastapi import APIRouter, Depends, HTTPException

from app.models.query import Query
from app.core.security import get_current_user
from app.rag.clients import (
    openai_client,
    pinecone_index,
    bm25,
    co
)
from app.rag.parent_store import parent_store

from app.cache.semantic_cache import (
    semantic_cache_lookup,
    store_semantic_cache
)
from app.cache.memory import (
    build_memory_context,
    store_turn,
    maybe_summarize
)

from app.core.config import (
    TOP_K,
    RERANK_SCORE_THRESHOLD
)

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

router = APIRouter()

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.2
)


def run_rag_pipeline(payload, current_user, include_metrics: bool):
    t0 = time.perf_counter()

    semantic_cache_hit = False

    if openai_client is None or pinecone_index is None or bm25 is None:
        raise HTTPException(status_code=500, detail="Server not configured")

    role = current_user["role"]
    question = payload.question
    session_id = current_user["user_id"]

    t_embed_start = time.perf_counter()

    emb_resp = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    query_embedding = emb_resp.data[0].embedding
    embedding_tokens = emb_resp.usage.total_tokens
    embed_time = time.perf_counter() - t_embed_start

    cached_answer, _ = semantic_cache_lookup(role, query_embedding)

    if cached_answer:
        semantic_cache_hit = True

        total_time = time.perf_counter() - t0

        if not include_metrics:
            return {"answer": cached_answer["answer"]}

        return {
            "answer": cached_answer["answer"],
            "latency": {
                "total": round(total_time, 3),
                "embedding": round(embed_time, 3)
            },
            "usage": {
                "embedding_tokens": embedding_tokens,
                "llm_input_tokens": 0,
                "llm_output_tokens": 0,
                "reranker_calls": 0
            },
            "cache": {
                "semantic_cache_hit": True
            }
        }

    t_retrieval_start = time.perf_counter()

    try:
        query_sparse = bm25.encode_queries([question])[0]
    except Exception:
        query_sparse = None

    args = {
        "vector": query_embedding,
        "top_k": TOP_K,
        "include_metadata": True,
        "filter": {role: {"$eq": True}}
    }

    if query_sparse:
        args["sparse_vector"] = query_sparse

    results = pinecone_index.query(**args)
    retrieval_time = time.perf_counter() - t_retrieval_start

    if not results.matches:
        total_time = time.perf_counter() - t0

        if not include_metrics:
            return {"answer": "No data found"}

        return {
            "answer": "No data found",
            "latency": {
                "total": round(total_time, 3),
                "embedding": round(embed_time, 3),
                "retrieval": round(retrieval_time, 3)
            },
            "usage": {
                "embedding_tokens": embedding_tokens,
                "llm_input_tokens": 0,
                "llm_output_tokens": 0,
                "reranker_calls": 0
            },
            "cache": {
                "semantic_cache_hit": False
            }
        }

    allowed = []
    for m in results.matches:
        meta = m.metadata or {}
        allowed.append({
            "chunk": meta.get("text", ""),
            "metadata": meta,
            "id": m.id
        })

    t_rerank_start = time.perf_counter()
    reranker_calls = 1
    top_children = allowed[:5]

    if co:
        docs = [a["chunk"] for a in allowed]
        try:
            rerank_response = co.rerank(
                model="rerank-v3.5",
                query=question,
                documents=docs,
                top_n=len(docs)
            )

            reranked = []
            for r in rerank_response.results:
                doc = allowed[r.index]
                doc["rerank_score"] = r.relevance_score
                reranked.append(doc)

            reranked.sort(key=lambda x: x["rerank_score"], reverse=True)

            top_children = [
                r for r in reranked
                if r["rerank_score"] >= RERANK_SCORE_THRESHOLD
            ][:3]

        except Exception:
            top_children = allowed[:3]

    rerank_time = time.perf_counter() - t_rerank_start

    context = ""
    for c in top_children:
        parent = parent_store.get(c["metadata"].get("parent_id"))
        parent_text = parent["text"] if parent else ""
        context += f"{parent_text}\n{c['chunk']}\n---\n"

    memory_messages = build_memory_context(session_id)

    t_llm_start = time.perf_counter()

    response = llm.invoke(
        memory_messages + [
            SystemMessage(content="Answer only from context."),
            HumanMessage(
                content=f"Context:\n{context}\n\nQuestion: {question}"
            )
        ]
    )

    answer = response.content

    llm_input_tokens = response.usage_metadata["input_tokens"]
    llm_output_tokens = response.usage_metadata["output_tokens"]

    llm_time = time.perf_counter() - t_llm_start
    total_time = time.perf_counter() - t0

    store_semantic_cache(
        role=role,
        question=question,
        embedding=query_embedding,
        answer={"answer": answer}
    )

    store_turn(
        session_id,
        {
            "user": question,
            "assistant": answer,
            "ts": time.time()
        }
    )

    maybe_summarize(session_id, llm)

    if not include_metrics:
        return {"answer": answer}

    return {
        "answer": answer,
        "latency": {
            "total": round(total_time, 3),
            "embedding": round(embed_time, 3),
            "retrieval": round(retrieval_time, 3),
            "reranker": round(rerank_time, 3),
            "llm": round(llm_time, 3)
        },
        "usage": {
            "embedding_tokens": embedding_tokens,
            "llm_input_tokens": llm_input_tokens,
            "llm_output_tokens": llm_output_tokens,
            "reranker_calls": reranker_calls
        },
        "cache": {
            "semantic_cache_hit": semantic_cache_hit
        }
    }


@router.post("/ask")
def ask(payload: Query, current_user=Depends(get_current_user)):
    return run_rag_pipeline(payload, current_user, include_metrics=False)


@router.post("/ask_with_metrics")
def ask_with_metrics(payload: Query, current_user=Depends(get_current_user)):
    return run_rag_pipeline(payload, current_user, include_metrics=True)
