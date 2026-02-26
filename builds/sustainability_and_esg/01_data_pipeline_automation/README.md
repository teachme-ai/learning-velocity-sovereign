**Introduction**

In today's rapidly evolving business landscape, companies are under increasing pressure to demonstrate their commitment to sustainability and environmental, social, and governance (ESG) practices. As a key enabler of sustainable decision-making, data-driven strategies have become indispensable for businesses seeking to meet these expectations. This session delves into the world of **Sovereign Data Pipeline**, focusing on the integration of artificial intelligence (AI) and machine learning (ML) technologies to automate data pipeline automation.

**Learning Outcomes**

- [ ] Integrate Google AI Studio with Pydantic to create a structured data cleaner.
- [ ] Develop a local Ollama model for policy compliance categorization using Llama 3.2:8b.
- [ ] Generate a JSON list of flagged IDs with a reason for each flag from the Gemini 2.0 Flash model.

## [INTEGRATOR] Lab: The Google AI Studio Flow

**Step 1:** Upload the `corporate_expenses.csv` to Google AI Studio and create a new pipeline.

**Step 2:** Use the **Gemini 2.0 Flash** model with a System Instruction:
> *"Identify transactions that violate a $1,000 limit for non-travel expenses."* and request the output as a JSON list of flagged IDs with a reason for each flag.

## [ARCHITECT] Lab: The OpenCode & Ollama Pipeline

**Step 1:** Use **OpenCode** to generate a Python script `logic/cleaner.py` using Pydantic to enforce a schema on the CSV.

**Step 2:** Integrate a local call to **Ollama** (`llama3.2:8b`) to categorize the `description` field into one of:
- `Policy-Compliant`
- `Suspicious`
- `Needs Review`

**Step 3:** Generate a summary report `data/audit_summary.md` using the local model results.

## Governance Notes
<!-- Compliance, security, and enterprise governance considerations. --> # Limit context window