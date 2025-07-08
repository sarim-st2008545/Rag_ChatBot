# Document Q&A Chatbot

This project is a sophisticated Question & Answer chatbot built with a Retrieval-Augmented Generation (RAG) architecture. It allows users to upload PDF documents, process them into a searchable knowledge base, and ask questions related to their content. The chatbot uses a powerful language model to provide answers grounded in the provided documents, complete with source citations.

---

## Features

* **PDF Document Upload**: Users can upload one or more PDF files to create a knowledge base.
* **Intelligent Q&A**: Ask questions in natural language and receive context-aware answers.
* **Persistent Memory**: The chatbot remembers the content of all uploaded documents for the duration of a session.
* **Simple UI**: A clean, intuitive, and user-friendly chat interface built with React.
* **Containerized Application**: The entire application is containerized with Docker for easy setup and deployment.

---
## Tech Stack

* **Backend**: Python with FastAPI
* **Frontend**: JavaScript with React.js
* **AI/NLP**:
    * **LLM**: Groq with Llama 3 `llama-3.3-70b-versatile`
    * **Embeddings**: Hugging Face `all-MiniLM-L6-v2`
    * **Framework**: LangChain
* **Vector Database**: ChromaDB
* **Containerization**: Docker & Docker Compose

---

## Setup and Installation

This project is fully containerized, so all you need is Docker and Docker Compose installed on your machine.

**Step 1: Clone the Repository**

```bash
git clone <your-repository-url>
cd <your-repository-name>
```

**Step 2: Create Your Environment File**

The application requires an API key from Groq.

1.  Create a new file named `.env` in the backend/ directory of the project by copying the template:
    ```bash
    cp .env.example .env
    ```
2.  Open the `.env` file and add your Groq API key.. (for testing I have also shared my own API key in the project ppt, you can use that!):
    ```
    GROQ_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
    ```

**Step 3: Build and Run the Application**

Use Docker Compose to build the images and run the containers:

```bash
docker-compose up --build -d
```

The `-d` flag runs the containers in detached mode.

**Step 4: Access the Application**

* **Frontend (Chat UI)**: Open your browser and go to `http://localhost:3000`
* **Backend (API Docs)**: The API documentation is available at `http://localhost:8000/docs`

---

## API Documentation

The backend provides the following RESTful API endpoints:

| Method | Endpoint | Description                                                               |
| :----- | :------- | :------------------------------------------------------------------------ |
| `POST` | `/upload`  | Uploads one or more PDF files to be processed and stored.                 |
| `POST` | `/chat`    | Submits a user's question and receives a context-aware answer.            |
| `GET`  | `/`        | A health check endpoint to confirm if the backend is running.             |

---

## Usage

1.  **Open the Application**: Navigate to `http://localhost:3000` in your web browser.
2.  **Upload Documents**: Click the paperclip icon (📎), select one or more PDF files, and click "Upload & Process".
3.  **Ask Questions**: Once the documents are processed, type your questions into the input bar and press Enter or click the send button (➤).

## These images show the chatbot running successfully!
![This image shows the chatbot when asked several questions, as the knowledge base was empty, it could'nt answer any question!](test_Images\before_rag.png)

![This image shows the chatbot when the files were successfully uploaded to the knowledge base!](test_Images\files_uploaded.png)

![This image shows the chatbot after multiple files were uploaded to the knowledge base, after that AI was able to answer those same questions!](test_Images\after_rag.png)