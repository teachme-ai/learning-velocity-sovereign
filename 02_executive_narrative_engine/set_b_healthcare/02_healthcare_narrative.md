# Session 02: Healthcare Narrative Engine

## [INTEGRATOR] Track

### Overview
This stage automates the translation of structured data issues (PII and formatting errors) into a professional compliance report for Hospital Administrators.

### Execution
Run the compliance generation proxy to interface with the local LLM:
```bash
python3 02_executive_narrative_engine/set_b_healthcare/logic/compliance_gen.py
```

## [ARCHITECT] Track

### Validation Pipeline
The backend process verifies the interaction between the data pipeline and local Ollama (`llama3.2:1b`), successfully proxying structured statistics into an executive summary markdown document.

### Validation Output
Sending data proxy to Local Ollama model (llama3.2:1b)...
Compliance Report successfully generated and saved to: /tmp/healthcare_output/compliance_report.md---

# [VALIDATE]
python3 02_executive_narrative_engine/set_b_healthcare/logic/compliance_gen.py
# Verify proxy connects and report generated successfully.

---
**[Back to Curriculum Hub](../../README.md) | [Previous Lab: Session 01](../../01_data_pipeline_automation/set_b_healthcare/01_healthcare_pipeline.md) | [Next Lab: Session 03](../../03_multi_agent_systems/set_b_healthcare/03_healthcare_swarm.md)**
