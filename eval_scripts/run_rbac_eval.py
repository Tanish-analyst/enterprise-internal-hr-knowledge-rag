import json
import argparse
import time
import requests
from typing import List, Dict


def load_eval_data(path: str) -> List[Dict]:
    records = []
    with open(path, "r") as f:
        for line in f:
            records.append(json.loads(line))
    return records


def call_api(api_url, token, question):

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "query": question
    }

    resp = requests.post(api_url, headers=headers, json=payload)
    return resp.status_code, resp.json()


def evaluate(records, api_url, token):

    total = len(records)
    violations = 0

    for r in records:

        q = r["question"]
        expected_access = r["allowed"]

        status, resp = call_api(api_url, token, q)

        if expected_access:
            if status != 200:
                violations += 1
        else:
            if status == 200:
                violations += 1

        time.sleep(0.2)

    return total, violations


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--api_url", type=str, required=True)
    parser.add_argument("--token", type=str, required=True)
    args = parser.parse_args()

    records = load_eval_data(args.data)

    start = time.time()

    total, violations = evaluate(
        records,
        args.api_url,
        args.token
    )

    elapsed = time.time() - start

    print("\nRBAC EVALUATION")
    print("=" * 40)
    print(f"Total queries    : {total}")
    print(f"RBAC violations  : {violations}")
    print(f"Accuracy         : {(total - violations)/total:.3f}")
    print(f"Runtime          : {elapsed:.2f}s")
    print("=" * 40)


if __name__ == "__main__":
    main()
