import json
import argparse
import time
from typing import List, Dict

from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone_text.sparse import BM25Encoder

from app.core.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX,
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

    return index, emb, bm25


def run_retrieval(index, emb, bm25, role: str, question: str):

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

    filtered = [
        m for m in res.matches
        if m.score >= PINECONE_SCORE_THRESHOLD
    ]

    return filtered


def evaluate(records: List[Dict], index, emb, bm25):

    total = len(records)

    recall_hits = 0
    precision_sum = 0
    mrr_sum = 0

    failure_cases = []

    for r in records:

        question = r["question"]
        role = r["role"]
        gold_docs = set(r["relevant_doc_ids"])

        results = run_retrieval(index, emb, bm25, role, question)

        if not results:
            failure_cases.append({
                "question": question,
                "reason": "No retrieval results"
            })
            continue

        retrieved_ids = [
            m.metadata["doc_id"] for m in results
        ]

        hit = any(doc in gold_docs for doc in retrieved_ids)
        if hit:
            recall_hits += 1

        correct = sum(
            1 for doc in retrieved_ids if doc in gold_docs
        )
        precision_sum += correct / len(retrieved_ids)

        rr = 0
        for i, doc in enumerate(retrieved_ids):
            if doc in gold_docs:
                rr = 1 / (i + 1)
                break
        mrr_sum += rr

    recall = recall_hits / total
    precision = precision_sum / total
    mrr = mrr_sum / total

    return recall, precision, mrr, failure_cases


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data",
        type=str,
        required=True
    )
    args = parser.parse_args()

    records = load_eval_data(args.data)

    print(f"\nLoaded {len(records)} samples")

    index, emb, bm25 = init_clients()

    start = time.time()

    recall, precision, mrr, failures = evaluate(
        records, index, emb, bm25
    )

    elapsed = time.time() - start

    print("\nRETRIEVAL METRICS")
    print("=" * 40)
    print(f"Recall@{TOP_K}     : {recall:.4f}")
    print(f"Precision@{TOP_K}  : {precision:.4f}")
    print(f"MRR               : {mrr:.4f}")
    print(f"Runtime           : {elapsed:.2f}s")
    print("=" * 40)

    if failures:
        for f in failures[:5]:
            print(json.dumps(f, indent=2))


if __name__ == "__main__":
    main()
