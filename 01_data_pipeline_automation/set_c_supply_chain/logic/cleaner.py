"""
set_c_supply_chain/logic/cleaner.py — Inventory Audit Pipeline
Session 01: Data Pipeline Automation | Domain: Supply Chain

Two-phase approach:
  Phase 1 (Deterministic) — Pydantic schema: positive stock, unit_price > 0, valid SKU pattern.
  Phase 2 (Probabilistic) — Ollama LLM flags high-value items for procurement justification.
"""

import json
import re
import sys
from pathlib import Path

import ollama
import pandas as pd
from pydantic import BaseModel, ValidationError, field_validator

# ── Config ────────────────────────────────────────────────────────────────────

OLLAMA_MODEL     = "llama3.2"
PRICE_THRESHOLD  = 5_000.00
SKU_PATTERN      = re.compile(r"^[A-Z]{2,4}-[0-9]{4,6}$")

BASE_DIR   = Path(__file__).resolve().parent.parent
INPUT_CSV  = BASE_DIR / "data" / "inventory_records.csv"
OUTPUT_CSV = BASE_DIR / "data" / "flagged_inventory.csv"


# ── Phase 1: Pydantic Schema ──────────────────────────────────────────────────

class InventoryRecord(BaseModel):
    item_sku: str
    warehouse_id: str
    stock_quantity: int
    unit_price: float
    last_restock_date: str

    @field_validator("stock_quantity")
    @classmethod
    def stock_must_not_be_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError(f"stock_quantity cannot be negative (got {v})")
        return v

    @field_validator("unit_price")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError(f"unit_price must be > 0 (got {v})")
        return v

    @field_validator("item_sku")
    @classmethod
    def must_match_sku_pattern(cls, v: str) -> str:
        if not SKU_PATTERN.match(v.strip()):
            raise ValueError(f"SKU '{v}' does not follow WH-XXXX pattern")
        return v.strip()


def load_and_validate(path: Path) -> tuple[list[dict], list[dict]]:
    df = pd.read_csv(path, dtype=str)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    valid, invalid = [], []
    for idx, row in df.iterrows():
        raw = row.to_dict()
        try:
            raw["stock_quantity"] = int(raw.get("stock_quantity", 0))
            raw["unit_price"]     = float(raw.get("unit_price", 0))
        except ValueError:
            raw["_validation_error"] = f"Row {idx}: numeric field is non-numeric"
            invalid.append(raw)
            continue
        try:
            record = InventoryRecord(**raw)
            valid.append(record.model_dump())
        except ValidationError as exc:
            raw["_validation_error"] = str(exc.errors())
            invalid.append(raw)
    return valid, invalid


# ── Phase 2: LLM Categorisation ───────────────────────────────────────────────

SYSTEM_PROMPT = """You are a procurement compliance analyst.
Review the inventory item and classify it into EXACTLY one of:
  - Standard Stock
  - High-Value Item: Verify
  - Procurement Alert

Respond with JSON only. Format:
{"category": "<label>", "reason": "<one sentence>"}"""


def llm_categorise(sku: str, price: float, qty: int) -> dict:
    user_msg = (
        f"SKU: {sku}\n"
        f"Unit Price: ${price:,.2f}\n"
        f"Stock Quantity: {qty} units\n"
        "Classify this inventory record."
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
        return {"category": "High-Value Item: Verify", "reason": "LLM returned non-JSON response."}
    except Exception as exc:
        return {"category": "High-Value Item: Verify", "reason": f"LLM error: {exc}"}


def run_llm_pass(records: list[dict]) -> list[dict]:
    print(f"[LLM]   Running {OLLAMA_MODEL} on {len(records)} rows...")
    enriched = []
    for rec in records:
        result = llm_categorise(rec["item_sku"], rec["unit_price"], rec["stock_quantity"])
        rec["llm_category"] = result.get("category", "High-Value Item: Verify")
        rec["llm_reason"]   = result.get("reason", "")
        icon = {"Standard Stock": "✅", "Procurement Alert": "🚨", "High-Value Item: Verify": "⚠️"}.get(rec["llm_category"], "❓")
        print(f"  {icon}  {rec['item_sku']:12s} | ${rec['unit_price']:>10,.2f} | {rec['llm_category']}")
        enriched.append(rec)
    return enriched


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not INPUT_CSV.exists():
        print(f"[ERROR] Input file not found: {INPUT_CSV}")
        sys.exit(1)

    print(f"\n{'═'*60}")
    print(f"  PHASE 1 — Deterministic Rules (SKU + Stock + Price Validation)")
    print(f"{'═'*60}")
    print(f"[INFO]  Loading → {INPUT_CSV}")
    valid_rows, invalid_rows = load_and_validate(INPUT_CSV)
    print(f"[INFO]  Validated {len(valid_rows)} rows | Rejected {len(invalid_rows)} invalid rows")

    if invalid_rows:
        print("[WARN]  Violations:")
        for r in invalid_rows:
            print(f"         • {r.get('item_sku', 'N/A')} — {r.get('_validation_error')}")

    high_value = [r for r in valid_rows if r["unit_price"] > PRICE_THRESHOLD]
    print(f"[INFO]  High-value flag: {len(high_value)} rows > ${PRICE_THRESHOLD:,.2f} unit price")

    print(f"\n{'═'*60}")
    print(f"  PHASE 2 — Probabilistic Intelligence ({OLLAMA_MODEL})")
    print(f"{'═'*60}")
    enriched_rows = run_llm_pass(valid_rows)

    enriched_df = pd.DataFrame(enriched_rows)
    final_df    = enriched_df[enriched_df["unit_price"] > PRICE_THRESHOLD].copy()
    final_df["rule_flag"] = final_df["unit_price"].apply(
        lambda p: f"unit_price ${p:,.2f} exceeds threshold ${PRICE_THRESHOLD:,.2f}"
    )
    final_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\n[INFO]  Saved → {OUTPUT_CSV}")

    print(f"\n{'═'*60}")
    print(f"  INVENTORY AUDIT SUMMARY")
    print(f"{'═'*60}")
    print(final_df[["item_sku", "warehouse_id", "unit_price", "stock_quantity", "llm_category", "llm_reason"]].to_string(index=False))


if __name__ == "__main__":
    main()
