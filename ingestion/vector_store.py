from pinecone import Pinecone, ServerlessSpec
from config import (
    PINECONE_API_KEY,
    INDEX_NAME,
    DIMENSION,
    METRIC,
    CLOUD,
    REGION,
)


def init_index():
    pc = Pinecone(api_key=PINECONE_API_KEY)

    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric=METRIC,
            spec=ServerlessSpec(
                cloud=CLOUD,
                region=REGION,
            ),
        )

    return pc.Index(INDEX_NAME)


def hybrid_upsert(index, embedded_child_chunks, sparse_vectors):
    for embedded, sparse in zip(embedded_child_chunks, sparse_vectors):
        metadata = embedded["metadata"].copy()
        metadata["text"] = embedded["text"]

        index.upsert(
            [
                {
                    "id": embedded["id"],
                    "values": embedded["values"],
                    "sparse_values": sparse,
                    "metadata": metadata,
                }
            ]
        )
