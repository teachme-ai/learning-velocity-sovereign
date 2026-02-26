# Session 01: Legal Data Pipeline

## [INTEGRATOR] Track

### Overview
This step introduces scanning unstructured legal text blocks. Instead of parsing standard rows and columns, the scanner parses contracts directly for massive operational risk liabilities.

### Execution
Identify and categorize non-compete and high liability text clauses:
```bash
python3 01_data_pipeline_automation/set_e_legal/logic/clause_scanner.py
```

## [ARCHITECT] Track

### Validation Pipeline
The regex matching rules correctly partition unstructured "HIGH" and "MEDIUM" risk liabilities out of standard legal framework language.

### Validation Output
Legal Contract Scanning complete.
Total clauses evaluated: 30
High risks found: 2
Extraction mapped to /tmp/legal_output/scanned_clauses.json---

# [VALIDATE]
python3 01_data_pipeline_automation/set_e_legal/logic/clause_scanner.py
# Verify unstructured clauses map directly to high severity dictionaries.

---
**[Back to Curriculum Hub](../../README.md) | ~~Previous Lab~~ | [Next Lab: Session 02](../../02_executive_narrative_engine/set_e_legal/02_legal_narrative.md)**
