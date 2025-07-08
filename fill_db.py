from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import os

# Configuration
DATA_PATH = "data"  # Directory containing PDFs
CHROMA_PATH = "chroma_db"  # Directory for ChromaDB storage
COLLECTION_NAME = "document_qa"  # Collection name

# Create ChromaDB client and collection
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

def process_documents():
    # Load PDF documents from directory
    loader = PyPDFDirectoryLoader(DATA_PATH)
    documents = loader.load()
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    
    # Prepare data for ChromaDB
    docs = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        docs.append(chunk.page_content)
        metadatas.append(chunk.metadata)
        ids.append(f"doc_{i}")
    
    # Add to ChromaDB collection
    collection.upsert(
        documents=docs,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"Processed {len(chunks)} chunks into ChromaDB collection '{COLLECTION_NAME}'")

if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)
        print(f"Created {DATA_PATH} directory. Please add your PDF files there.")
    else:
        process_documents()