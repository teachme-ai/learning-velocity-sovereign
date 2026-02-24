# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.11

# 1. Install System Dependencies (zstd is required for Ollama)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    zstd \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Node.js v20 via Nodesource
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# 3. Install Ollama CLI
RUN curl -fsSL https://ollama.com/install.sh | sh

# 4. Install Genkit CLI globally via npm
RUN npm install -g @genkit-ai/cli

# 5. Pre-install Core Python Packages
RUN pip install --no-cache-dir \
    pandas \
    pydantic \
    google-generativeai \
    chromadb \
    langchain \
    sentence-transformers \
    pypdf \
    langchain-text-splitters

# 6. Set Environment variables
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=development

WORKDIR /workspaces/learning-velocity-sovereign
