import json
import argparse
import time
import re
from typing import List, Dict

import cohere
from langchain_groq import ChatGroq
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone_text.sparse import BM25Encoder

from app.core.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX,
    GROQ_API_KEY,
    COHERE_API_KEY,
    TOP_K,
    PINECONE_SCORE_THRESHOLD
)


def load_eval_data(path: str) -> List[Dict]:
    records = []
    with open(path, "r") as f:
        for line in f:
            records.append(json.loads(line))
    return records


def init_clients():

    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX)

    emb = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    bm25 = BM25Encoder.default()

    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY
    )

    co = cohere.Client(COHERE_API_KEY)

    return index, emb, bm25, llm, co


def retrieve(index, emb, bm25, role: str, question: str):

    dense_vec = emb.embed_query(question)
    sparse_vec = bm25.encode_queries([question])[0]

    res = index.query(
        vector=dense_vec,
        sparse_vector=sparse_vec,
        top_k=TOP_K,
        include_metadata=True,
        filter={role: {"$eq": True}}
    )

    if not res.matches:
        return []

    return [
        m for m in res.matches
        if m.score >= PINECONE_SCORE_THRESHOLD
    ]


def build_context(matches):

    chunks = []
    for m in matches:
        chunks.append(m.metadata["text"])

    return "\n\n".join(chunks)


def score_faithfulness(llm, question, answer, context):

    prompt = f"""
You are evaluating an AI answer.

Question:
{question}

Context:
{context}

Answer:
{answer}

Is the answer fully grounded in the context?
Give score from 1 to 5.
Explain briefly.

Format:
Score: <number>
Reason: <text>
"""

    resp = llm.invoke(prompt).content

    score = int(re.search(r"Score:\s*(\d)", resp).group(1))
    reason = re.search(r"Reason:\s*(.*)", resp).group(1)

    return score, reason


def score_relevance(co, question, answer):

    resp = co.rerank(
        model="rerank-english-v2.0",
        query=question,
        documents=[answer]
    )

    score = int(resp.results[0].relevance_score * 5)

    return score


def evaluate(records, index, emb, bm25, llm, co, max_q):

    faithfulness_scores = []
    relevance_scores = []

    for i, r in enumerate(records[:max_q], start=1):

        q = r["question"]
        role = r["role"]
        gt_answer = r["answer"]

        matches = retrieve(index, emb, bm25, role, q)

        if not matches:
            continue

        context = build_context(matches)

        faith_score, _ = score_faithfulness(
            llm, q, gt_answer, context
        )

        rel_score = score_relevance(
            co, q, gt_answer
        )

        faithfulness_scores.append(faith_score)
        relevance_scores.append(rel_score)

        time.sleep(1)

    avg_faith = sum(faithfulness_scores) / len(faithfulness_scores)
    avg_rel = sum(relevance_scores) / len(relevance_scores)

    return avg_faith, avg_rel


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--max_q", type=int, default=60)
    args = parser.parse_args()

    records = load_eval_data(args.data)

    index, emb, bm25, llm, co = init_clients()

    start = time.time()

    avg_faith, avg_rel = evaluate(
        records,
        index,
        emb,
        bm25,
        llm,
        co,
        args.max_q
    )

    elapsed = time.time() - start

    print("\nGENERATION METRICS")
    print("=" * 40)
    print(f"Avg Faithfulness     : {avg_faith:.3f}")
    print(f"Avg Answer Relevance : {avg_rel:.2f} / 5")
    print(f"Runtime              : {elapsed:.2f}s")
    print("=" * 40)


if __name__ == "__main__":
    main()
