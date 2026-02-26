# Introduction
Welcome to the **Base Track** for Sustainability and Environmental, Social, and Governance (ESG) in Supply Chain. Here we orchestrate the data cleaning pipeline using visual node-based workflows tailored to the sustainability industry.

## Goal
Build an n8n workflow that ingests `supply_chain_dirty_data.csv` (or Google Sheets) and uses a **Google AI Studio** node to clean and structure it, with a focus on reducing operational emissions while promoting stakeholder transparency.

## Step-by-Step Guide
1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas.
2. **The Scrubber**: Add a **Google AI Studio** node. Configure it to use the `gemini-1.5-pro` model, specifically designed for ESG-related data analysis tasks.
   - **System Prompt**: "You are an ESG analyst responsible for optimizing supply chain operations while mitigating negative environmental and social impacts."
3. **The Output**: Add a **Google Sheets** (or Write File) node to save the cleaned data, ensuring compliance with industry regulations such as GDPR.

*An n8n template `workflow_session_01.json` is provided in this directory to import directly into your instance.*

---
# Limit context window
### GUIDELINES:
1. Replace generic analogies with Sustainability & ESG specific ones.
2. Keep the technical steps, terminal commands, and code blocks IDENTICAL.
3. Ensure the tone matches the industry (Sustainability & ESG).
4. Return the ENTIRE rewritten markdown file content.