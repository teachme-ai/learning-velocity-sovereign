# Lab 01: Data Pipeline Automation — Sovereign Audit
**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 The Objective
Welcome to the start of your Sovereign AI journey! In this lab, we are building a **Hybrid Sovereign Audit Pipeline**. Our mission is to protect our enterprise's financial integrity by combining the rigid rules of code with the nuanced intelligence of local LLM orchestration.

---

## ⚙️ 1. Environment Setup
Copy and paste this block into your terminal to prepare your lab environment.

```bash
# 1. Create and Activate Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install Core Lab Dependencies
pip install pandas pydantic ollama

# 3. Pull Sovereign Intelligence (Local LLM)
ollama pull llama3.2

# 4. Verification Check
ls -F data/
# Expected: corporate_expenses.csv
```

---

## 🛠️ 2. Step-by-Step Execution
Follow these commands in sequence to run the audit pipeline.

### Phase A: The Deterministic Pass
We start by applying hard-coded rules and Pydantic schema validation.

```bash
# Execute the Audit Logic
# Run from within the 01_data_pipeline_automation/ directory
python3 logic/cleaner.py
```

### Phase B: Verification
Verify that the hybrid audit successfully generated our review file.

```bash
# Check for generated flagged expenses
ls data/flagged_expenses.csv

# Preview the High-Risk findings
head -n 5 data/flagged_expenses.csv
```

---

## 📈 [INTEGRATOR] Proof of Work
**Focus**: *Operational implementation.*

Successfully running `cleaner.py` results in a hybrid summary. Below is your target output:
```text
════════════════════════════════════════════════════════════
  PHASE 1 — Deterministic Rules (Pydantic + Thresholds)
════════════════════════════════════════════════════════════
[INFO]  Validated 15 rows | Verified schema integrity.
[INFO]  Threshold flag: 4 rows exceeding $10,000.00 ceiling.

════════════════════════════════════════════════════════════
  PHASE 2 — Probabilistic Intelligence (llama3.2)
════════════════════════════════════════════════════════════
[LLM]   Running categorisation...
  ✅  TXN-001    | $    499.00 | Policy-Compliant
  🚨  TXN-003    | $ 12,500.00 | Flagged: High Value
```

---

## 🏗️ [ARCHITECT] Proof of Work
**Focus**: *Governance and Security.*

The Pydantic shield prevents invalid data ingestion. You can test this by running a security audit against intentionally broken data.
```bash
# Architect Check: Verify rejection of invalid transactions
# (Conceptual: Running a validator against logic/test_architect.py)
python3 logic/cleaner.py --test-security
```
Target Result:
```text
═══ ARCHITECT VALIDATION TEST ═══
Rejected Row: INVALID-001 | Error: amount_usd cannot be negative
[GOVERNANCE RESULT] System prevented invalid ingestion.
```
