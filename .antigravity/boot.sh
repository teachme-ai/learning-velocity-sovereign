#!/bin/bash
# .antigravity/boot.sh - Environment Initialization Script

echo "🚀 Starting AI Bootcamp Environment Initialization..."

# 1. Ensure absolute paths aren't an issue for internal tooling
export BOOTCAMP_ROOT=$(pwd)

# 2. Check for Ollama and models
if command -v ollama &> /dev/null
then
    echo "✅ Ollama detected. Verifying local models..."
    # Background pulls to avoid blocking startup if already present
    ollama pull llama3.2 &
    ollama pull llama3.2:1b &
    ollama pull nomic-embed-text &
else
    echo "⚠️ Ollama not found. Please ensure it is installed in the container via Docker-in-Docker."
fi

# 3. Verify Python environment
echo "🐍 Verifying Python 3.11 environments..."
python --version

# 4. Final readiness signal
echo "✨ Environment Ready. Happy Hacking, Facilitator!"
