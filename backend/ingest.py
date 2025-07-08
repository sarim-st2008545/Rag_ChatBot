# In ingest.py

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
from typing import List

# Get data paths from environment variables, with local defaults
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "chroma_db")

def get_embeddings():
    """Initialize and return embeddings model"""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def process_multiple_pdfs(file_paths: List[str]):
    """
    Processes multiple PDF files and adds them to a persistent vector store
    without deleting existing data.
    """
    all_documents = []
    
    for file_path in file_paths:
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            # Add source file info to metadata
            for doc in documents:
                doc.metadata['source_file'] = os.path.basename(file_path)
            
            all_documents.extend(documents)
            print(f"✅ Loaded {len(documents)} pages from {os.path.basename(file_path)}")
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            continue
    
    if not all_documents:
        raise ValueError("No new documents found to process")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(all_documents)
    
    embeddings = get_embeddings()
    
    # --- THIS IS THE KEY CHANGE ---
    # The code no longer deletes the database. It connects to the existing one
    # (or creates it if it doesn't exist) and adds new documents.
    vector_store = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings,
        collection_name="doc_qa"
    )
    
    vector_store.add_documents(chunks)
    # vector_store.persist()
    
    print(f"✅ Added {len(chunks)} new chunks to the database from {len(file_paths)} files.")
    return vector_store, len(chunks)

def get_vector_store():
    """Get existing vector store if available"""
    embeddings = get_embeddings()
    # Use the environment variable path
    if os.path.exists(CHROMA_DB_PATH):
        return Chroma(
            collection_name="doc_qa",
            embedding_function=embeddings,
            persist_directory=CHROMA_DB_PATH
        )
    return None