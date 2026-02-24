FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# 1. Install critical system tools
RUN apt-get update && apt-get install -y zstd curl gnupg && rm -rf /var/lib/apt/lists/*

# 2. Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y nodejs

# 3. Install Ollama and Genkit
RUN curl -fsSL https://ollama.com/install.sh | sh
RUN npm install -g genkit

# 4. Install base AI libraries
RUN pip install pandas pydantic google-generativeai chromadb langchain ollama
