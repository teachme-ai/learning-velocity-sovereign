# Session 01: Healthcare Data Pipeline

## [INTEGRATOR] Track

### Overview
This pipeline automated the generation and anonymization of standard healthcare CSV forms. It cleans the data format to ensure compliance.

### Execution
Run the scrubber logic to see the automated PII removal:
```bash
python3 01_data_pipeline_automation/set_b_healthcare/logic/scrubber.py
```

## [ARCHITECT] Track

### Validation Pipeline
The backend process verifies cost legitimacy and ICD-10 formatting matches `[A-Z][0-9]{2}` structure while anonymizing sensitive string representations.

### Validation Output
Scrubbing complete.
Total rows processed: 50
PII Anonymized: 23 rows
Rows with Validation Flags: 7
Cleaned output saved to /tmp/healthcare_output/scrubbed_billing.csv---

# [VALIDATE]
python3 01_data_pipeline_automation/set_b_healthcare/logic/scrubber.py
# Check that the file was processed, flags correctly added, and output generated.
