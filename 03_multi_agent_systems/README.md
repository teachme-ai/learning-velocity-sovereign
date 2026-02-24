# Session 03: Multi-Agent Systems

## Overview

In this session you will build a **Sovereign Audit Committee** — a three-agent AI pipeline
where specialized agents collaborate, critique one another, and enforce quality gates.
You will learn how to define agent roles via system instructions, pass structured findings
between agents using Pydantic schemas, and implement **The Critic Pattern**: an agent that
is mandated to find weaknesses and force a revision cycle before any output is approved.

The session has two tracks:
- **`logic/audit_committee.py`** — pure Python baseline (no framework)
- **`logic/genkit_audit_py/main.py`** — Firebase Genkit Python SDK with full Developer UI observability

---

## Learning Outcomes
- [x] LO1: Define specialized agent roles and system instructions.
- [x] LO2: Orchestrate sequential and parallel agent workflows.
- [x] LO3: Implement "The Critic" pattern for automated quality control.

---

## [INTEGRATOR] Lab

> **Goal:** Run the three-agent pipeline and observe the inter-agent dialogue.

### Step 1 — Run the Python Baseline

```bash
cd "03_multi_agent_systems"
python3 -m venv .venv && source .venv/bin/activate
pip install google-genai pandas
python logic/audit_committee.py
```

**Expected output:**
- Agent 1 logs found violations
- Agent 2 assigns a Risk Rating + total exposure
- Agent 3 identifies ≥2 weaknesses and reveals a revised strategy
- Full committee report saved → `data/committee_report.md`

### Step 2 — Read the Report

Open `data/committee_report.md`. Compare:
- The **Strategist's original draft** (3 bullet mitigations)
- The **Critic's revised strategy** (which must address each weakness)

**Reflection question:** Why did The Critic reject the first draft? What was missing?

---

## [ARCHITECT] Lab

> **Goal:** Use the Genkit Developer UI to inspect the "internal brain" of the multi-agent pipeline — observing each agent as a traced Action span.

### Step 1 — Start the Engine

```bash
cd "/Users/khalidirfan/projects/Ai Bootcamps/03_multi_agent_systems/logic/genkit_audit_py"
source .venv/bin/activate && source ~/.zshrc
npx genkit-cli start -- .venv/bin/python3 main.py
```

The terminal will print:

```
Genkit Developer UI: http://localhost:4000
```

### Step 2 — Access the UI

Open **http://localhost:4000** in your browser.

Navigate to the **Flows** tab in the left sidebar. You will see `auditCommitteeFlow` listed.

### Step 3 — Run a Trace

Click `auditCommitteeFlow` → **Run** tab.

Paste this input and click **Run**:

```json
{
  "csv_data": "transaction_id,date,employee_id,department,description,amount_usd,approved_by\nTXN-003,2024-01-10,EMP-099,Finance,Ergonomic workstation,12500,mgr-ali\nTXN-006,2024-01-18,EMP-077,Engineering,AWS reserved instance,18750,mgr-ali\nTXN-009,2024-01-25,EMP-088,Operations,International relocation,45000,cfo-wright\nTXN-010,2024-02-01,EMP-022,Engineering,GPU server for ML,32000,cto-hassan"
}
```

Watch the terminal — you will see the three agents deliberating in sequence.

### Step 4 — Analyze the Brain

Once the flow completes, click **View trace** (or open the **Inspect** tab).

You will see the full trace tree:

```
auditCommitteeFlow  (root span)
 ├── generate  → Forensic Investigator  (ForensicReport schema)
 ├── generate  → Risk Strategist        (StrategyDraft schema)
 └── generate  → Executive Critic       (CriticOutput schema, attempt 1)
```

**Click each `generate` Action span** and examine:

| Span | What to look for |
|---|---|
| **Forensic Investigator** | `output.violations[]` — each transaction flagged with rule, severity, approval_issue |
| **Risk Strategist** | `output.risk_rating`, `output.total_exposure_usd`, `output.mitigations[]` — the first draft |
| **Executive Critic** | `output.weaknesses[]` — the ≥2 mandated weaknesses, `output.revised_strategy` — the improved version |

### Step 5 — The Critic Debrief

In the Critic span, compare:
- **Draft strategy** (passed in from Risk Strategist, visible in the `prompt` field)
- **Weaknesses** found (`weaknesses[0]` and `weaknesses[1]`)
- **Revised strategy** (`revised_strategy` field)

**Architect question:** The `CriticOutput` Pydantic schema has `min_length=2` on `weaknesses`.  
What happens if the model tries to return only one weakness? Trace the retry loop in `main.py` — where does the guard live?

---

## Governance Notes

- **The Critic Pattern** is a software-enforced quality gate — the schema constraint (`min_length=2`) ensures the LLM cannot skip revision regardless of prompt compliance.
- In production, The Critic could be replaced by a human reviewer webhook — the Genkit trace gives an immutable audit log of every decision.
- `mgr-ali` approving $12,500 and $18,750 without executive sign-off is a **real-world internal controls failure** — this pipeline would flag it automatically at scale.
