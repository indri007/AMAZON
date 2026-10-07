# Dockerfile - Environment Reproducibility untuk Eksperimen RAG HRD Q1
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency specifications
COPY requirements.txt requirements-eval.txt* ./

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir ragas deepeval bert-score rouge-score sacrebleu rank-bm25 sentence-transformers scipy statsmodels pingouin
RUN python -m spacy download en_core_web_lg || true

# Copy project files
COPY . .

# Expose port for Google Cloud Run
EXPOSE 8080
ENV PORT=8080

# Command default untuk Google Cloud Run 3D Showcase & Health Probe
CMD ["python", "server.py"]
