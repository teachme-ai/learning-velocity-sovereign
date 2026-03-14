# Introduction
Welcome to the Base Track for Legal: AI for Global Finance. This track focuses on building an n8n workflow that ingests and cleans data from legal sources, using Google AI Studio (Gemini) as a natural language processing (NLP) model.

## Goal
Build an **n8n** workflow that ingests `legal_dirty_data.csv` or Google Sheets containing legal documents and uses a **Google AI Studio (Gemini)** node to clean and structure it, providing accurate insights for the legal team.

## Step-by-Step Guide
1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas.
2. **The Scrubber**: Add a **Google AI Studio** node. Configure it to use the `gemini-1.5-pro` model, specifically designed for extracting relevant information from unstructured text data, such as legal documents.
   - **System Prompt**: "Analyze and extract key information from a large number of PDF or CSV files."
3. **The Output**: Add a **Google Sheets** (or Write File) node to save the cleaned data.

### n8n Template: `workflow_session_01.json`
```json
{
  "nodes": [
    {
      "name": "Trigger",
      "type": "googleSheets",
      "id": "trigger",
      "parameters": {
        "trigger": "legal_dirty_data.csv"
      }
    },
    {
      "name": "Scrubber",
      "type": "googleAiStudio",
      "id": "scrubber",
      "parameters": {
        "modelId": "gemini-1.5-pro",
        "prompt": "Analyze and extract key information from a large number of PDF or CSV files."
      }
    },
    {
      "name": "Output",
      "type": "googleSheets",
      "id": "output",
      "parameters": {
        "sheetId": "#A1:Z1000", // Start from row 1 and go up to column Z
        "dataFormat": "text"
      }
    }
  ]
}
```
---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window