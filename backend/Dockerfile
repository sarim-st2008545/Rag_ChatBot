# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY backend/ .

# Create necessary directories
RUN mkdir -p data chroma_db

# Environment variables
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Create necessary directories with proper permissions
RUN mkdir -p /app/data /app/chroma_db && \
    chmod 777 /app/data /app/chroma_db

# Set environment variables for ChromaDB
ENV CHROMA_DB_PATH=/app/chroma_db
ENV ALLOW_RESET=TRUE

# Use uvicorn directly
CMD ["uvicorn", "fast:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]