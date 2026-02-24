# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.11

# 1. Install System Dependencies & Node.js
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    zstd \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# 2. Install Ollama CLI
RUN curl -fsSL https://ollama.com/install.sh | sh

# 3. Install Genkit CLI via npm
RUN npm install -g @genkit-ai/cli

# 4. Pre-install Core Python Packages
RUN pip install --no-cache-dir \
    pandas \
    pydantic \
    google-generativeai \
    ollama \
    genkit \
    chromadb \
    pypdf \
    langchain-text-splitters

# 5. Set Environment variables
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=development

WORKDIR /workspaces/learning-velocity-sovereign
