# Session 01: EdTech Data Pipeline

## [INTEGRATOR] Track

### Overview
This stage aggregates fabricated student velocity logs and scrubs out impossible or irregular values (e.g., negative time entries and scores over 100).

### Execution
Run the cleaner script against the raw logs:
```bash
python3 01_data_pipeline_automation/set_d_edtech/logic/velocity_cleaner.py
```

## [ARCHITECT] Track

### Validation Pipeline
The background logic successfully partitions `anomaly_flag` rows from standard progression metrics, writing the parsed results securely.

### Validation Output
EdTech Velocity Cleansing complete.
Total rows processed: 50
Rows with Anomalies Flagged: 7
Cleaned output saved to /tmp/edtech_output/cleaned_logs.csv---

# [VALIDATE]
python3 01_data_pipeline_automation/set_d_edtech/logic/velocity_cleaner.py
# Verify negative metrics are tagged and partitioned.

---
**[Back to Curriculum Hub](../../README.md) | ~~Previous Lab~~ | [Next Lab: Session 02](../../02_executive_narrative_engine/set_d_edtech/02_edtech_narrative.md)**
