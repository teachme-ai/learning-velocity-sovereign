## Introduction to AI for Global Finance Data Pipeline Automation

In this session, we will focus on implementing a **Sovereign Data Pipeline** using advanced technologies and tools. This automation enables efficient data preparation, validation, and scoring of financial transactions, ultimately facilitating informed business decisions.

## Learning Outcomes
- [ ] Utilize Google AI Studio to upload structured data from CSV files.
- [ ] Develop a Pydantic-validated data cleaner in Python, capable of validating against corporate expense structures.
- [ ] Integrate a local Ollama model for policy compliance categorization using a System Instruction.
- [ ] Generate a structured audit report from the local model outputs.

## Integrator Lab: The Google AI Studio Flow

**Step 1:** Upload the `corporate_expenses.csv` to Google AI Studio, ensuring proper schema validation and data quality checks.

**Step 2:** Utilize the **Gemini 2.0 Flash** model with a System Instruction:
> *"Identify transactions that violate a $1,000 limit for non-travel expenses."*

## Architect Lab: The OpenCode & Ollama Pipeline

**Step 1:** Develop a Python script `logic/cleaner.py` using Pydantic to enforce a schema on the CSV data, ensuring compliance with corporate expense structures.

**Step 2:** Integrate a local call to **Ollama** (`llama3.2:8b`) to categorize the `description` field into one of:
- `Policy-Compliant`
- `Suspicious`
- `Needs Review`

## Governance Notes
<!-- Compliance, security, and enterprise governance considerations. --> 

### Limitations

- This automation should be adapted for real-world use cases, which may involve varying dataset structures, regulatory requirements, and business context.
- Ensure adherence to all relevant industry guidelines, regulations, and standards when implementing in production environments.

### Additional Guidance

For further details on these topics, please refer to the attached resources:

* Google AI Studio documentation
* Pydantic library documentation
* Ollama documentation