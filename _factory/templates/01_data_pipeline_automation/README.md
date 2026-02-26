# Session 01: Data Pipeline Automation

## Overview

This session focuses on the **Sovereign Data Pipeline**. We move from manual spreadsheet cleaning to automated, reproducible scoring using AI.

## Learning Outcomes
- [ ] Upload and interrogate structured data using Google AI Studio
- [ ] Build a Pydantic-validated data cleaner in Python
- [ ] Integrate a local Ollama model for policy compliance categorisation
- [ ] Generate a structured audit report from local model outputs

## [INTEGRATOR] Lab: The Google AI Studio Flow

**Step 1:** Upload the `corporate_expenses.csv` to Google AI Studio.

**Step 2:** Use the **Gemini 2.0 Flash** model with a System Instruction:
> *"Identify transactions that violate a $1,000 limit for non-travel expenses."*

**Step 3:** Request the output as a **JSON list** of flagged IDs with a reason for each flag.

## [ARCHITECT] Lab: The OpenCode & Ollama Pipeline

**Step 1:** Use **OpenCode** to generate a Python script `logic/cleaner.py` using **Pydantic** to enforce a schema on the CSV.

**Step 2:** Integrate a local call to **Ollama** (`llama3.2:8b`) to categorise the `description` field into one of:
- `Policy-Compliant`
- `Suspicious`
- `Needs Review`

**Step 3:** Generate a summary report `data/audit_summary.md` using the local model results.

## Governance Notes
<!-- Compliance, security, and enterprise governance considerations. -->
