"""
logic/audit_committee.py — The Sovereign Audit Committee
Session 03: Multi-Agent Systems

A three-agent pipeline implementing the Researcher → Strategist → Critic pattern.
Each agent has a specialized role, a distinct system instruction, and passes its
findings to the next. The Critic MUST identify weaknesses and force a revision cycle.

Agents:
  1. Forensic Investigator  — technical policy violation analysis
  2. Risk Strategist        — financial impact on quarterly budget
  3. Executive Critic       — quality gate; must find ≥2 weaknesses and revise

Brain: Gemini 2.5 Flash (via google.genai SDK)
"""

import os
import sys
from pathlib import Path
from google import genai
from google.genai import types

# ── Config ────────────────────────────────────────────────────────────────────

GEMINI_MODEL = "gemini-2.5-flash"
SEPARATOR    = "═" * 60

BASE_DIR  = Path(__file__).resolve().parent.parent
INPUT_CSV = (
    BASE_DIR.parent
    / "01_data_pipeline_automation"
    / "data"
    / "flagged_expenses.csv"
)
OUTPUT_MD = BASE_DIR / "data" / "committee_report.md"


# ── Agent Definitions ─────────────────────────────────────────────────────────

AGENTS = {
    "forensic_investigator": {
        "title": "🔍 Agent 1 — Forensic Investigator",
        "system": (
            "You are the Forensic Investigator on the Sovereign Audit Committee. "
            "Your job is to analyze raw flagged expense data and identify SPECIFIC "
            "technical policy violations. For each flagged transaction, state: "
            "(1) the exact policy rule broken, (2) the severity (HIGH / MEDIUM / LOW), "
            "(3) whether the approval chain was correctly followed. "
            "Be precise, structured, and factual. Format your output as a numbered list."
        ),
        "prompt_template": (
            "Analyze these flagged transactions for policy violations:\n\n{data}\n\n"
            "Identify every technical violation. Do not summarize — be exhaustive."
        ),
    },
    "risk_strategist": {
        "title": "♟️  Agent 2 — Risk Strategist",
        "system": (
            "You are the Risk Strategist on the Sovereign Audit Committee. "
            "You receive investigation findings and assess the FINANCIAL IMPACT "
            "on the company's quarterly budget. Quantify: total exposure, "
            "percentage of budget at risk, and projected cost if violations recur. "
            "Assign a Risk Rating: CRITICAL / HIGH / MODERATE / LOW. "
            "Propose three specific mitigation strategies with estimated cost savings."
        ),
        "prompt_template": (
            "The Forensic Investigator has produced these findings:\n\n{findings}\n\n"
            "Assess the financial impact on the quarterly budget and propose "
            "three mitigation strategies."
        ),
    },
    "executive_critic": {
        "title": "🖊️  Agent 3 — Executive Critic",
        "system": (
            "You are the Executive Critic on the Sovereign Audit Committee. "
            "Your role is QUALITY CONTROL — you must be demanding and rigorous. "
            "You MUST identify AT LEAST TWO specific weaknesses in the strategy "
            "presented to you, then provide a REVISED and IMPROVED version. "
            "Label weaknesses clearly as [WEAKNESS 1] and [WEAKNESS 2], then "
            "provide [REVISED STRATEGY] that directly addresses each weakness. "
            "Do not approve without revision — that is your mandate."
        ),
        "prompt_template": (
            "The Risk Strategist has produced this analysis:\n\n{strategy}\n\n"
            "Critique this strategy. Find at least two weaknesses, then produce "
            "a revised version that fixes them. Show your work."
        ),
    },
}


# ── Core Engine ───────────────────────────────────────────────────────────────

def build_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY not set.")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def run_agent(client: genai.Client, agent_key: str, prompt: str) -> str:
    """Call Gemini with a specific agent's persona and return its output."""
    agent = AGENTS[agent_key]
    print(f"\n{SEPARATOR}")
    print(f"  {agent['title']}")
    print(f"{SEPARATOR}")
    print(f"[THINKING]  {agent['title'].split('—')[1].strip()} is deliberating...\n")

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=agent["system"],
            temperature=0.7,
        ),
    )

    output = response.text
    print(output)
    return output


def load_csv(path: Path) -> str:
    """Load CSV as plain text for the LLM."""
    if not path.exists():
        print(f"[ERROR] Input CSV not found: {path}")
        print("  Run Session 01's cleaner.py first.")
        sys.exit(1)
    with open(path) as f:
        return f.read()


def save_report(
    csv_data: str,
    findings: str,
    strategy: str,
    critique: str,
    path: Path,
) -> None:
    """Write the full committee dialogue to Markdown."""
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"""<!-- Committee Report — Generated by audit_committee.py -->
<!-- Session 03: Multi-Agent Systems -->

# Sovereign Audit Committee Report

## Input Data
```
{csv_data.strip()}
```

---

## 🔍 Forensic Investigator — Findings

{findings}

---

## ♟️ Risk Strategist — Financial Impact & Mitigation

{strategy}

---

## 🖊️ Executive Critic — Quality Review & Revised Strategy

{critique}
"""
    path.write_text(content, encoding="utf-8")
    print(f"\n[INFO]  Full committee report saved → {path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"\n{SEPARATOR}")
    print("  SESSION 03 — The Sovereign Audit Committee")
    print(f"  Multi-Agent Pipeline: 3 Agents · {GEMINI_MODEL}")
    print(f"{SEPARATOR}")

    client   = build_client()
    csv_data = load_csv(INPUT_CSV)

    print(f"\n[INFO]  Input: {INPUT_CSV.name} loaded.")
    print(f"[INFO]  Launching 3-agent deliberation sequence...\n")

    # ── Round 1: Forensic Investigator ──
    findings = run_agent(
        client,
        "forensic_investigator",
        AGENTS["forensic_investigator"]["prompt_template"].format(data=csv_data),
    )

    # ── Round 2: Risk Strategist ──
    strategy = run_agent(
        client,
        "risk_strategist",
        AGENTS["risk_strategist"]["prompt_template"].format(findings=findings),
    )

    # ── Round 3: Executive Critic ──
    critique = run_agent(
        client,
        "executive_critic",
        AGENTS["executive_critic"]["prompt_template"].format(strategy=strategy),
    )

    # ── Save full dialogue ──
    save_report(csv_data, findings, strategy, critique, OUTPUT_MD)

    print(f"\n{SEPARATOR}")
    print("  COMMITTEE DELIBERATION COMPLETE")
    print(f"  Report → {OUTPUT_MD}")
    print(f"{SEPARATOR}\n")


if __name__ == "__main__":
    main()
