import redis

from app.core.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_USERNAME,
    REDIS_PASSWORD,
)

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
        print("⚠️ Redis config missing (check .env)")

except Exception as e:
    redis_client = None
    print("⚠️ Redis unavailable:", e)
