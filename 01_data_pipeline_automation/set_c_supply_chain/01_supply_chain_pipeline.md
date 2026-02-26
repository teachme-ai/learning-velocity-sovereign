# Session 01: Supply Chain Data Pipeline

## [INTEGRATOR] Track

### Overview
This stage automates the generation and cleansing of supply chain inventory logs, focusing on SKU standardizations, pricing integrity, and reality checks against negative stock values.

### Execution
Run the inventory validator logic to ensure anomalies are safely scrubbed:
```bash
python3 01_data_pipeline_automation/set_c_supply_chain/logic/inventory_validator.py
```

## [ARCHITECT] Track

### Validation Pipeline
The backend process verifies the flags correctly classify and quantify SKU errors (`MALFORMED_SKU`), physical reality discrepancies (`NEGATIVE_STOCK`), and out-of-bounds metrics (`INVALID_PRICE`).

### Validation Output
Inventory Validation complete.
Total rows processed: 50
Rows with Validation Flags: 23
Validated output saved to /tmp/supply_chain_output/scrubbed_inventory.csv---

# [VALIDATE]
python3 01_data_pipeline_automation/set_c_supply_chain/logic/inventory_validator.py
# Verify flags properly classify supply anomalies and outputs scrubbed inventory.

---
**[Back to Curriculum Hub](../../README.md) | ~~Previous Lab~~ | [Next Lab: Session 02](../../02_executive_narrative_engine/set_c_supply_chain/02_supply_chain_narrative.md)**
