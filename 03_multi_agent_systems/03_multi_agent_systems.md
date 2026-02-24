# Lab 03: Multi-Agent Systems — Sovereign Audit Committee
**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 The Objective
Welcome to the frontier of Agentic Workflows! In this lab, we orchestrate a **Sovereign Audit Committee**. You will build a multi-agent sequential pipeline using **Firebase Genkit** to ensure forensic accuracy and strategic depth in corporate auditing.

---

## ⚙️ 1. Environment Setup
Copy and paste this block to prepare your multi-agent architecture.

```bash
# 1. Create and Activate Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install Genkit & Sovereign Intelligence
pip install genkit genkit-plugin-google-genai pydantic flask

# 3. Configure Security Keys
export GEMINI_API_KEY='your-key-here'

# 4. Verify Path Integrity
ls logic/audit_flow.py
# Expected: audit_flow.py exists
```

---

## 🛠️ 2. Step-by-Step Execution
Follow these commands to launch your committee deliberation.

### Phase A: Orchestration
We run the refined Genkit flow which wraps our Forensic, Strategist, and Critic brains.

```bash
# Execute the Committee Flow
python3 logic/audit_flow.py
```

### Phase B: Verification
Confirm that the deliberation was processed and the quality gate was passed.

```bash
# Check the final committee response (if saved to file)
# Note: In this lab, we primarily verify via terminal logs
# or the Genkit Dev UI (Reflection Server on port 3100)
```

---

## 📈 [INTEGRATOR] Proof of Work
**Focus**: *Flow and Orchestration.*

Successful committee orchestration results in a tiered deliberation. Below is your target terminal proof:
```text
--- Starting Sovereign Audit Committee ---

[STEP 1] Forensic Investigator analyzing data...
 [OK] Found 3 violations.

[STEP 2] Risk Strategist drafting summary...
 [OK] Strategy draft complete.

[STEP 3] Executive Critic reviewing report...
 [OK] Tone: Exceptionally professional and balanced.
 [OK] Advice: Includes clear, prioritized recommendations.

--- Final Approved Boardroom Report ---

**Boardroom Audit Summary**
Analysis indicates 3 high-priority policy violations requiring immediate remediation.

*Tone Verified: Professional.*
```

---

## 🏗️ [ARCHITECT] Proof of Work
**Focus**: *Critic Pattern Governance.*

The Critic agent enforces a **Quality Gate**. Below is the Pydantic check that ensures the Critic provides actionable feedback.

```python
# ARCHITECT EVIDENCE: Quality Gate Schema
class CriticOutput(BaseModel):
    tone_evaluation: str = Field(description='Check for Tone')
    critique: str = Field(description='Actionable feedback')
    final_report: str = Field(description='The approved Markdown')
```
Target Result:
```text
[OK] Tone: Exceptionally professional and balanced.
[OK] Advice: Includes clear, prioritized recommendations.
--- Final Approved Boardroom Report ---
```
