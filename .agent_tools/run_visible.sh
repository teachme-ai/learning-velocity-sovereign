#!/bin/bash
# ============================================================
# Amazon Q Agent — Transparent Command Runner
# ============================================================
# This script wraps command execution so that everything
# the agent runs is visible in real-time via tail -f.
#
# Usage:  ./run_visible.sh "your command here" [working_dir]
# Watch:  tail -f /tmp/q_agent_log.txt
# ============================================================

LOG="/tmp/q_agent_log.txt"
CMD="$1"
CWD="${2:-$(pwd)}"
TIMESTAMP=$(date '+%H:%M:%S')

touch "$LOG"

{
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "⏱  $TIMESTAMP  │  📂 $CWD"
  echo "▶  $CMD"
  echo "────────────────────────────────────────────────────────"
} >> "$LOG"

cd "$CWD" 2>/dev/null || cd /tmp

# Execute and tee output to both log and stdout
eval "$CMD" 2>&1 | while IFS= read -r line; do
  echo "$line" >> "$LOG"
  echo "$line"
done

EXIT_CODE=${PIPESTATUS[0]}

{
  echo "────────────────────────────────────────────────────────"
  if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Exit: $EXIT_CODE  │  Completed at $(date '+%H:%M:%S')"
  else
    echo "❌ Exit: $EXIT_CODE  │  Failed at $(date '+%H:%M:%S')"
  fi
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
} >> "$LOG"

exit $EXIT_CODE
