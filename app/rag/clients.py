import os
import cohere

from openai import OpenAI
from pinecone import Pinecone
from pinecone_text.sparse import BM25Encoder
from langchain_groq import ChatGroq

from app.core.config import (
    OPENAI_API_KEY,
    PINECONE_API_KEY,
    COHERE_API_KEY,
    GROQ_API_KEY
)

openai_client = None
pinecone_index = None
bm25 = None
co = None
groq_llm = None

if OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

if PINECONE_API_KEY:
    os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
    pc = Pinecone(api_key=PINECONE_API_KEY)
    pinecone_index = pc.Index("multi-rag-system")

bm25 = BM25Encoder.default()

if COHERE_API_KEY:
    co = cohere.ClientV2(api_key=COHERE_API_KEY)

if GROQ_API_KEY:
    groq_llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        api_key=GROQ_API_KEY
    )
