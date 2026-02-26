import os
from pathlib import Path

DOMAINS = {
    "a_finance": "Finance",
    "b_healthcare": "Healthcare",
    "c_supply_chain": "Supply Chain",
    "d_edtech": "EdTech",
    "e_legal": "Legal"
}

SESSION_01_TEMPLATE = """# Lab 01: {domain} Data Pipeline (Base Track)
**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 The Objective
As a Base Track (No-Code) Creator, you will orchestrate a data cleaning pipeline without writing code. You will build an **n8n workflow** that ingests raw {domain} data (`dirty_data.csv`), processes it through a **Google AI Studio** node to extract and clean anomalies, and outputs a structured dataset.

---

## ⚙️ 1. Environment Setup

1. **Launch n8n**: Ensure your n8n instance is running.
2. **Obtain API Key**: Secure your Google Gemini API key from Google AI Studio.
3. **Locate Data**: Find your `dirty_data.csv` in the `{domain_key}` directory of the curriculum.

---

## 🛠️ 2. Step-by-Step Execution

### Phase A: Ingestion Node
1. Create a new n8n workflow.
2. Add a **Read/Write Files from Disk** node to read `dirty_data.csv`.
3. Add a **Spreadsheet File** node to parse the CSV into JSON items.

### Phase B: Intelligence Node (Google AI Studio)
1. Add the **Google Gemini** node.
2. Authenticate using your Google AI Studio API key.
3. Set the Operation to "Generate Text".
4. Provide the system prompt: 
   > "You are a {domain} data cleaner. Review the incoming JSON rows, fix formatting errors, identify anomalies, and return a clean JSON array."

### Phase C: Output Node
1. Add another **Spreadsheet File** node to convert the cleaned JSON back to CSV format.
2. Add a **Read/Write Files from Disk** node to save the output as `clean_data.csv`.

---

## 📈 [INTEGRATOR] Proof of Work
**Focus**: *Node Connections and Execution.*

To validate this step, provide a screenshot of the successful execution of your n8n workflow. All nodes should have green checkmarks indicating successful data flow.

---

## 🏗️ [ARCHITECT] Proof of Work
**Focus**: *LLM Config and Output Integrity.*

Provide a screenshot of the Google AI Studio node configuration, demonstrating the prompt and the exact output JSON payload confirming the {domain} data was accurately structured.
"""

SESSION_02_TEMPLATE = """# Lab 02: {domain} Executive Narrative (Base Track)
**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 The Objective
Data is only valuable when properly communicated. In this Base Track session, you will leverage **Google NotebookLM** to transform your cleaned {domain} dataset into compelling executive narratives: an 'Audio Overview' (Podcast) and a structured 'Project Brief'.

---

## ⚙️ 1. Environment Setup

1. **Access NotebookLM**: Navigate to [notebooklm.google.com](https://notebooklm.google.com).
2. **Create Notebook**: Create a new Notebook named `{domain} Executive Insights`.
3. **Gather Sources**: Have your `clean_data.csv` (from Session 01) ready to upload.

---

## 🛠️ 2. Step-by-Step Execution

### Phase A: Source Ingestion
1. **Upload Data**: Click 'Add Source' and upload `clean_data.csv`.
2. **Analyze**: Let NotebookLM digest the structured data. Verify it accurately recognizes the columns and key {domain} metrics.

### Phase B: The Project Brief
1. Below the source, click the **Project Brief** shortcut in the Notebook Guide.
2. Review the auto-generated brief. Ensure it highlights the primary risks, anomalies, and insights derived from your data.
3. Pin the brief to your notebook.

### Phase C: The Audio Overview (Podcast)
1. In the Notebook Guide panel, locate the **Audio Overview** section.
2. Click **Generate** to create an AI-hosted podcast discussing your {domain} data.
3. Listen to the overview—it provides an incredibly human-sounding, narrative synthesis of the data anomalies.

---

## 📈 [INTEGRATOR] Proof of Work
**Focus**: *Notebook setup and brief generation.*

Provide a screenshot of your NotebookLM interface showing the `clean_data.csv` successfully added as a source and the generated Project Brief pinned to your board.

---

## 🏗️ [ARCHITECT] Proof of Work
**Focus**: *Narrative Synthesis and Audio Processing.*

Download the generated Audio Overview (`.wav` or `.mp3`) and save it to your `assets/proof/session_02/` directory alongside the exported text of your Project Brief. 
"""

def generate():
    base = Path(__file__).parent

    for key, name in DOMAINS.items():
        # Session 01
        s01_dir = base / "session_01" / f"set_{key}"
        s01_dir.mkdir(parents=True, exist_ok=True)
        with open(s01_dir / f"01_{key.split('_', 1)[1]}_nocode.md", "w") as f:
            f.write(SESSION_01_TEMPLATE.format(domain=name, domain_key=f"set_{key}"))

        # Session 02
        s02_dir = base / "session_02" / f"set_{key}"
        s02_dir.mkdir(parents=True, exist_ok=True)
        with open(s02_dir / f"02_{key.split('_', 1)[1]}_nocode.md", "w") as f:
            f.write(SESSION_02_TEMPLATE.format(domain=name, domain_key=f"set_{key}"))

if __name__ == "__main__":
    generate()
    print("Base Track guides generated successfully.")
