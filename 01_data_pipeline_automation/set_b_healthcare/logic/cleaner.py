"""
set_b_healthcare/logic/cleaner.py — Healthcare Billing Audit Pipeline
Session 01: Data Pipeline Automation | Domain: Healthcare

Two-phase approach:
  Phase 1 (Deterministic) — Pydantic schema: ICD-10 format, positive cost, no future dates.
  Phase 2 (Probabilistic) — Ollama LLM reviews high-cost procedures for clinical necessity.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Optional

import ollama
import pandas as pd
from pydantic import BaseModel, ValidationError, field_validator

# ── Config ────────────────────────────────────────────────────────────────────

OLLAMA_MODEL       = "llama3.2"
COST_THRESHOLD     = 10_000.00
ICD10_PATTERN      = re.compile(r"^[A-Z][0-9]{2}(\.[0-9A-Z]{1,4})?$")

BASE_DIR   = Path(__file__).resolve().parent.parent
INPUT_CSV  = BASE_DIR / "data" / "patient_billing.csv"
OUTPUT_CSV = BASE_DIR / "data" / "flagged_billing.csv"


# ── Phase 1: Pydantic Schema ──────────────────────────────────────────────────

class PatientBillingRecord(BaseModel):
    patient_id: str
    admission_date: str
    diagnosis_code: str
    treatment_cost: float
    insurance_provider: str

    @field_validator("treatment_cost")
    @classmethod
    def cost_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError(f"treatment_cost cannot be negative (got {v})")
        return v

    @field_validator("diagnosis_code")
    @classmethod
    def must_be_valid_icd10(cls, v: str) -> str:
        if not ICD10_PATTERN.match(v.strip()):
            raise ValueError(f"Invalid ICD-10 code format: '{v}'")
        return v.strip()

    @field_validator("admission_date")
    @classmethod
    def no_future_dates(cls, v: str) -> str:
        try:
            admission = date.fromisoformat(v)
            if admission > date.today():
                raise ValueError(f"admission_date '{v}' is in the future.")
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
        return v


def load_and_validate(path: Path) -> tuple[list[dict], list[dict]]:
    df = pd.read_csv(path, dtype=str)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    valid, invalid = [], []
    for idx, row in df.iterrows():
        raw = row.to_dict()
        try:
            raw["treatment_cost"] = float(raw.get("treatment_cost", 0))
        except ValueError:
            raw["_validation_error"] = f"Row {idx}: treatment_cost is not numeric"
            invalid.append(raw)
            continue
        try:
            record = PatientBillingRecord(**raw)
            valid.append(record.model_dump())
        except ValidationError as exc:
            raw["_validation_error"] = str(exc.errors())
            invalid.append(raw)
    return valid, invalid


# ── Phase 2: LLM Categorisation ───────────────────────────────────────────────

SYSTEM_PROMPT = """You are a hospital billing compliance officer.
Review the billing entry and classify it into EXACTLY one of:
  - Clinically Justified
  - Requires Peer Review
  - Suspected Upcoding

Respond with JSON only. Format:
{"category": "<label>", "reason": "<one sentence>"}"""


def llm_categorise(diagnosis_code: str, cost: float, provider: str) -> dict:
    user_msg = (
        f"Diagnosis Code: {diagnosis_code}\n"
        f"Treatment Cost: ${cost:,.2f}\n"
        f"Insurance Provider: {provider}\n"
        "Classify this billing record."
    )
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
        )
        return json.loads(response["message"]["content"].strip())
    except json.JSONDecodeError:
        return {"category": "Requires Peer Review", "reason": "LLM returned non-JSON response."}
    except Exception as exc:
        return {"category": "Requires Peer Review", "reason": f"LLM error: {exc}"}


def run_llm_pass(records: list[dict]) -> list[dict]:
    print(f"[LLM]   Running {OLLAMA_MODEL} on {len(records)} rows...")
    enriched = []
    for rec in records:
        result = llm_categorise(rec["diagnosis_code"], rec["treatment_cost"], rec["insurance_provider"])
        rec["llm_category"] = result.get("category", "Requires Peer Review")
        rec["llm_reason"]   = result.get("reason", "")
        icon = {"Clinically Justified": "✅", "Suspected Upcoding": "🚨", "Requires Peer Review": "⚠️"}.get(rec["llm_category"], "❓")
        print(f"  {icon}  {rec['patient_id']:10s} | ${rec['treatment_cost']:>10,.2f} | {rec['llm_category']}")
        enriched.append(rec)
    return enriched


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not INPUT_CSV.exists():
        print(f"[ERROR] Input file not found: {INPUT_CSV}")
        sys.exit(1)

    print(f"\n{'═'*60}")
    print(f"  PHASE 1 — Deterministic Rules (ICD-10 + Cost Validation)")
    print(f"{'═'*60}")
    print(f"[INFO]  Loading → {INPUT_CSV}")
    valid_rows, invalid_rows = load_and_validate(INPUT_CSV)
    print(f"[INFO]  Validated {len(valid_rows)} rows | Rejected {len(invalid_rows)} invalid rows")

    if invalid_rows:
        print("[WARN]  Violations:")
        for r in invalid_rows:
            print(f"         • {r.get('patient_id', 'N/A')} — {r.get('_validation_error')}")

    high_cost = [r for r in valid_rows if r["treatment_cost"] > COST_THRESHOLD]
    print(f"[INFO]  High-cost flag: {len(high_cost)} rows > ${COST_THRESHOLD:,.2f}")

    print(f"\n{'═'*60}")
    print(f"  PHASE 2 — Probabilistic Intelligence ({OLLAMA_MODEL})")
    print(f"{'═'*60}")
    enriched_rows = run_llm_pass(valid_rows)

    enriched_df = pd.DataFrame(enriched_rows)
    final_df    = enriched_df[enriched_df["treatment_cost"] > COST_THRESHOLD].copy()
    final_df["rule_flag"] = final_df["treatment_cost"].apply(
        lambda c: f"treatment_cost ${c:,.2f} exceeds threshold ${COST_THRESHOLD:,.2f}"
    )
    final_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n[INFO]  Saved → {OUTPUT_CSV}")

    print(f"\n{'═'*60}")
    print(f"  BILLING AUDIT SUMMARY")
    print(f"{'═'*60}")
    print(final_df[["patient_id", "admission_date", "treatment_cost", "diagnosis_code", "llm_category", "llm_reason"]].to_string(index=False))


if __name__ == "__main__":
    main()
