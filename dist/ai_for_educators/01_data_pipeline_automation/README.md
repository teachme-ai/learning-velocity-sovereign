**Introduction**

In today's data-driven world, educators and researchers face complex tasks that require high-quality data. One such task is automating the process of cleaning, validating, and analyzing structured data. This session focuses on creating a **Sovereign Data Pipeline**, leveraging Artificial Intelligence (AI) to move from manual spreadsheet cleaning to automated, reproducible scoring.

**Learning Outcomes**

- [ ] Utilize Google AI Studio to upload and interrogate structured data.
- [ ] Build a Pydantic-validated data cleaner in Python using the `datacleaner` library.
- [ ] Integrate a local Ollama model for policy compliance categorization using the `ollama` library.
- [ ] Generate a structured audit report from local model outputs, leveraging the insights gained.

## Integrator: Flow for Automated Data Pipelines

**Step 1:** Upload data to Google AI Studio.

**Step 2:** Define a custom **Gemini 2.0 Flash** model with a **System Instruction**: *"Identify transactions that violate a $1,000 limit for non-travel expenses."*

## Architect: OpenCode & Ollama Pipeline

**Step 1:** Create a Python script `logic/cleaner.py` using Pydantic to enforce a schema on the CSV.

**Step 2:** Integrate the local Ollama model (`llama3.2:8b`) for policy compliance categorization of the `description` field.

**Step 3:** Generate a summary report `data/audit_summary.md` using the local model results.

## Governance Notes

<!-- Compliance, security, and enterprise governance considerations. -->

1. Replace generic analogies (e.g., finance, banks, generic business) with AI for Educators specific ones.
2. Keep the technical steps, terminal commands, and code blocks IDENTICAL.
3. Ensure the tone matches the industry (AI for Educators).
4. Return the ENTIRE rewritten markdown file content.
5. Start immediately with the markdown content. No conversational filler.