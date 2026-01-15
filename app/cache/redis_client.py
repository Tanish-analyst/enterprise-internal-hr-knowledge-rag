import os
import redis

ENABLE_REDIS = os.getenv("ENABLE_REDIS", "false").lower() == "true"

if not ENABLE_REDIS:
    redis_client = None
    print("ℹ️ Redis disabled by config")
    return
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

redis_client = None

try:
    if REDIS_HOST and REDIS_PASSWORD:
        redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            username=REDIS_USERNAME,
            password=REDIS_PASSWORD,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2,
        )
        redis_client.ping()
        print("✅ Redis connected")
    else:
        print("ℹ️ Redis not configured (env vars missing)")
except Exception as e:
    redis_client = None
    print("⚠️ Redis unavailable:", e)
