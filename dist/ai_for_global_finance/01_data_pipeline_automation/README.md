## Session 01: Data Pipeline Automation - Sovereign AI Solutions

### Overview
This session focuses on the **Sovereign Data Pipeline**, a comprehensive approach to automating data pipeline workflows critical for advanced cyber defense and threat intelligence. We leverage Artificial Intelligence (AI) and Machine Learning (ML) technologies to streamline manual processes in areas like SIEM correlation, incident enrichment, and proactive threat hunting, thereby ensuring the integrity, consistency, and accuracy of critical security telemetry.
### Learning Outcomes
- [ ] Develop a custom Pydantic validator in Python using AI Studio to automate data cleaning.
- [ ] Integrate a local Ollama model for policy compliance categorization, with automated output filtering and validation.
- [ ] Generate a structured audit report from local model outputs, ensuring compliance with regulatory requirements.

## [INTEGRATOR] Lab: The Sovereign Data Pipeline Flow

**Step 1:** Upload the `corporate_expenses.csv` to AI Studio using **Gemini 2.0 Flash**, a system instruction optimized for data quality and accuracy.

**Step 2:** Request the output as a **JSON list** of flagged IDs with a reason for each flag, ensuring compliance with regulatory requirements.

## [ARCHITECT] Lab: The OpenCode & Ollama Pipeline

**Step 1:** Develop a custom Pydantic validator in Python using AI Studio to enforce a schema on the CSV, ensuring data quality and consistency.

**Step 2:** Integrate a local call to **Ollama** (`llama3.2:8b`) to categorize the `description` field into one of:
- `Policy-Compliant`
- `Suspicious`
- `Needs Review`

**Step 3:** Generate a summary report `data/audit_summary.md` using the local model results, ensuring compliance with regulatory requirements.

## Governance Notes
<!-- Compliance, security, and enterprise governance considerations. --> # Limit context window