#!/bin/bash
# .antigravity/boot.sh - Environment Initialization Script

echo "🚀 Starting AI Bootcamp Environment Initialization..."

# 1. Ensure absolute paths aren't an issue for internal tooling
export BOOTCAMP_ROOT=$(pwd)

# 2. Start Ollama and pull models
if command -v ollama &> /dev/null
then
    echo "✅ Ollama detected. Starting daemon..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    
    # Wait a moment for the daemon to initialize
    sleep 3
    
    echo "📥 Initiating background model pulls..."
    nohup ollama pull llama3.2 > /tmp/pull_llama32.log 2>&1 &
    nohup ollama pull llama3.2:1b > /tmp/pull_llama1b.log 2>&1 &
    nohup ollama pull nomic-embed-text > /tmp/pull_nomic.log 2>&1 &
else
    echo "⚠️ Ollama not found. Please ensure it is installed in the container via Dockerfile."
fi

# 3. Verify Python environment
echo "🐍 Verifying Python 3.11 environments..."
python --version

# 4. Final readiness signal
echo "✨ Environment Ready. Happy Hacking, Facilitator!"
