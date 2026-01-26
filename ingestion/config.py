import os
DATA_DIR = "hr_rag"

PARENT_CHUNK_SIZE = 1500
PARENT_CHUNK_OVERLAP = 200

CHILD_CHUNK_SIZE = 500
CHILD_CHUNK_OVERLAP = 80

SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

DENSE_MODEL = "text-embedding-3-small"

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "multi-rag-system"
DIMENSION = 1536
METRIC = "dotproduct"
CLOUD = "aws"
REGION = "us-east-1"
