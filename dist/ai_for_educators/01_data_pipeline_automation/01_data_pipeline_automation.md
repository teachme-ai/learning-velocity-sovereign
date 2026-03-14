**Introduction**
=====================================

Welcome to the start of your Sovereign AI journey! In this lab, we will build a hybrid sovereign audit pipeline designed to protect our enterprise's financial integrity by combining the rigid rules of code with the nuanced intelligence of local LLM orchestration.

**Business Value**
====================

The Sovereign Audit Pipeline provides significant business value in several key areas:

*   **Improved Financial Integrity**: By automating data validation and flagging, we can ensure that financial transactions are compliant with our enterprise's policies.
*   **Enhanced Risk Management**: The hybrid pipeline combines deterministic rules with probabilistic intelligence from local LLMs to provide a more comprehensive risk assessment.
*   **Increased Efficiency**: Automating the audit process reduces manual intervention, allowing our team to focus on higher-value tasks and improving overall efficiency.
*   **Better Decision-Making**: With a clear understanding of financial risks and opportunities, we can make data-driven decisions that drive business growth.

**Step-by-Step Execution**
==========================

Follow these commands in sequence to run the audit pipeline:

### Phase A: The Deterministic Pass
We start by applying hard-coded rules and Pydantic schema validation using the following command:

```bash
# Execute the Audit Logic
# Run from within the 01_data_pipeline_automation/ directory
python3 logic/cleaner.py
```

### Phase B: Verification
Verify that the hybrid audit successfully generated our review file by checking for flagged expenses and previewing high-risk findings. Below is your target output:

```text
════════════════════════════════════════════════════════════
  PHASE 1 — Deterministic Rules
════════════════════════════════════════════════════════════
[INFO]  Loading  → /Users/khalidarfan/projects/Ai Bootcamps/01_data_pipeline_automation/data/corporate_expenses.csv
[INFO]  Validated 15 rows | Rejected 0 invalid rows
[INFO]  Threshold flag: 4 rows > $10,000.00

════════════════════════════════════════════════════════════
  PHASE 2 — Probabilistic Intelligence  (llama3.2)
════════════════════════════════════════════════════════════
[LLM]   Running llama3.2 categorisation on 15 rows...
  ✅  TXN-001    | $    499.00 | Policy-Compliant
  ⚠️  TXN-002    | $  3,200.00 | Needs Review
  ✅  TXN-003    | $ 12,500.00 | Policy-Compliant
  ✅  TXN-004    | $    980.00 | Policy-Compliant
  ✅  TXN-005    | $  2,200.00 | Policy-Compliant
  ✅  TXN-006    | $ 18,750.00 | Policy-Compliant
  ✅  TXN-007    | $  8,900.00 | Policy-Compliant
  ✅  TXN-008    | $  1,100.00 | Policy-Compliant
  ✅  TXN-009    | $ 45,000.00 | Policy-Compliant
  ✅  TXN-010    | $ 32,000.00 | Policy-Compliant
  ✅  TXN-011    | $  1,850.00 | Policy-Compliant
  ✅  TXN-012    | $    750.00 | Policy-Compliant
  ✅  TXN-013    | $  3,400.00 | Policy-Compliant
  ✅  TXN-014    | $  6,200.00 | Policy-Compliant
  ✅  TXN-015    | $    920.00 | Policy-Compliant

[INFO]  Saved hybrid audit → /Users/khalidarfan/projects/Ai Bootcamps/01_data_pipeline_automation/flagged_expenses.csv
```

**Integration and Proof of Work**
=====================================

The Sovereign Audit Pipeline is designed to be an operational implementation, meaning that once the pipeline is set up and running, it will generate reports and insights automatically. Below is your target output:

```text
════════════════════════════════════════════════════════════
  PHASE 1 — Deterministic Rules
════════════════════════════════════════════════════════════
[INFO]  Loading  → /Users/khalidarfan/projects/Ai Bootcamps/01_data_pipeline_automation/data/corporate_expenses.csv
[INFO]  Validated 15 rows | Rejected 0 invalid rows
[INFO]  Threshold flag: 4 rows > $10,000.00

════════════════════════════════════════════════════════════
  PHASE 2 — Probabilistic Intelligence  (llama3.2)
════════════════════════════════════════════════════════════
[LLM]   Running llama3.2 categorisation on 15 rows...
  ✅  TXN-001    | $    499.00 | Policy-Compliant
  ⚠️  TXN-002    | $  3,200.00 | Needs Review
  ✅  TXN-003    | $ 12,500.00 | Policy-Compliant
  ✅  TXN-004    | $    980.00 | Policy-Compliant
  ✅  TXN-005    | $  2,200.00 | Policy-Compliant
  ✅  TXN-006    | $ 18,750.00 | Policy-Compliant
  ✅  TXN-007    | $  8,900.00 | Policy-Compliant
  ✅  TXN-008    | $  1,100.00 | Policy-Compliant
  ✅  TXN-009    | $ 45,000.00 | Policy-Compliant
  ✅  TXN-010    | $ 32,000.00 | Policy-Compliant
  ✅  TXN-011    | $  1,850.00 | Policy-Compliant
  ✅  TXN-012    | $    750.00 | Policy-Compliant
  ✅  TXN-013    | $  3,400.00 | Policy-Compliant
  ✅  TXN-014    | $  6,200.00 | Policy-Compliant
  ✅  TXN-015    | $    920.00 | Policy-Compliant

[INFO]  Saved hybrid audit → /Users/khalidarfan/projects/Ai Bootcamps/01_data_pipeline_automation/flagged_expenses.csv
```