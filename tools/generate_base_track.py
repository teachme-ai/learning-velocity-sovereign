import os

domains = {
    "finance": ("Finance", "Finance (Set A)"),
    "healthcare": ("Healthcare", "Healthcare (Set B)"),
    "supply_chain": ("Supply Chain", "Supply Chain (Set C)"),
    "edtech": ("EdTech", "EdTech (Set D)"),
    "legal": ("Legal", "Legal (Set E)")
}

session_1_template = """# {domain_label} — Base Track: Data Pipeline (No-Code)

Welcome to the **Base Track** for {domain_name}. Instead of writing Python scripts, we will orchestrate the data cleaning pipeline using visual node-based workflows.

## Goal
Build an **n8n** workflow that ingests our raw `{domain_key}_dirty_data.csv` and uses a **Google AI Studio** node to clean and structure it.

## Prerequisites
- Local or Cloud n8n instance running.
- Google Gemini API Key.

## Step-by-Step Guide

### 1. The Trigger
- Add a **Manual Trigger** node or a **Read File** node to your n8n canvas.
- Load the raw `.csv` file containing the unscrubbed {domain_name} logs.

### 2. The AI Transformation
- Add a **Google AI Studio** (or generic LLM/HTTP request) node.
- Configure it to use the `gemini-1.5-pro` or `gemini-1.5-flash` model.
- **System Prompt**: "You are an expert {domain_name} data analyst. Parse the following messy CSV rows and output clean, structured JSON containing the essential fields (e.g., dates, amounts, risk flags)."
- Connect the output of the file reader to the input of the AI node.

### 3. The Output
- Add a **Write File** node (or Spreadsheet node) to save the parsed JSON/CSV.
- Name the output file `{domain_key}_clean_data.csv`.

Once the flow executes successfully, you have constructed a local AI data pipeline—without writing a single line of code!

---
**[Back to Curriculum Hub](../../README.md)**
"""

session_2_template = """# {domain_label} — Base Track: Narrative Engine (No-Code)

Welcome to the **Base Track** for {domain_name}. We will use cutting-edge sovereign reasoning tools to transform our clean data into an Executive Narrative.

## Goal
Upload the cleaned data from Session 01 into **NotebookLM** to autonomously generate a Project Brief and a synthesized Audio Overview (Podcast).

## Prerequisites
- Access to NotebookLM (Google).
- The structurally sound `{domain_key}_clean_data.csv` from Session 01.

## Step-by-Step Guide

### 1. Create the Notebook
- Open NotebookLM and create a new notebook titled **"{domain_name} Executive Narrative"**.

### 2. Ingest the Source Data
- Click **Add Source** and upload your `{domain_key}_clean_data.csv`.
- NotebookLM will immediately begin citing and grounding itself on your specific vertical data.

### 3. Generate the Project Brief
- In the Notebook Guide layout, click on **"Project Brief"** or **"Executive Summary"**.
- The AI will read the structured data and output a comprehensive text memo highlighting the core anomalies, risks, or key metrics.

### 4. Generate the Audio Overview
- Open the **Audio Overview** panel in the top right.
- Click **"Generate"**. NotebookLM will synthesize a two-host podcast deep-diving into the insights hidden within your {domain_name} data.

This represents the 'Executive Narrative' tier constructed entirely via No-Code interfaces.

---
**[Back to Curriculum Hub](../../README.md)**
"""

for i in range(1, 6):
    os.makedirs(f"00_base_track_creators/session_{i:02d}", exist_ok=True)

for key, (name, label) in domains.items():
    with open(f"00_base_track_creators/session_01/{key}_base_pipeline.md", "w") as f:
        f.write(session_1_template.format(domain_name=name, domain_label=label, domain_key=key))
    with open(f"00_base_track_creators/session_02/{key}_base_narrative.md", "w") as f:
        f.write(session_2_template.format(domain_name=name, domain_label=label, domain_key=key))

print("Created Base Track directories and 10 markdown guides.")
