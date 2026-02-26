# Lab 02: Executive Narrative Engine — Strategic Synthesis
**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 The Objective
Welcome back! In this lab, we build an **Executive Narrative Engine**. We are moving from raw data to strategic insight by using Gemini 2.5 Flash to synthesize audit findings into a high-grade board-level memo.

---

## ⚙️ 1. Environment Setup
Copy and paste this block into your terminal to prepare your session.

```bash
# 1. Activate your Sovereignty Environment
# Run from within the 02_executive_narrative_engine/ directory
source .venv/bin/activate || python3 -m venv .venv && source .venv/bin/activate

# 2. Install Strategy Engines
pip install pandas pydantic google-genai

# 3. Configure API Gateway
export GEMINI_API_KEY='your-key-here'

# 4. Data Verification
ls -F data/
# Expected: sample_data.csv
```

---

## 🛠️ 2. Step-by-Step Execution
Follow these commands in sequence to generate your board-level report.

### Phase A: Narrative Synthesis
We will run the engine to process flagged transactions from Session 01.

```bash
# Generate the Executive Memo
python3 logic/narrative_gen.py
```

### Phase B: Output Verification
Confirm that the AI has successfully drafted the board document.

```bash
# Verify memo creation
ls data/executive_memo.md

# Preview the AI's strategic summary
head -n 20 data/executive_memo.md
```

---

## 📈 [INTEGRATOR] Proof of Work
**Focus**: *Narrative generation.*

Below is the verified **Executive Board Memo** synthesized from the high-risk flags. Note the transition from numbers to systemic risk assessment.

```markdown
**Board Memo**
**Subject:** Review of High-Value Transaction Flags

**Executive Summary**
Analysis of recent transactions reveals a pattern where essential operational needs (AWS, R&D) are exceeding automated $10k thresholds, indicating policy misalignment rather than non-compliance.
```

---

## 🏗️ [ARCHITECT] Proof of Work
**Focus**: *Prompt Governance.*

As an Architect, you control the **System Instructions**. Below is the governance block that enforces the "Cyber-Sovereign" tone.

```python
# ARCHITECT EVIDENCE: Sovereign Prompt Governance
SYSTEM_PROMPT = """You are a Senior Corporate Auditor reporting to the Board.
TRANSFORM raw audit data into a strategic 'Cyber-Sovereign' narrative.
- Tone: Professional, Enterprise-Focused.
"""
```
Target Result:
```text
[INFO] Connecting to gemini-2.5-flash...
[INFO] Generating Executive Board Memo...
[OK] Response validated and saved to 'executive_memo.md'.
```

---
**[Back to Curriculum Hub](../README.md) | [Previous Lab: Session 01](../01_data_pipeline_automation/01_data_pipeline_automation.md) | [Next Lab: Session 03](../03_multi_agent_systems/set_a_finance/03_finance_swarm.md)**
