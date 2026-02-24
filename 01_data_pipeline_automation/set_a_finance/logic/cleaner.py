"""
logic/cleaner.py  —  Hybrid Sovereign Audit Pipeline
Session 01: Data Pipeline Automation

Two-phase approach:
  Phase 1 (Deterministic) — Pydantic schema validation + threshold rules.
  Phase 2 (Probabilistic) — Ollama LLM categorises the description field.
"""

import json
import sys
from pathlib import Path
from typing import Optional

import ollama
import pandas as pd
from pydantic import BaseModel, ValidationError, field_validator


# ── Config ────────────────────────────────────────────────────────────────────

OLLAMA_MODEL     = "llama3.2"          # pull with: ollama pull llama3.2
AMOUNT_THRESHOLD = 10_000.00

BASE_DIR   = Path(__file__).resolve().parent.parent
INPUT_CSV  = BASE_DIR / "data" / "corporate_expenses.csv"
OUTPUT_CSV = BASE_DIR / "data" / "flagged_expenses.csv"


# ── Phase 1: Pydantic Schema ──────────────────────────────────────────────────

class ExpenseRecord(BaseModel):
    """Strict schema for a corporate expense row."""

    transaction_id: str
    date: str
    employee_id: str
    department: str
    category: str
    description: str
    amount_usd: float
    currency: Optional[str] = "USD"
    approved_by: Optional[str] = None

    @field_validator("amount_usd")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v < 0:
            raise ValueError(f"amount_usd cannot be negative (got {v})")
        return v

    @field_validator("transaction_id", "employee_id", "department", "category")
    @classmethod
    def fields_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Required string field cannot be empty")
        return v.strip()


def load_and_validate(path: Path) -> tuple[list[dict], list[dict]]:
    """Load CSV → validate each row against ExpenseRecord schema."""
    df = pd.read_csv(path, dtype=str)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    valid, invalid = [], []

    for idx, row in df.iterrows():
        raw = row.to_dict()
        try:
            raw["amount_usd"] = float(raw.get("amount_usd", 0))
        except ValueError:
            raw["_validation_error"] = f"Row {idx}: amount_usd is not numeric"
            invalid.append(raw)
            continue

        try:
            record = ExpenseRecord(**raw)
            valid.append(record.model_dump())
        except ValidationError as exc:
            raw["_validation_error"] = str(exc.errors())
            invalid.append(raw)

    return valid, invalid


# ── Phase 2: LLM Categorisation ───────────────────────────────────────────────

SYSTEM_PROMPT = """You are a corporate finance compliance officer.
Classify the expense description into EXACTLY one of these three categories:
  - Policy-Compliant
  - Suspicious
  - Needs Review

Respond with a JSON object only, no explanation. Format:
{"category": "<one of the three labels>", "reason": "<one sentence>"}"""


def llm_categorise(description: str, amount_usd: float) -> dict:
    """Ask Ollama to classify a single expense description."""
    user_msg = (
        f"Expense description: '{description}'\n"
        f"Amount: ${amount_usd:,.2f}\n"
        "Classify this expense."
    )
    try:
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_msg},
            ],
        )
        raw_text = response["message"]["content"].strip()
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {"category": "Needs Review", "reason": "LLM returned non-JSON response."}
    except Exception as exc:
        return {"category": "Needs Review", "reason": f"LLM error: {exc}"}


def run_llm_pass(records: list[dict]) -> list[dict]:
    """Enrich every validated record with an LLM compliance category."""
    print(f"[LLM]   Running {OLLAMA_MODEL} categorisation on {len(records)} rows...")
    enriched = []
    for rec in records:
        result = llm_categorise(rec["description"], rec["amount_usd"])
        rec["llm_category"] = result.get("category", "Needs Review")
        rec["llm_reason"]   = result.get("reason", "")
        status_icon = {"Policy-Compliant": "✅", "Suspicious": "🚨", "Needs Review": "⚠️"}.get(
            rec["llm_category"], "❓"
        )
        print(f"  {status_icon}  {rec['transaction_id']:10s} | ${rec['amount_usd']:>10,.2f} "
              f"| {rec['llm_category']}")
        enriched.append(rec)
    return enriched


# ── Phase 1b: Threshold Flagging ──────────────────────────────────────────────

def flag_high_value(records: list[dict], threshold: float = AMOUNT_THRESHOLD) -> pd.DataFrame:
    """Return rows where amount_usd exceeds the threshold."""
    df = pd.DataFrame(records)
    flagged = df[df["amount_usd"] > threshold].copy()
    flagged["rule_flag"] = flagged["amount_usd"].apply(
        lambda amt: f"amount_usd ${amt:,.2f} exceeds threshold ${threshold:,.2f}"
    )
    return flagged


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not INPUT_CSV.exists():
        print(f"[ERROR] Input file not found: {INPUT_CSV}")
        sys.exit(1)

    # ── Phase 1: Schema validation ──
    print(f"\n{'═'*60}")
    print(f"  PHASE 1 — Deterministic Rules")
    print(f"{'═'*60}")
    print(f"[INFO]  Loading  → {INPUT_CSV}")
    valid_rows, invalid_rows = load_and_validate(INPUT_CSV)
    print(f"[INFO]  Validated {len(valid_rows)} rows | Rejected {len(invalid_rows)} invalid rows")

    if invalid_rows:
        print("[WARN]  Schema violations:")
        for r in invalid_rows:
            print(f"         • {r.get('transaction_id', 'N/A')} — {r.get('_validation_error')}")

    flagged_df = flag_high_value(valid_rows)
    print(f"[INFO]  Threshold flag: {len(flagged_df)} rows > ${AMOUNT_THRESHOLD:,.2f}")

    # ── Phase 2: LLM enrichment ──
    print(f"\n{'═'*60}")
    print(f"  PHASE 2 — Probabilistic Intelligence  ({OLLAMA_MODEL})")
    print(f"{'═'*60}")
    enriched_rows = run_llm_pass(valid_rows)

    # ── Merge & save ──
    enriched_df = pd.DataFrame(enriched_rows)
    final_df    = enriched_df[enriched_df["amount_usd"] > AMOUNT_THRESHOLD].copy()
    final_df["rule_flag"] = final_df["amount_usd"].apply(
        lambda amt: f"amount_usd ${amt:,.2f} exceeds threshold ${AMOUNT_THRESHOLD:,.2f}"
    )

    final_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n[INFO]  Saved hybrid audit → {OUTPUT_CSV}")

    print(f"\n{'═'*60}")
    print(f"  HYBRID AUDIT SUMMARY")
    print(f"{'═'*60}")
    print(final_df[[
        "transaction_id", "date", "amount_usd",
        "rule_flag", "llm_category", "llm_reason"
    ]].to_string(index=False))


if __name__ == "__main__":
    main()
