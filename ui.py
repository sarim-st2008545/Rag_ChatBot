import gradio as gr
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI base URL
API_URL = "http://localhost:8000"

def upload_file(files):
    """Upload PDF files to FastAPI endpoint"""
    if not files:
        return "No files selected"
    
    responses = []
    for file in files:
        try:
            with open(file.name, "rb") as f:
                response = requests.post(
                    f"{API_URL}/upload",
                    files={"file": f}
                )
            if response.status_code == 200:
                responses.append(f"✅ {os.path.basename(file.name)}: {response.json()['message']}")
            else:
                responses.append(f"❌ {os.path.basename(file.name)}: {response.json().get('detail', 'Upload failed')}")
        except Exception as e:
            responses.append(f"❌ {os.path.basename(file.name)}: {str(e)}")
    
    return "\n".join(responses)

def chat_response(message, history):
    """Send chat message to FastAPI endpoint"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": message}
        )
        if response.status_code == 200:
            return response.json()["response"]
        return f"API Error: {response.json().get('detail', 'Unknown error')}"
    except requests.exceptions.ConnectionError:
        return "⚠️ Could not connect to API server. Is it running?"
    except Exception as e:
        return f"Error: {str(e)}"

def create_interface():
    """Create Gradio interface with upload and chat tabs"""
    with gr.Blocks(title="Document Chatbot") as demo:
        gr.Markdown("# 📄 Document Chatbot")
        gr.Markdown("Upload PDFs and ask questions about their content")
        
        with gr.Tab("Upload Documents"):
            file_input = gr.File(
                label="Upload PDFs",
                file_count="multiple",
                file_types=[".pdf"]
            )
            upload_button = gr.Button("Process Documents")
            upload_output = gr.Textbox(label="Status")
            
        with gr.Tab("Chat"):
            gr.ChatInterface(
                fn=chat_response,
                examples=["What is this document about?", "Summarize the key points"],
                title="Ask about your documents"
            )
        
        upload_button.click(
            fn=upload_file,
            inputs=file_input,
            outputs=upload_output
        )
    
    return demo

if __name__ == "__main__":
    # Check if API is running
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code != 200:
            print("⚠️ FastAPI server not running. Please start it first with:")
            print("uvicorn fastapi_app:app --reload")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("⚠️ Could not connect to FastAPI server. Please start it first with:")
        print("uvicorn fastapi_app:app --reload")
        exit(1)
    
    # Create and launch interface
    interface = create_interface()
    interface.launch()