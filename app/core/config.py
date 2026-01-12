import os

SECRET_KEY = os.getenv("SECRET_KEY", "please_set_a_real_secret_in_env")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
