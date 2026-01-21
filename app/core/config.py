import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX", "final-rag-trailer")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

SEMANTIC_CACHE_THRESHOLD = float(
    os.getenv("SEMANTIC_CACHE_THRESHOLD", "0.6")
)
SEMANTIC_CACHE_TTL = int(
    os.getenv("SEMANTIC_CACHE_TTL", "3600")
)

TOP_K = int(os.getenv("RAG_TOP_K", "10"))
PINECONE_SCORE_THRESHOLD = float(
    os.getenv("PINECONE_SCORE_THRESHOLD", "0.5")
)
RERANK_SCORE_THRESHOLD = float(
    os.getenv("RERANK_SCORE_THRESHOLD", "0.5")
)
