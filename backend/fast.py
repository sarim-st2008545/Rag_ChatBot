from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from ingest import process_multiple_pdfs
from chatbot import generate_response
from typing import List

# Get data paths from environment variables, with local defaults
DATA_DIR = os.getenv("PDF_DATA_PATH", "data")
CHROMA_DIR = os.getenv("CHROMA_DB_PATH", "chroma_db")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    """Ensure data directories exist when the application starts."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(CHROMA_DIR, exist_ok=True)

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Handles PDF uploads and adds them to the persistent database."""
    if not all(file.filename.endswith('.pdf') for file in files):
        raise HTTPException(400, "Only PDF files are supported.")
    
    newly_uploaded_paths = []
    skipped_files = []
    
    for file in files:
        # Use the correct DATA_DIR from the environment variable
        file_path = os.path.join(DATA_DIR, file.filename)
        
        if not os.path.exists(file_path):
            try:
                content = await file.read()
                with open(file_path, "wb") as buffer:
                    buffer.write(content)
                newly_uploaded_paths.append(file_path)
            except Exception as e:
                raise HTTPException(500, f"Error saving file {file.filename}: {e}")
        else:
            skipped_files.append(file.filename)
            print(f"File '{file.filename}' already exists. Skipping.")

    if not newly_uploaded_paths:
        return {
            "message": f"No new files to process. Skipped existing files: {', '.join(skipped_files) if skipped_files else 'None'}"
        }

    try:
        # Process ONLY the newly uploaded files
        _, chunk_count = process_multiple_pdfs(newly_uploaded_paths)
        
        return {
            "message": f"Successfully processed {len(newly_uploaded_paths)} new files.",
            "chunks_added": chunk_count,
            "skipped_files": skipped_files
        }
    except Exception as e:
        raise HTTPException(500, f"Error processing PDFs: {str(e)}")

@app.post("/chat")
async def chat(message: str = Form(...)):
    """Handle chat messages using Form data."""
    try:
        chat_response = generate_response(message)
        return {"response": chat_response.response}
    except Exception as e:
        raise HTTPException(500, f"Error generating response: {str(e)}")

# @app.post("/chat-json")
# async def chat_json(request: ChatRequest):
#     """Handle chat messages using JSON."""
#     try:
#         chat_response = generate_response(request.message)
#         return {"response": chat_response.response}
#     except Exception as e:
#         raise HTTPException(500, f"Error generating response: {str(e)}")

@app.get("/")
def health_check():
    return {"status": "running"}