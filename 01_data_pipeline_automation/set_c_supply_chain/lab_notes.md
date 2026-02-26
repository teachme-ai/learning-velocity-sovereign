# Lab Notes: Session 01 — Inventory Audit Pipeline (Set C)

## 🎯 Objective
Audit warehouse inventory records for supply chain integrity using deterministic rules (SKU format, stock levels, unit pricing) and a local LLM to flag high-value procurement anomalies.

---

## 🛠️ Step 1: Run

```bash
python3 01_data_pipeline_automation/set_c_supply_chain/logic/cleaner.py
```

---

## 📋 [INTEGRATOR] Expected Evidence

**Phase 1** rejects:
- Negative stock (WH-9004: -30 units)
- Zero unit price (WH-9007: $0.00)
- Invalid SKU format (BADINPUT)

**Phase 2** LLM reviews high-value items (> $5,000 per unit):
- WH-9006: $8,750 | WH-9011: $6,200 | WH-9015: $12,500

**Target Terminal Summary:**
```text
═══════════════════════════════════════
  INVENTORY AUDIT SUMMARY
═══════════════════════════════════════
item_sku  unit_price  llm_category
 WH-9006     8750.00  Procurement Alert
 WH-9011     6200.00  High-Value Item: Verify
 WH-9015    12500.00  Procurement Alert
```

---

## 🏗️ [ARCHITECT] Schema Design Notes

**Rule 1 — Stock Reality:** `stock_quantity >= 0`
**Rule 2 — Price Integrity:** `unit_price > 0`
**Rule 3 — SKU Pattern:** Regex `^[A-Z]{2,4}-[0-9]{4,6}$`
