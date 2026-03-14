**Introduction**
===============

Welcome to the **Base Track** for EdTech, specifically tailored for an **n8n** workflow that ingests `edtech_dirty_data.csv` (or Google Sheets) and uses a **Google AI Studio (Gemini)** node to clean and structure it. In this lab manual, we will outline the steps necessary to create an efficient data pipeline in no-code.

## Goal
---------------

* Build an n8n workflow that ingests `edtech_dirty_data.csv` or Google Sheets and cleans and structures it using a **Google AI Studio (Gemini)** node.
* Define the specific business value of this project, including its potential impact on financial institutions and organizations in the AI for Global Finance industry.

## Step-by-Step Guide
-------------------------

### Step 1: Trigger
--------------

Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas. This trigger will initiate the workflow when new data is added to the specified file.

### Step 2: Scrubber
--------------

Add a **Google AI Studio** node, configured to use the `gemini-1.5-pro` model. Configure this node according to your needs:

* System Prompt: "You are an EdTech data analyst. Parse this messy row and output clean JSON."

### Step 3: Output
-------------

Add a **Google Sheets** (or Write File) node to save the cleaned data.

Note:
An n8n template `workflow_session_01.json` is provided in this directory to import directly into your instance. This template will guide you through the setup process and ensure consistency across all instances.

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window