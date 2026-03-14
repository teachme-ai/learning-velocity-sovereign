**Introduction**

Welcome to the **Base Track** for AI for Global Finance, focusing on building an N8N workflow that ingests `ai_for_global_finance_dirty_data.csv` (or Google Sheets) and utilizes a Google AI Studio (Gemini) node to clean and structure it.

## Goal
Build an n8n workflow that processes the provided data pipeline using visual node-based workflows.

## Step-by-Step Guide
1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas.
2. **The Scrubber**: Connect the Google AI Studio (Gemini) node, specifying the `gemini-1.5-pro` model for data cleaning and structure.
   - **System Prompt**: "As an expert in Global Finance, you receive a dataset containing messy financial records. Clean and format it according to our requirements."
3. **The Output**: Create a Google Sheets (or Write File) node to save the cleaned data.

*An n8n template `workflow_session_01.json` is provided in this directory to import directly into your instance.*

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window