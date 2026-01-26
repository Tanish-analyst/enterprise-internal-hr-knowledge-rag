from pinecone_text.sparse import BM25Encoder

def sparse_embed(child_chunks):
  bm25 = BM25Encoder.default()
  bm25.fit([doc.page_content for doc in child_chunks])
  sparse_vectors = bm25.encode_documents([doc.page_content for doc in child_chunks])
  return sparse_vectors
