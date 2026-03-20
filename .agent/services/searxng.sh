#!/usr/bin/env bash
# SearXNG — self-hosted search engine for AI agents
# Usage: ./searxng.sh start | stop | status | test

CONTAINER="searxng"
PORT="${SEARXNG_PORT:-8888}"
IMAGE="searxng/searxng:latest"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SETTINGS="${SCRIPT_DIR}/searxng_settings.yml"

case "${1:-status}" in
  start)
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
      echo "✅ SearXNG already running on port ${PORT}"
    else
      docker rm -f "$CONTAINER" 2>/dev/null
      echo "🚀 Starting SearXNG on port ${PORT}..."
      docker run -d --name "$CONTAINER" \
        -p "${PORT}:8080" \
        -v "${SETTINGS}:/etc/searxng/settings.yml:ro" \
        -e SEARXNG_BASE_URL="http://localhost:${PORT}/" \
        "$IMAGE"
      sleep 3
      if curl -sf "http://localhost:${PORT}/healthz" >/dev/null 2>&1 || \
         curl -sf "http://localhost:${PORT}/" >/dev/null 2>&1; then
        echo "✅ SearXNG ready at http://localhost:${PORT}"
      else
        echo "⏳ SearXNG starting... try again in a few seconds"
      fi
    fi
    ;;
  stop)
    docker rm -f "$CONTAINER" 2>/dev/null
    echo "🛑 SearXNG stopped"
    ;;
  status)
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER}$"; then
      echo "✅ SearXNG running on port ${PORT}"
    else
      echo "❌ SearXNG not running. Use: $0 start"
    fi
    ;;
  test)
    echo "🔍 Testing search for 'AI tools for healthcare'..."
    curl -s "http://localhost:${PORT}/search?q=AI+tools+for+healthcare&format=json" | \
      python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Got {len(d.get(\"results\",[]))} results'); [print(f'  - {r[\"title\"]}') for r in d.get('results',[])[:3]]"
    ;;
  *)
    echo "Usage: $0 {start|stop|status|test}"
    ;;
esac
