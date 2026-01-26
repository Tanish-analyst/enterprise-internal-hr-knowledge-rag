from loader import load_documents
from preprocessor import preprocess
from chunker import parent_chunk, child_chunk
from embedder import dense_embed
from hybrid_encoder import sparse_embed
from vector_store import init_index, hybrid_upsert


def run_pipeline():
    print("[1] Loading documents...")
    documents = load_documents()

    print("[2] Preprocessing & merging...")
    merged_docs = preprocess(documents)

    print("[3] Parent chunking...")
    parent_chunks = parent_chunk(merged_docs)

    print("[4] Child chunking...")
    child_chunks = child_chunk(parent_chunks)

    print("[5] Dense embeddings...")
    embedded_child_chunks = dense_embed(child_chunks)

    print("[6] Sparse embeddings...")
    sparse_vectors = sparse_embed(child_chunks)

    print("[7] Initializing Pinecone index...")
    index = init_index()

    print("[8] Hybrid upsert...")
    hybrid_upsert(index, embedded_child_chunks, sparse_vectors)

    print("✅ Ingestion pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()
