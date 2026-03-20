# Session 01: Data Pipeline Automation

## Overview
In this session, we'll dive into the Sovereign Data Pipeline, a critical component of AI for Cyber-Security that automates data preparation and validation. By moving away from manual spreadsheet cleaning, we can focus on what matters most - detecting and responding to threats in real-time.

Think of it like setting up an Incident Response playbook: you can't just wing it when an attack hits; you need a structured process to contain, eradicate, and recover. Similarly, our data pipeline needs to be efficient, scalable, and reliable to support our threat detection and response efforts.

We'll explore how the Sovereign Data Pipeline integrates with popular AI frameworks like TensorFlow, PyTorch, and Scikit-learn to automate tasks such as data preprocessing, feature engineering, and model training. By leveraging these technologies, we can create a repeatable, auditable process for scoring sensitive data - a crucial step in identifying potential security threats.
## Learning Outcomes
- [ ] Upload and interrogate structured data using Google AI Studio
- [ ] Build a Pydantic-validated data cleaner in Python
- [ ] Integrate a local Ollama model for policy compliance categorisation
- [ ] Generate a structured audit report from local model outputs

## [BUILDER] Lab: The Google AI Studio Flow

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