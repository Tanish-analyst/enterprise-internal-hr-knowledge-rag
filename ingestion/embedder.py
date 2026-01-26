from openai import OpenAI
from config import DENSE_MODEL


client = OpenAI()


def dense_embed(child_chunks):
    embedded_child_chunks = []

    for doc in child_chunks:
        resp = client.embeddings.create(
            model=DENSE_MODEL,
            input=doc.page_content,
        )

        vec = resp.data[0].embedding

        embedded_child_chunks.append(
            {
                "id": doc.metadata["child_id"],
                "values": vec,
                "metadata": doc.metadata,
                "text": doc.page_content,
            }
        )

    return embedded_child_chunks
