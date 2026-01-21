import json
import argparse
import time
import requests
import numpy as np
from typing import List, Dict


PRICING = {
    "embedding_per_1k": 0.00002,
    "llm_input_per_1k": 0.0005,
    "llm_output_per_1k": 0.0015,
    "reranker_per_call": 0.001
}


def load_eval_data(path: str) -> List[Dict]:
    with open(path, "r") as f:
        return [json.loads(line) for line in f]


def call_api(api_url: str, token: str, question: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {"question": question}

    start = time.time()
    resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    elapsed = time.time() - start

    return elapsed, resp.json()


def compute_cost(usage: Dict) -> Dict:
    embed = usage["embedding_tokens"] / 1000 * PRICING["embedding_per_1k"]
    llm_in = usage["llm_input_tokens"] / 1000 * PRICING["llm_input_per_1k"]
    llm_out = usage["llm_output_tokens"] / 1000 * PRICING["llm_output_per_1k"]
    rerank = usage["reranker_calls"] * PRICING["reranker_per_call"]

    return {
        "total": embed + llm_in + llm_out + rerank,
        "embedding": embed,
        "llm_input": llm_in,
        "llm_output": llm_out,
        "reranker": rerank
    }


def stats(arr):
    return (
        np.percentile(arr, 50),
        np.percentile(arr, 95),
        np.percentile(arr, 99),
        np.mean(arr)
    )

def evaluate(records, api_url, token, sleep_s):

    lat_total, lat_embed, lat_ret, lat_rerank, lat_llm = [], [], [], [], []
    cost_total, cost_embed, cost_llm_in, cost_llm_out, cost_rerank = [], [], [], [], []

    for r in records:
        latency, data = call_api(api_url, token, r["question"])

        lat = data["latency"]
        usage = data["usage"]
        cost = compute_cost(usage)

        lat_total.append(lat["total"])
        lat_embed.append(lat["embedding"])
        lat_ret.append(lat["retrieval"])
        lat_rerank.append(lat["reranker"])
        lat_llm.append(lat["llm"])

        cost_total.append(cost["total"])
        cost_embed.append(cost["embedding"])
        cost_llm_in.append(cost["llm_input"])
        cost_llm_out.append(cost["llm_output"])
        cost_rerank.append(cost["reranker"])

        time.sleep(sleep_s)

    return {
        "latency": {
            "total": lat_total,
            "embedding": lat_embed,
            "retrieval": lat_ret,
            "reranker": lat_rerank,
            "llm": lat_llm
        },
        "cost": {
            "total": cost_total,
            "embedding": cost_embed,
            "llm_input": cost_llm_in,
            "llm_output": cost_llm_out,
            "reranker": cost_rerank
        }
    }


def print_summary(lat_total, cost_total):
    print("\n🔎 BENCHMARK SUMMARY (TL;DR)")
    print("-" * 60)
    print(f"• Median latency: ~{np.percentile(lat_total, 50):.1f}s")
    print(f"• P95 latency: ~{np.percentile(lat_total, 95):.1f}s")
    print(f"• P99 latency: <{np.percentile(lat_total, 99):.1f}s")
    avg_cost = np.mean(cost_total)
    print(f"• Avg cost per query: ~${avg_cost:.4f}")
    print(f"• Cost per 1K queries: ~${avg_cost * 1000:.2f}")


def print_block(title, arr, decimals=2):
    p50, p95, p99, avg = stats(arr)
    print(f"\n{title}")
    print(f"P50: {p50:.{decimals}f}")
    print(f"P95: {p95:.{decimals}f}")
    print(f"P99: {p99:.{decimals}f}")
    print(f"AVG: {avg:.{decimals}f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--api_url", required=True)
    parser.add_argument("--token", required=True)
    parser.add_argument("--sleep", type=float, default=0.3)
    args = parser.parse_args()

    records = load_eval_data(args.data)
    start = time.time()

    metrics = evaluate(records, args.api_url, args.token, args.sleep)

    elapsed = time.time() - start

    print("=" * 60)
    print("🚀 FINAL METRICS (LATENCY + COST)")
    print("=" * 60)

    print_summary(metrics["latency"]["total"], metrics["cost"]["total"])

    print_block("TOTAL LATENCY (s)", metrics["latency"]["total"])
    print_block("EMBEDDING LATENCY (s)", metrics["latency"]["embedding"])
    print_block("RETRIEVAL LATENCY (s)", metrics["latency"]["retrieval"])
    print_block("RERANKER LATENCY (s)", metrics["latency"]["reranker"])
    print_block("LLM LATENCY (s)", metrics["latency"]["llm"])

    print("\nCOST PER QUERY (USD)")
    print_block("COST", metrics["cost"]["total"], decimals=5)

    print("\nCOST BREAKDOWN (AVG PER QUERY)")
    print(f"Embedding:   ${np.mean(metrics['cost']['embedding']):.5f}")
    print(f"LLM Input:   ${np.mean(metrics['cost']['llm_input']):.5f}")
    print(f"LLM Output:  ${np.mean(metrics['cost']['llm_output']):.5f}")
    print(f"Reranker:    ${np.mean(metrics['cost']['reranker']):.5f}")

    print("\nSamples:", len(records))
    print(f"Total runtime: {elapsed:.2f}s")
    print("=" * 60)
    print("Benchmark completed without errors")


if __name__ == "__main__":
    main()
