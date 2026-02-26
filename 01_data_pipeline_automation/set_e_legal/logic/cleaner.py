"""
set_e_legal/logic/cleaner.py — Contract Review Audit Pipeline
Session 01: Data Pipeline Automation | Domain: Legal

Two-phase approach:
  Phase 1 (Deterministic) — Pydantic schema: positive value, known contract types, no future dates.
  Phase 2 (Probabilistic) — Ollama LLM flags high-value contracts for legal risk review.
"""

import json
import sys
from datetime import date
from pathlib import Path
from typing import Literal

import ollama
import pandas as pd
from pydantic import BaseModel, ValidationError, field_validator

# ── Config ────────────────────────────────────────────────────────────────────

OLLAMA_MODEL       = "llama3.2"
VALUE_THRESHOLD    = 1_000_000.00
VALID_TYPES        = {"NDA", "SaaS Agreement", "Vendor MSA", "Employment", "Acquisition"}

BASE_DIR   = Path(__file__).resolve().parent.parent
INPUT_CSV  = BASE_DIR / "data" / "contract_reviews.csv"
OUTPUT_CSV = BASE_DIR / "data" / "flagged_contracts.csv"


# ── Phase 1: Pydantic Schema ──────────────────────────────────────────────────

class ContractRecord(BaseModel):
    contract_id: str
    review_date: str
    contract_type: str
    contract_value_usd: float
    reviewing_party: str

    @field_validator("contract_value_usd")
    @classmethod
    def value_must_not_be_negative(cls, v: float) -> float:
        if v < 0:
            raise ValueError(f"contract_value_usd cannot be negative (got {v})")
        return v

    @field_validator("contract_type")
    @classmethod
    def must_be_known_type(cls, v: str) -> str:
        if not v or v.strip() not in VALID_TYPES:
            raise ValueError(f"Unknown contract_type: '{v}'. Expected one of {VALID_TYPES}")
        return v.strip()

    @field_validator("review_date")
    @classmethod
    def no_future_dates(cls, v: str) -> str:
        try:
            review = date.fromisoformat(v)
            if review > date.today():
                raise ValueError(f"review_date '{v}' is in the future.")
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
            raw["contract_value_usd"] = float(raw.get("contract_value_usd", 0))
        except ValueError:
            raw["_validation_error"] = f"Row {idx}: contract_value_usd is not numeric"
            invalid.append(raw)
            continue
        try:
            record = ContractRecord(**raw)
            valid.append(record.model_dump())
        except ValidationError as exc:
            raw["_validation_error"] = str(exc.errors())
            invalid.append(raw)
    return valid, invalid


# ── Phase 2: LLM Categorisation ───────────────────────────────────────────────

SYSTEM_PROMPT = """You are a senior legal compliance officer at a law firm.
Review the contract entry and classify it into EXACTLY one of:
  - Standard Review
  - Escalate to Partner
  - Red Flag: Legal Risk

Respond with JSON only. Format:
{"category": "<label>", "reason": "<one sentence>"}"""


def llm_categorise(contract_type: str, value: float, party: str) -> dict:
    user_msg = (
        f"Contract Type: {contract_type}\n"
        f"Contract Value: ${value:,.2f}\n"
        f"Reviewing Party: {party}\n"
        "Classify this contract for legal risk."
    )
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_msg},
            ],
        )
        return json.loads(response["message"]["content"].strip())
    except json.JSONDecodeError:
        return {"category": "Escalate to Partner", "reason": "LLM returned non-JSON response."}
    except Exception as exc:
        return {"category": "Escalate to Partner", "reason": f"LLM error: {exc}"}


def run_llm_pass(records: list[dict]) -> list[dict]:
    print(f"[LLM]   Running {OLLAMA_MODEL} on {len(records)} rows...")
    enriched = []
    for rec in records:
        result = llm_categorise(rec["contract_type"], rec["contract_value_usd"], rec["reviewing_party"])
        rec["llm_category"] = result.get("category", "Escalate to Partner")
        rec["llm_reason"]   = result.get("reason", "")
        icon = {"Standard Review": "✅", "Red Flag: Legal Risk": "🚨", "Escalate to Partner": "⚠️"}.get(rec["llm_category"], "❓")
        print(f"  {icon}  {rec['contract_id']:10s} | ${rec['contract_value_usd']:>12,.2f} | {rec['llm_category']}")
        enriched.append(rec)
    return enriched


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not INPUT_CSV.exists():
        print(f"[ERROR] Input file not found: {INPUT_CSV}")
        sys.exit(1)

    print(f"\n{'═'*60}")
    print(f"  PHASE 1 — Deterministic Rules (Contract Type + Value Validation)")
    print(f"{'═'*60}")
    print(f"[INFO]  Loading → {INPUT_CSV}")
    valid_rows, invalid_rows = load_and_validate(INPUT_CSV)
    print(f"[INFO]  Validated {len(valid_rows)} rows | Rejected {len(invalid_rows)} invalid rows")

    if invalid_rows:
        print("[WARN]  Violations:")
        for r in invalid_rows:
            print(f"         • {r.get('contract_id', 'N/A')} — {r.get('_validation_error')}")

    high_value = [r for r in valid_rows if r["contract_value_usd"] > VALUE_THRESHOLD]
    print(f"[INFO]  Escalation flag: {len(high_value)} contracts > ${VALUE_THRESHOLD:,.2f}")

    print(f"\n{'═'*60}")
    print(f"  PHASE 2 — Probabilistic Intelligence ({OLLAMA_MODEL})")
    print(f"{'═'*60}")
    enriched_rows = run_llm_pass(valid_rows)

    enriched_df = pd.DataFrame(enriched_rows)
    final_df    = enriched_df[enriched_df["contract_value_usd"] > VALUE_THRESHOLD].copy()
    final_df["rule_flag"] = final_df["contract_value_usd"].apply(
        lambda v: f"contract_value ${v:,.2f} exceeds threshold ${VALUE_THRESHOLD:,.2f}"
    )
    final_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n[INFO]  Saved → {OUTPUT_CSV}")

    print(f"\n{'═'*60}")
    print(f"  CONTRACT AUDIT SUMMARY")
    print(f"{'═'*60}")
    print(final_df[["contract_id", "contract_type", "contract_value_usd", "rule_flag", "llm_category", "llm_reason"]].to_string(index=False))


if __name__ == "__main__":
    main()
