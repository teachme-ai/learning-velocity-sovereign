#!/bin/bash
# run_nano_banana.sh — Run the Nano Banana image generator using the correct venv
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSION01="$SCRIPT_DIR/01_data_pipeline_automation"

source ~/.zshrc 2>/dev/null
"$SESSION01/.venv/bin/python" "$SESSION01/assets/diagrams/test_nano_banana.py"
