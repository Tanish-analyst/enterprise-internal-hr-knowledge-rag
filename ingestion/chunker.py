from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import (
    PARENT_CHUNK_SIZE,
    PARENT_CHUNK_OVERLAP,
    CHILD_CHUNK_SIZE,
    CHILD_CHUNK_OVERLAP,
    SEPARATORS,
)


def parent_chunk(merged_docs):
    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=PARENT_CHUNK_SIZE,
        chunk_overlap=PARENT_CHUNK_OVERLAP,
        separators=SEPARATORS,
    )

    parent_chunks = []

    for doc in merged_docs:
        splits = parent_splitter.split_text(doc.page_content)

        clean_base = (
            doc.metadata["source"]
            .replace(" ", "_")
            .replace("/", "_")
        )

        for i, text in enumerate(splits):
            parent_meta = doc.metadata.copy()
            parent_meta["parent_id"] = f"{clean_base}_parent_{i}"

            parent_chunks.append(
                Document(
                    page_content=text,
                    metadata=parent_meta,
                )
            )

    return parent_chunks


def child_chunk(parent_chunks):
    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHILD_CHUNK_SIZE,
        chunk_overlap=CHILD_CHUNK_OVERLAP,
        separators=SEPARATORS,
    )

    child_chunks = []

    for parent in parent_chunks:
        splits = child_splitter.split_text(parent.page_content)

        for j, text in enumerate(splits):
            child_meta = parent.metadata.copy()
            child_meta["child_id"] = (
                f"{parent.metadata['parent_id']}_child_{j}"
            )

            child_chunks.append(
                Document(
                    page_content=text,
                    metadata=child_meta,
                )
            )

    return child_chunks
