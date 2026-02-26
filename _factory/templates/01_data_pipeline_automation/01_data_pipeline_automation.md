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
  PHASE 1 — Deterministic Rules
════════════════════════════════════════════════════════════
[INFO]  Loading  → /Users/khalidirfan/projects/Ai Bootcamps/01_data_pipeline_automation/data/corporate_expenses.csv
[INFO]  Validated 15 rows | Rejected 0 invalid rows
[INFO]  Threshold flag: 4 rows > $10,000.00

════════════════════════════════════════════════════════════
  PHASE 2 — Probabilistic Intelligence  (llama3.2)
════════════════════════════════════════════════════════════
[LLM]   Running llama3.2 categorisation on 15 rows...
  ✅  TXN-001    | $    499.00 | Policy-Compliant
  ⚠️  TXN-002    | $  3,200.00 | Needs Review
  ✅  TXN-003    | $ 12,500.00 | Policy-Compliant
  ✅  TXN-004    | $    980.00 | Policy-Compliant
  ✅  TXN-005    | $  2,200.00 | Policy-Compliant
  ✅  TXN-006    | $ 18,750.00 | Policy-Compliant
  ✅  TXN-007    | $  8,900.00 | Policy-Compliant
  ✅  TXN-008    | $  1,100.00 | Policy-Compliant
  ✅  TXN-009    | $ 45,000.00 | Policy-Compliant
  ✅  TXN-010    | $ 32,000.00 | Policy-Compliant
  ✅  TXN-011    | $  1,850.00 | Policy-Compliant
  ✅  TXN-012    | $    750.00 | Policy-Compliant
  ✅  TXN-013    | $  3,400.00 | Policy-Compliant
  ✅  TXN-014    | $  6,200.00 | Policy-Compliant
  ✅  TXN-015    | $    920.00 | Policy-Compliant

[INFO]  Saved hybrid audit → /Users/khalidirfan/projects/Ai Bootcamps/01_data_pipeline_automation/data/flagged_expenses.csv

════════════════════════════════════════════════════════════
  HYBRID AUDIT SUMMARY
════════════════════════════════════════════════════════════
transaction_id       date  amount_usd                                          rule_flag     llm_category                                                                                                                                  llm_reason
       TXN-003 2024-01-10     12500.0 amount_usd $12,500.00 exceeds threshold $10,000.00 Policy-Compliant                                              Typical office equipment and furniture expenses are generally compliant with company policies.
       TXN-006 2024-01-18     18750.0 amount_usd $18,750.00 exceeds threshold $10,000.00 Policy-Compliant                                                  AWS reserved instances are a standard and approved IT expense under most company policies.
       TXN-009 2024-01-25     45000.0 amount_usd $45,000.00 exceeds threshold $10,000.00 Policy-Compliant Generally, providing an international relocation allowance to employees is a common business practice in certain industries and situations.
       TXN-010 2024-02-01     32000.0 amount_usd $32,000.00 exceeds threshold $10,000.00 Policy-Compliant                                                  Purchased in accordance with company's approved hardware policy for data science projects.
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

---
**[Back to Curriculum Hub](../README.md) | ~~Previous Lab~~ | [Next Lab: Session 02](../02_executive_narrative_engine/02_executive_narrative_engine.md)**
