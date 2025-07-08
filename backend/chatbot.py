from groq import Groq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel

load_dotenv()

# Get data path from environment variable
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "chroma_db")

class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None

def get_vector_store():
    """Get existing vector store if available from the persistent path."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # Check the correct path
    if os.path.exists(CHROMA_DB_PATH):
        return Chroma(
            collection_name="doc_qa",
            embedding_function=embeddings,
            persist_directory=CHROMA_DB_PATH # Use the correct path
        )
    print(f"Warning: Vector store not found at {CHROMA_DB_PATH}")
    return None

def get_enhanced_response(query: str):
    """Core RAG functionality"""
    vector_store = get_vector_store()
    if not vector_store:
        return None
    
    strategies = [
        lambda: vector_store.similarity_search(query, k=5),
        lambda: vector_store.max_marginal_relevance_search(query, k=3)
    ]
    
    for strategy in strategies:
        try:
            docs = strategy()
            if docs:
                return docs
        except Exception as e:
            continue
    
    return None

def generate_response(message: str) -> ChatResponse:
    """Generate response using Groq and context - used by both API and UI"""
    docs = get_enhanced_response(message)
    if not docs:
        return ChatResponse(
            response="No relevant documents found",
            success=False,
            error="No documents"
        )
    
    context = "\n\n---\n\n".join(
        f"Document {i}:\n{doc.page_content}" 
        for i, doc in enumerate(docs, 1))
    
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        response = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Answer using ONLY this context:\n{context}\n\nQuestion: {message}"
            }],
            model="llama-3.3-70b-versatile",
            temperature=0.3
        )
        return ChatResponse(
            response=response.choices[0].message.content,
            success=True
        )
    except Exception as e:
        return ChatResponse(
            response=f"Error: {str(e)}",
            success=False,
            error=str(e))