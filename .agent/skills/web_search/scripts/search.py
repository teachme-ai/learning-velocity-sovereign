"""
Web Search Skill — powered by Tavily
Usage:
    python3 search.py "your query here"
    python3 search.py "your query" --mode research   # deep search, more results
    python3 search.py "your query" --mode news        # recent news only
    python3 search.py "your query" --output json      # machine-readable output
"""

import os
import sys
import json
import argparse
from pathlib import Path


def load_env():
    """Load .env file from project root if TAVILY_API_KEY not already in environment."""
    if os.environ.get("TAVILY_API_KEY"):
        return
    env_path = Path(__file__).resolve().parents[4] / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


def search(query, mode="general", max_results=5):
    """
    Run a Tavily search and return structured results.

    Args:
        query:       Search query string
        mode:        "general" | "research" | "news"
        max_results: Number of results to return (1-10)

    Returns:
        dict with keys: query, answer, results (list of {title, url, content, score})
    """
    load_env()
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise EnvironmentError("TAVILY_API_KEY not set. Add it to .env or export it.")

    from tavily import TavilyClient
    client = TavilyClient(api_key=api_key)

    search_depth = "advanced" if mode == "research" else "basic"
    topic = "news" if mode == "news" else "general"

    response = client.search(
        query=query,
        search_depth=search_depth,
        topic=topic,
        max_results=max_results,
        include_answer=True,
    )

    return {
        "query": query,
        "answer": response.get("answer", ""),
        "results": [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "content": r.get("content", ""),
                "score": round(r.get("score", 0), 3),
            }
            for r in response.get("results", [])
        ],
    }


def format_results(data, output_format="text"):
    if output_format == "json":
        return json.dumps(data, indent=2)

    lines = []
    lines.append(f"\n🔍 Query: {data['query']}")
    lines.append("─" * 60)

    if data["answer"]:
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
    parser = argparse.ArgumentParser(description="Tavily Web Search Skill")
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
        sys.exit(1)
