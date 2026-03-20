"""
Session Planner — generates a dynamic curriculum plan from persona data and tools.
"""


def plan_sessions(persona_dict, tools_list, llm_caller):
    """
    Generate a dynamic session plan based on persona and discovered tools.

    Args:
        persona_dict: Dict with topPriorities, marketMaturityScore, etc.
        tools_list:   List of tool dicts from tool_researcher.
        llm_caller:   Callable that takes a prompt and returns parsed JSON.

    Returns:
        Dict with total_sessions, justification, and sessions list.
    """
    maturity = persona_dict.get("marketMaturityScore", 30)
    priorities = persona_dict.get("topPriorities", [])
    decision_style = persona_dict.get("decisionStyle", "Balanced")

    priorities_str = ""
    for p in priorities:
        if isinstance(p, dict):
            priorities_str += f"- {p.get('name', str(p))}\n"
        else:
            priorities_str += f"- {p}\n"
    if not priorities_str:
        priorities_str = "- General AI literacy\n"

    tools_str = ""
    for t in tools_list:
        if isinstance(t, dict):
            tools_str += f"- {t.get('name', 'Unknown')}: {t.get('reason', '')}\n"
        else:
            tools_str += f"- {t}\n"
    if not tools_str:
        tools_str = "- No specific tools discovered\n"

    session_floor = 8
    allow_extra = maturity > 45

    prompt = f"""You are an AI curriculum planner. Design a session plan.

Learner Profile:
- Market Maturity Score: {maturity}
- Decision Style: {decision_style}
- Top Priorities:
{priorities_str}

Available Tools:
{tools_str}

Rules:
1. Fixed floor of {session_floor} sessions (2 hours each, 16 hours total).
2. {"Maturity score is above 45 — you MAY add 1-2 extra sessions (9 or 10 max) if justified." if allow_extra else "Maturity score is 45 or below — stick to exactly 8 sessions."}
3. Every session MUST produce a portfolioArtifact (a tangible deliverable).
4. Map the learner's top priorities to specific sessions.
5. Integrate the discovered tools into relevant sessions.

Return ONLY a JSON object:
{{
  "total_sessions": {session_floor},
  "justification": "...",
  "sessions": [
    {{
      "session_number": 1,
      "title": "...",
      "description": "...",
      "portfolio_artifact": "...",
      "tools_used": ["..."]
    }}
  ]
}}
"""
    result = llm_caller(prompt)

    if not isinstance(result, dict) or "sessions" not in result:
        return _fallback_plan(session_floor)

    # Enforce constraints
    total = result.get("total_sessions", session_floor)
    if not allow_extra:
        total = session_floor
    elif total > 10:
        total = 10
    result["total_sessions"] = total

    return result


def _fallback_plan(count):
    """Return a minimal fallback plan if LLM fails."""
    titles = [
        "Data Pipeline Automation",
        "Executive Narrative Engine",
        "Multi-Agent Systems",
        "Sovereign Knowledge RAG",
        "Advanced UI / LobeChat",
        "Observability & Tracing",
        "Sovereign Security",
        "Grand Capstone",
        "Extended: Advanced Integration",
        "Extended: Production Deployment",
    ]
    sessions = []
    for i in range(min(count, len(titles))):
        sessions.append({
            "session_number": i + 1,
            "title": titles[i],
            "description": f"Session {i+1}: {titles[i]}",
            "portfolio_artifact": f"Artifact for {titles[i]}",
            "tools_used": [],
        })
    return {
        "total_sessions": count,
        "justification": "Fallback plan — LLM was unavailable.",
        "sessions": sessions,
    }
