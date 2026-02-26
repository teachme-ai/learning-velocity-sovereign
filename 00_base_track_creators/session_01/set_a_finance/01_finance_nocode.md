# Finance (Set A) — Base Track: Data Pipeline (No-Code)

Welcome to the **Base Track** for Finance. Here we orchestrate the data cleaning pipeline using visual node-based workflows.

## Goal
Build an **n8n** workflow that ingests `finance_dirty_data.csv` (or Google Sheets) and uses a **Google AI Studio (Gemini)** node to clean and structure it.

## Step-by-Step Guide
1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas.
2. **The Scrubber**: Add a **Google AI Studio** node. Configure it to use the `gemini-1.5-pro` model.
   - **System Prompt**: "You are a Finance data analyst. Parse this messy row and output clean JSON."
3. **The Output**: Add a **Google Sheets** (or Write File) node to save the cleaned data.

*An n8n template `workflow_session_01.json` is provided in this directory to import directly into your instance.*

---
**[Back to Curriculum Hub](../../../README.md)**
