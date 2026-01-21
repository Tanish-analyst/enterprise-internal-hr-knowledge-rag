from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.rag.routes import router as rag_router


app = FastAPI(title="Multi-RAG HR Assistant (Secure)")

@app.get("/")
def root():
    return {"status": "Multi-RAG HR Assistant (FastAPI) , secure mode"}

app.include_router(auth_router)
app.include_router(rag_router)
