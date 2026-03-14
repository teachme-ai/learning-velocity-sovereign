#!/bin/bash
# Bootstrap a fresh GitHub Codespace for AI Bootcamp lab execution.
# After this script completes, run verify_env.py to confirm all checks pass.

set -e

echo "=== AI Bootcamp Codespace Bootstrap ==="

# ── 1. Install Ollama and pull required model ──────────────────────────────────
echo ""
echo "[1/4] Installing Ollama..."
if command -v ollama &>/dev/null; then
    echo "      Ollama already installed — skipping install."
else
    curl -fsSL https://ollama.com/install.sh | sh
fi

echo "      Starting Ollama service..."
ollama serve &>/tmp/ollama.log &
sleep 5

echo "      Pulling llama3.2:1b (this may take a few minutes)..."
ollama pull llama3.2:1b
echo "      ✅ Ollama ready."

# ── 2. Set up Genkit Python venv ───────────────────────────────────────────────
echo ""
echo "[2/4] Setting up Genkit venv at /tmp/genkit_env..."
if [ -d /tmp/genkit_env ]; then
    echo "      Existing venv found — reinstalling packages."
fi
python3 -m venv /tmp/genkit_env
source /tmp/genkit_env/bin/activate
pip install --quiet --upgrade pip
pip install --quiet genkit genkit-plugin-ollama pydantic fastapi uvicorn pandas jinja2 pyyaml rich
echo "      ✅ Genkit venv ready."

# ── 3. Install project-level Python dependencies ──────────────────────────────
echo ""
echo "[3/4] Installing project dependencies..."
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../../" && pwd)"
if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    pip install --quiet -r "$PROJECT_ROOT/requirements.txt"
    echo "      ✅ requirements.txt installed."
else
    echo "      No requirements.txt found — skipping."
fi

# ── 4. Confirm environment ─────────────────────────────────────────────────────
echo ""
echo "[4/4] Running Guardian verification..."
python3 "$PROJECT_ROOT/.agent/skills/guardian/scripts/verify_env.py"

echo ""
echo "=== Bootstrap complete. ==="
echo "If any checks above show ❌, review the error and re-run this script."
