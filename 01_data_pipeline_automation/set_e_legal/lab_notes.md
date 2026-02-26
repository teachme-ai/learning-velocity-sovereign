# Lab Notes: Session 01 — Contract Review Audit Pipeline (Set E)

## 🎯 Objective
Automate the initial triage of legal contracts using deterministic rules (valid contract types, positive values, no future dates) and a local LLM to escalate high-value contracts for partner review or red-flag for legal risk.

---

## 🛠️ Step 1: Run

```bash
python3 01_data_pipeline_automation/set_e_legal/logic/cleaner.py
```

---

## 📋 [INTEGRATOR] Expected Evidence

**Phase 1** rejects:
- Negative contract value (CTR-004: -$500.00)
- Unknown/missing contract type (CTR-008: empty)
- Future review date (CTR-015: 2026-12-01)

**Phase 2** LLM reviews high-value contracts (> $1,000,000):
- CTR-006: $5,500,000 (Acquisition) | CTR-009: $2,200,000 (Vendor MSA) | CTR-014: $8,800,000 (Acquisition)

**Target Terminal Summary:**
```text
════════════════════════════════════════════════
  CONTRACT AUDIT SUMMARY
════════════════════════════════════════════════
contract_id  contract_type  value           llm_category
    CTR-006    Acquisition   5,500,000.00   Escalate to Partner
    CTR-009     Vendor MSA   2,200,000.00   Escalate to Partner
    CTR-014    Acquisition   8,800,000.00   Red Flag: Legal Risk
```

---

## 🏗️ [ARCHITECT] Schema Design Notes

**Rule 1 — Positive Value:** `contract_value_usd >= 0`
**Rule 2 — Known Type:** Must be in `{NDA, SaaS Agreement, Vendor MSA, Employment, Acquisition}`
**Rule 3 — No Future Dates:** `review_date <= today()`
