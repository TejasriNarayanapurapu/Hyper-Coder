import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def create_vector_store(documents_path: str, persist_directory: str = "chroma_db"):
    """
    Reads text files from documents_path, splits text, creates embeddings, and stores in Chroma vector DB.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    # Load all text files
    from pathlib import Path
    docs = []
    for file_path in Path(documents_path).rglob("*.md"):  # or .txt or .py
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            docs.append(content)

    # Split into chunks
    texts = text_splitter.split_documents([{"page_content": doc} for doc in docs])

    # Create vector store
    vector_store = Chroma.from_documents(texts, embeddings, persist_directory=persist_directory)
    vector_store.persist()

    return vector_store

def load_vector_store(persist_directory: str = "chroma_db"):
    """
    Loads existing vector store from disk.
    """
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vector_store

def query_vector_store(query: str, vector_store):
    """
    Queries vector store for relevant documents.
    """
    results = vector_store.similarity_search(query, k=3)
    return results

if __name__ == "__main__":
    # Example usage
    vector_store = create_vector_store(documents_path="../data/sample_repo")
    results = query_vector_store("Explain the training script.")
    for doc in results:
        print(doc.page_content)
