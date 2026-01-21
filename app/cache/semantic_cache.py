import json
import time
import hashlib
import numpy as np
from typing import Optional, Tuple
from app.cache.redis_client import redis_client
from app.core.config import SEMANTIC_CACHE_THRESHOLD, SEMANTIC_CACHE_TTL

SIM_THRESHOLD = SEMANTIC_CACHE_THRESHOLD
CACHE_TTL = SEMANTIC_CACHE_TTL

def cosine_sim(a, b) -> float:
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def make_cache_key(role: str, text: str) -> str:
    h = hashlib.md5(text.encode()).hexdigest()
    return f"semantic_cache:{role}:{h}"


def semantic_cache_lookup(
    role: str,
    query_embedding: list
) -> Tuple[Optional[dict], Optional[float]]:

    if redis_client is None:
        return None, None

    pattern = f"semantic_cache:{role}:*"
    best_match = None
    best_score = 0.0

    try:
        for key in redis_client.scan_iter(pattern):
            data = redis_client.hgetall(key)
            if not data or "embedding" not in data:
                continue

            cached_emb = json.loads(data["embedding"])
            score = cosine_sim(query_embedding, cached_emb)

            if score > best_score:
                best_score = score
                best_match = data

        if best_score >= SIM_THRESHOLD and best_match:
            print(
                f"\n⚡ REDIS SEMANTIC CACHE HIT"
                f"\n📊 Similarity: {best_score:.3f}"
            )
            return json.loads(best_match["answer"]), best_score

    except Exception as e:
        print("Semantic cache lookup failed:", e)

    return None, None


def store_semantic_cache(
    role: str,
    question: str,
    embedding: list,
    answer: dict
) -> None:

    if redis_client is None:
        return

    try:
        key = make_cache_key(role, question)
        payload = {
            "role": role,
            "question": question,
            "embedding": json.dumps(embedding),
            "answer": json.dumps(answer),
            "ts": time.time()
        }
        redis_client.hset(key, mapping=payload)
        redis_client.expire(key, CACHE_TTL)

    except Exception as e:
        print("Semantic cache store failed:", e)
