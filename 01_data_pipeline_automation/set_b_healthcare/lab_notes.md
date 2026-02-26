# Lab Notes: Session 01 — Healthcare Billing Data Pipeline (Set B)

## 🎯 Objective
Validate hospital patient billing records using a deterministic Pydantic schema combined with an LLM compliance categoriser. This mirrors a real-world hospital pre-authorization audit workflow.

---

## 🛠️ Step 1: Setup & Run

```bash
# Install dependencies (if not already done)
pip install pandas pydantic ollama

# Pull local model
ollama pull llama3.2

# Run the healthcare pipeline
python3 01_data_pipeline_automation/set_b_healthcare/logic/cleaner.py
```

---

## 📋 [INTEGRATOR] Expected Evidence

**Phase 1** rejects rows with:
- Negative treatment costs (P-10012: -$200.00)
- Invalid ICD-10 codes (P-10008: `INVALID_CODE`)
- Future admission dates (P-10015: 2026-12-31)

**Phase 2** LLM reviews high-cost procedures (> $10,000 threshold):
- P-10006: $15,500 — Hypertension (I10)
- P-10009: $48,000 — Lung Cancer (C34.10)

**Target Terminal Summary:**
```text
═══════════════════════════════════════════════
  BILLING AUDIT SUMMARY
═══════════════════════════════════════════════
patient_id  treatment_cost  diagnosis_code  llm_category
  P-10006        15500.00            I10    Requires Peer Review
  P-10009        48000.00         C34.10    Clinically Justified
```

---

## 🏗️ [ARCHITECT] Schema Design Notes

**Rule 1 — Cost Validity:** `treatment_cost > 0`
**Rule 2 — ICD-10 Format:** Regex `^[A-Z][0-9]{2}(\.[0-9A-Z]+)?$`
**Rule 3 — Temporal Sanity:** `admission_date <= today()`

The `PatientBillingRecord` Pydantic model enforces all three in a single validation pass, rejecting structurally invalid rows before the expensive LLM phase is invoked.
