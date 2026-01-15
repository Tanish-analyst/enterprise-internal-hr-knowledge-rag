from fastapi import APIRouter, Depends, HTTPException

from app.models.query import Query
from app.core.security import get_current_user
from app.rag.clients import openai_client, pinecone_index, bm25, co, groq_llm
from app.rag.parent_store import parent_store

from app.cache.semantic_cache import (
    semantic_cache_lookup,
    store_semantic_cache
)
from langchain_core.messages import SystemMessage, HumanMessage

router = APIRouter()

@router.post("/ask")
def ask_bot(payload: Query, current_user=Depends(get_current_user)):
    if openai_client is None or pinecone_index is None or bm25 is None:
        raise HTTPException(status_code=500, detail="Server not fully configured")

    role = current_user["role"]
    question = payload.question

    q_resp = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )
    query_embedding = q_resp.data[0].embedding

    cached_answer, similarity = semantic_cache_lookup(role, query_embedding)

    if cached_answer:
        return {
            "answer": cached_answer["answer"],
            "cached": True,
            "similarity": similarity
        }

    try:
        query_sparse = bm25.encode_queries([question])[0]
    except Exception:
        query_sparse = None

    args = {
        "vector": query_embedding,
        "top_k": 10,
        "include_metadata": True
    }
    if query_sparse:
        args["sparse_vector"] = query_sparse

    results = pinecone_index.query(**args)

    WEIGHTS = {"allowed": 1, "forbidden": -100}
    allowed = []

    for match in results.matches:
        meta = match.metadata or {}
        if meta.get(role):
            allowed.append({
                "chunk": meta.get("text", ""),
                "metadata": meta,
                "final_score": (match.score or 0) + WEIGHTS["allowed"]
            })

    if not allowed:
        return {"answer": "You are not authorized to access this information."}

    docs = [a["chunk"] for a in allowed]
    top_children = allowed[:3]

    if co:
        rer = co.rerank(
            model="rerank-v3.5",
            query=question,
            documents=docs,
            top_n=3
        )
        ordered = []
        for r in rer.results:
            ordered.append(allowed[r.index])
        top_children = ordered

    context = ""
    for c in top_children:
        parent = parent_store.get(c["metadata"].get("parent_id"))
        parent_text = parent["text"] if parent else "(parent text not found)"
        context += f"[PARENT]\n{parent_text}\n\n[CHILD]\n{c['chunk']}\n\n---\n"

    if not groq_llm:
        return {"answer": "Context returned. Set GROQ_API_KEY.", "context": context}

    messages = [
        SystemMessage(content="You are an HR compliance assistant. Only answer using the provided context."),
        HumanMessage(content=f"Context:\n{context}\n\nQuestion: {question}")
    ]

    answer = groq_llm.invoke(messages).content
    store_semantic_cache(
        role=role,
        question=question,
        embedding=query_embedding,
        answer={
            "answer": answer,
            "context_used": context
        }
    )

    return {
        "answer": answer,
        "context_used": context,
        "cached": False
    }
