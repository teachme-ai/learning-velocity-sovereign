"""
Web Search Skill — SearXNG primary, Tavily fallback.

SearXNG: Self-hosted, free, unlimited. Requires Docker container running.
Tavily:  Cloud API, 1000/mo free tier. Requires TAVILY_API_KEY.

Usage:
    python3 search.py "your query here"
    python3 search.py "your query" --mode research
    python3 search.py "your query" --output json
"""

import os
import json
import argparse
from pathlib import Path

import requests as _requests

SEARXNG_URL = os.environ.get("SEARXNG_URL", "http://localhost:8888")


def load_env():
    """Load .env from project root if keys not already set."""
    if os.environ.get("TAVILY_API_KEY") and os.environ.get("SEARXNG_URL"):
        return
    env_path = Path(__file__).resolve().parents[4] / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


def _searxng_search(query, max_results=5):
    """Query local SearXNG instance. Returns standardized dict."""
    url = f"{SEARXNG_URL}/search"
    params = {"q": query, "format": "json", "categories": "general"}
    resp = _requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    results = []
    for r in data.get("results", [])[:max_results]:
        results.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "content": r.get("content", ""),
            "score": round(r.get("score", 0), 3),
        })
    return {"query": query, "answer": "", "results": results, "source": "searxng"}


def _tavily_search(query, mode="general", max_results=5):
    """Query Tavily cloud API. Returns standardized dict."""
    load_env()
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise EnvironmentError("TAVILY_API_KEY not set")
    from tavily import TavilyClient
    client = TavilyClient(api_key=api_key)
    search_depth = "advanced" if mode == "research" else "basic"
    topic = "news" if mode == "news" else "general"
    response = client.search(
        query=query, search_depth=search_depth, topic=topic,
        max_results=max_results, include_answer=True,
    )
    results = [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "content": r.get("content", ""),
            "score": round(r.get("score", 0), 3),
        }
        for r in response.get("results", [])
    ]
    return {"query": query, "answer": response.get("answer", ""), "results": results, "source": "tavily"}


def search(query, mode="general", max_results=5):
    """
    Search with SearXNG first, fall back to Tavily if unavailable.

    Returns:
        dict with keys: query, answer, results [{title, url, content, score}], source
    """
    # Primary: SearXNG (free, unlimited)
    try:
        result = _searxng_search(query, max_results)
        if result["results"]:
            return result
    except Exception:
        pass

    # Fallback: Tavily (cloud, rate-limited)
    try:
        return _tavily_search(query, mode, max_results)
    except Exception:
        pass

    return {"query": query, "answer": "", "results": [], "source": "none"}


def format_results(data, output_format="text"):
    if output_format == "json":
        return json.dumps(data, indent=2)
    lines = []
    src = data.get("source", "unknown")
    lines.append(f"\n🔍 Query: {data['query']}  [via {src}]")
    lines.append("─" * 60)
    if data.get("answer"):
        lines.append(f"\n📌 Summary:\n{data['answer']}")
        lines.append("─" * 60)
    lines.append(f"\n📄 Top {len(data['results'])} Results:\n")
    for i, r in enumerate(data["results"], 1):
        lines.append(f"{i}. {r['title']}")
        lines.append(f"   🔗 {r['url']}")
        lines.append(f"   {r['content'][:200].strip()}...")
        lines.append(f"   Relevance: {r['score']}")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Search (SearXNG → Tavily)")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--mode", choices=["general", "research", "news"], default="general")
    parser.add_argument("--max", type=int, default=5, help="Max results (1-10)")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()
    try:
        data = search(args.query, mode=args.mode, max_results=args.max)
        print(format_results(data, output_format=args.output))
    except Exception as e:
        print(f"❌ Search failed: {e}")
        exit(1)
