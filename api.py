# api.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ingest import process_documents
import os
import shutil
from chatbot import chat_interface
from typing import List

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        # Clear existing data directory
        if os.path.exists("data"):
            shutil.rmtree("data")
        os.makedirs("data")
        
        # Save uploaded files
        for file in files:
            if not file.filename.lower().endswith('.pdf'):
                continue
            file_path = os.path.join("data", file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        
        # Process documents
        process_documents()
        return {"message": "Files uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/")
async def chat(message: str):
    try:
        response = chat_interface(message, [])
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))