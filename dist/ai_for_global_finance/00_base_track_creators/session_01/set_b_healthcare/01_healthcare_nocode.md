# AI for Global Finance (Set B) — Base Track: Data Pipeline (No-Code)

Welcome to the **Base Track** for AI for Global Finance. Here we orchestrate the data cleaning pipeline using visual node-based workflows.

## Goal
Build an **n8n workflow that ingests `ai_for_global_finance_dirty_data.csv` (or Google Sheets) and uses a **Google AI Studio (Gemini)** node to clean and structure it.

## Step-by-Step Guide
1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas.
2. **The Scrubber**: Add a **Google AI Studio** node. Configure it to use the `gemini-1.5-pro` model.
   - **System Prompt**: "Process this raw data from ai_for_global_finance_dirty_data.csv (or Google Sheets) for financial insights, providing cleaned and structured JSON output."
3. **The Output**: Add a **Google Sheets** (or Write File) node to save the cleaned data.

*An n8n template `workflow_session_01.json` is provided in this directory to import directly into your instance.*

---
# Limit context window

### Technical Guidelines:
1. Replace generic analogies (e.g., finance, banks, generic business) with AI for Global Finance specific ones.
2. Keep the technical steps, terminal commands, and code blocks IDENTICAL.
3. Ensure the tone matches the industry (AI for Global Finance).
4. Return the ENTIRE rewritten markdown file content.

### Business Value:
Building this workflow enables financial institutions to:

* **Improve Data Quality**: Automate data cleaning processes to reduce manual errors and ensure data consistency across platforms.
* **Enhance Analytical Capabilities**: Use AI-driven insights to inform strategic decisions, optimize operations, and increase revenue growth.
* **Reduce Costs**: Automate routine tasks, minimizing the need for human intervention and reducing labor costs.

By implementing this no-code pipeline, financial institutions can accelerate their journey to using AI for Global Finance.