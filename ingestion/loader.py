import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from config import DATA_DIR

def load_documents():
loader = DirectoryLoader(
DATA_DIR,
glob="**/*.pdf",
loader_cls=PyPDFLoader,
recursive=True
)

documents = loader.load()
return documents
