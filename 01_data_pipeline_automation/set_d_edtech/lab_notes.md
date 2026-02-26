# Lab Notes: Session 01 — Student Assessment Audit Pipeline (Set D)

## 🎯 Objective
Validate student assessment records using Pydantic rules (score range 0-100, valid course codes, no future submissions) and a local LLM to flag at-risk learners and academic integrity concerns.

---

## 🛠️ Step 1: Run

```bash
python3 01_data_pipeline_automation/set_d_edtech/logic/cleaner.py
```

---

## 📋 [INTEGRATOR] Expected Evidence

**Phase 1** rejects:
- Out-of-range scores (STU-004: -5.0 | STU-005: 105.0)
- Missing course code (STU-008)
- Future submission date (STU-015: 2026-12-01)

**Phase 2** LLM reviews at-risk students (score < 50):
- STU-003: 55.0 (borderline) | STU-010: 42.0

**Target Terminal Summary:**
```text
════════════════════════════════════════
  ASSESSMENT AUDIT SUMMARY
════════════════════════════════════════
student_id  course_code  score  llm_category
   STU-010       ML-301   42.0  At-Risk Student: Intervene
```

---

## 🏗️ [ARCHITECT] Schema Design Notes

**Rule 1 — Score Range:** `0 <= score <= 100`
**Rule 2 — Code Format:** Regex `^[A-Z]{2,4}-[0-9]{3}$`
**Rule 3 — Future Date Block:** `submission_date <= today()`
