import json
import os
from typing import Dict, Any

PARENT_CHUNKS_FILE = "data/parent_chunks.jsonl"
parent_store: Dict[str, Dict[str, Any]] = {}

if os.path.exists(PARENT_CHUNKS_FILE):
    with open(PARENT_CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line)
                meta = obj.get("metadata", {})
                pid = meta.get("parent_id") or obj.get("id")
                parent_store[pid] = {
                    "text": obj.get("text"),
                    "metadata": meta
                }
            except Exception:
                continue
