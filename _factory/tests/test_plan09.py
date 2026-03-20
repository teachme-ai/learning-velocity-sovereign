"""
Plan 09 Integration Test
Tests: manifest validation -> persona loading -> tool research -> session planning
"""
import json
import yaml
import os
import sys

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# ── Step 1: Load and validate manifest ────────────────────────────────
print("=" * 70)
print("STEP 1: MANIFEST VALIDATION")
print("=" * 70)
from _factory.core.manifest_validator import ManifestValidator

with open("_factory/manifests/test_plan09_manifest.yaml") as f:
    raw = yaml.safe_load(f)

v = ManifestValidator(raw)
valid = v.validate()
merged = v.get_merged()
print(f"Valid: {valid}")
if v.warnings:
    print(f"Warnings:\n{v.report()}")
print(f"persona_source: {merged.get('persona_source')}")
print(f"audience: {merged.get('audience')}")
print(f"tracks: {merged.get('tracks')}")
print()

# ── Step 2: Load persona ──────────────────────────────────────────────
print("=" * 70)
print("STEP 2: PERSONA LOADING")
print("=" * 70)
from _factory.core.persona_parser import load_persona

persona_path = merged["persona_source"]
persona = load_persona(persona_path)
print(f"marketMaturityScore: {persona['marketMaturityScore']}")
print(f"decisionStyle: {persona['decisionStyle']}")
print(f"topPriorities ({len(persona['topPriorities'])}):")
for p in persona["topPriorities"]:
    if isinstance(p, dict):
        print(f"  - {p['name']} -> artifact: {p.get('portfolioArtifact', 'N/A')}")
    else:
        print(f"  - {p}")
print()

# ── Step 3: Tool Research (mock LLM) ─────────────────────────────────
print("=" * 70)
print("STEP 3: TOOL RESEARCH (mock LLM)")
print("=" * 70)
from _factory.core.tool_researcher import research_tools


def mock_tool_llm(prompt):
    assert "Retail" in prompt, "Prompt should mention Retail"
    assert "Personalization" in prompt or "Churn" in prompt, "Prompt should mention use cases"
    print("  [LLM prompt contains: industry=Retail, use_cases=present] OK")
    return [
        {
            "name": "Google AI Studio",
            "url": "https://aistudio.google.com",
            "setup_requirements": "Browser only, Google account",
            "reason": "No-code prompt engineering and model testing for non-technical users",
        },
        {
            "name": "n8n",
            "url": "https://n8n.io",
            "setup_requirements": "Docker or cloud hosted",
            "reason": "Visual workflow automation -- connects data sources to AI models without code",
        },
        {
            "name": "Streamlit",
            "url": "https://streamlit.io",
            "setup_requirements": "pip install streamlit",
            "reason": "Low-code Python dashboards -- minimal code for Business Analysts",
        },
    ]


tools = research_tools(
    merged["industry"],
    merged.get("use_cases", []),
    mock_tool_llm,
)
print(f"Tools discovered: {len(tools)}")
for t in tools:
    print(f"  Tool: {t['name']} -- {t['reason']}")
    print(f"     Setup: {t['setup_requirements']}")
print()

# ── Step 4: Session Planning (mock LLM) ──────────────────────────────
print("=" * 70)
print("STEP 4: SESSION PLANNING (mock LLM)")
print("=" * 70)
from _factory.core.session_planner import plan_sessions


def mock_session_llm(prompt):
    assert "stick to exactly 8 sessions" in prompt, "Should enforce 8 sessions for maturity <= 45"
    assert "Collaborative" in prompt, "Should include decision style"
    print("  [LLM prompt enforces: 8-session cap, includes decision style] OK")

    return {
        "total_sessions": 8,
        "justification": "Maturity score is 38 (below 45). Sticking to the standard 8-session bootcamp.",
        "sessions": [
            {"session_number": 1, "title": "Data Pipeline for Retail Analytics", "description": "Build automated data ingestion from POS and CRM systems", "portfolio_artifact": "Automated Weekly Report Pipeline", "tools_used": ["Google AI Studio", "n8n"]},
            {"session_number": 2, "title": "Customer Narrative Engine", "description": "Generate executive summaries from customer behavior data", "portfolio_artifact": "Executive Customer Insights Report", "tools_used": ["Google AI Studio"]},
            {"session_number": 3, "title": "Multi-Agent Churn Detection", "description": "Deploy agent swarm to identify at-risk customer segments", "portfolio_artifact": "Churn Risk Alert System", "tools_used": ["n8n"]},
            {"session_number": 4, "title": "Product Knowledge RAG", "description": "Build a retrieval system over product catalog and reviews", "portfolio_artifact": "Self-Service Product Q&A Bot", "tools_used": ["Streamlit"]},
            {"session_number": 5, "title": "Analytics Dashboard UI", "description": "Create interactive dashboards for pricing and personalization KPIs", "portfolio_artifact": "Self-Service Analytics Dashboard", "tools_used": ["Streamlit"]},
            {"session_number": 6, "title": "Pipeline Observability", "description": "Add tracing and monitoring to all automated workflows", "portfolio_artifact": "Observability Dashboard with Alerts", "tools_used": ["n8n", "Streamlit"]},
            {"session_number": 7, "title": "GDPR Compliance & Data Security", "description": "Implement PII scrubbing and consent tracking for EU compliance", "portfolio_artifact": "GDPR Compliance Audit Report", "tools_used": ["Google AI Studio"]},
            {"session_number": 8, "title": "Capstone: Meeting Intelligence Agent", "description": "End-to-end AI agent that summarizes meetings and extracts action items", "portfolio_artifact": "Meeting Intelligence Agent", "tools_used": ["Google AI Studio", "n8n", "Streamlit"]},
        ],
    }


plan = plan_sessions(persona, tools, mock_session_llm)
print(f"Total sessions: {plan['total_sessions']}")
print(f"Justification: {plan['justification']}")
print()

# ── Verification ──────────────────────────────────────────────────────
print("=" * 70)
print("VERIFICATION")
print("=" * 70)

# Check 1: Exactly 8 sessions
assert plan["total_sessions"] == 8, f"FAIL: Expected 8, got {plan['total_sessions']}"
print(f"[PASS] Session count: {plan['total_sessions']} (capped at 8 for maturity={persona['marketMaturityScore']})")

# Check 2: Every session has a portfolio artifact
all_have_artifacts = all(s.get("portfolio_artifact") for s in plan["sessions"])
assert all_have_artifacts, "FAIL: Not all sessions have portfolio artifacts"
print(f"[PASS] All {len(plan['sessions'])} sessions have portfolio artifacts")

# Check 3: No-code/low-code tools are present
all_tools_used = set()
for s in plan["sessions"]:
    all_tools_used.update(s.get("tools_used", []))
print(f"[PASS] Tools used across sessions: {sorted(all_tools_used)}")
assert "Google AI Studio" in all_tools_used, "FAIL: No-code tool missing"
assert "n8n" in all_tools_used, "FAIL: No-code tool missing"
print("[PASS] No-code platforms confirmed: Google AI Studio, n8n")

# Check 4: 8 distinct session topics
session_titles = [s["title"] for s in plan["sessions"]]
assert len(session_titles) == 8, f"FAIL: Expected 8 titles, got {len(session_titles)}"
assert len(set(session_titles)) == 8, "FAIL: Session titles not unique"
print("[PASS] 8 unique session topics generated")

print()
print("SESSION PLAN:")
print("-" * 70)
for s in plan["sessions"]:
    tools_str = ", ".join(s.get("tools_used", []))
    print(f"  Session {s['session_number']}: {s['title']}")
    print(f"    Artifact: {s['portfolio_artifact']}")
    print(f"    Tools: {tools_str}")
    print()

print("=" * 70)
print("ALL PLAN 09 TESTS PASSED")
print("=" * 70)
