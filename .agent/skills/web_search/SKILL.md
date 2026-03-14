---
name: Web Search
description: 'Live internet search via Tavily. Supports general, research (deep), and news modes. Returns AI-summarised answer + ranked source URLs. Used by Amazon Q to research tools, trends, and curriculum content.'
triggers:
  - 'search the web'
  - 'search for'
  - 'look up'
  - 'find latest'
  - 'research'
  - 'what are the latest'
  - 'find tools'
---

# Web Search Skill

## Purpose
Gives Amazon Q live internet access to research topics, find tools, check trends, and gather curriculum content — without leaving the project environment.

Powered by **Tavily** — an AI-native search API that returns clean summaries + ranked sources.

## Setup
Requires `TAVILY_API_KEY` in the project `.env` file:
```
TAVILY_API_KEY=tvly-your-key-here
```

## Usage

### General search (default)
```bash
python3 .agent/skills/web_search/scripts/search.py "no-code AI tools 2024"
```

### Deep research mode (more results, advanced depth)
```bash
python3 .agent/skills/web_search/scripts/search.py "enterprise no-code AI platforms" --mode research --max 10
```

### News mode (recent articles only)
```bash
python3 .agent/skills/web_search/scripts/search.py "Flowise vs Dify 2024" --mode news
```

### JSON output (for piping into other scripts)
```bash
python3 .agent/skills/web_search/scripts/search.py "n8n alternatives" --output json
```

## Python API (used by Amazon Q directly)
```python
import sys
sys.path.insert(0, '.agent/skills/web_search/scripts')
from search import search

results = search("no-code AI tools for enterprise", mode="research", max_results=8)
print(results["answer"])          # AI-generated summary
for r in results["results"]:      # ranked sources
    print(r["title"], r["url"])
```

## Modes
| Mode | Depth | Best For |
|---|---|---|
| `general` | basic | Quick lookups, tool names, definitions |
| `research` | advanced | Comparisons, deep dives, curriculum research |
| `news` | basic | Latest releases, recent updates |

## Output Fields
- `answer` — Tavily's AI-generated summary of the query
- `results` — list of `{title, url, content, score}` ranked by relevance
