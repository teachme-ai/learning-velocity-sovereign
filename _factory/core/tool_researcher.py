"""
Tool Researcher — discovers low-code AI tools via SearXNG (primary) / Tavily (fallback) + LLM curation.
"""
import os
import sys

# Resolve search.py path relative to this file
_SEARCH_SCRIPT = os.path.join(
    os.path.dirname(__file__), "../../.agent/skills/web_search/scripts"
)


def _import_search():
    """Import the search function from the web_search skill."""
    if _SEARCH_SCRIPT not in sys.path:
        sys.path.insert(0, _SEARCH_SCRIPT)
    from search import search
    return search


def research_tools(industry, use_cases, llm_caller):
    """
    Research and select 2-3 low-code AI tools for the given industry.

    Args:
        industry:   Industry name string.
        use_cases:  List of use case strings.
        llm_caller: Callable that takes a prompt string and returns parsed JSON.

    Returns:
        List of dicts: [{name, url, setup_requirements, reason}]
    """
    use_cases_str = ", ".join(use_cases) if use_cases else "general AI applications"
    query = f"top low code AI tools for {industry} {use_cases_str} deployable in github codespaces or visual interfaces"

    # Search: SearXNG → Tavily → LLM knowledge
    search_context = ""
    try:
        search_fn = _import_search()
        results = search_fn(query, mode="research", max_results=5)
        source = results.get("source", "unknown")
        snippets = []
        for r in results.get("results", []):
            snippets.append(f"- {r['title']}: {r['content'][:200]}")
        if results.get("answer"):
            snippets.insert(0, f"Summary: {results['answer']}")
        search_context = "\n".join(snippets)
        if search_context:
            search_context = f"[Source: {source}]\n{search_context}"
    except Exception:
        search_context = "Web search unavailable. Use your training knowledge."

    prompt = f"""You are an AI curriculum tool researcher.

Industry: {industry}
Use Cases: {use_cases_str}

Web research results:
{search_context}

Select exactly 2-3 tools for this curriculum. Rules:
1. Prioritize Codespace-executable tools (e.g. Python libraries, CLI tools, open-source frameworks).
2. Visual/external interfaces (Make.com, Lovable, Google AI Studio, n8n) are valid secondaries.
3. Tools must have minimal technical barrier for the target audience.
4. Do NOT blindly copy tools from the search results — validate and reason about each choice.

Return ONLY a JSON array:
[{{"name": "...", "url": "...", "setup_requirements": "...", "reason": "..."}}]
"""
    result = llm_caller(prompt)
    if isinstance(result, list):
        return result
    if isinstance(result, dict) and "tools" in result:
        return result["tools"]
    return []
