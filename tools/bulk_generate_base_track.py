import os
import json

domains = {
    "finance": ("Finance", "Finance (Set A)"),
    "healthcare": ("Healthcare", "Healthcare (Set B)"),
    "supply_chain": ("Supply Chain", "Supply Chain (Set C)"),
    "edtech": ("EdTech", "EdTech (Set D)"),
    "legal": ("Legal", "Legal (Set E)")
}

# ── Templates ──

session_01_md = """# {domain_label} — Base Track: Data Pipeline (No-Code)

Welcome to the **Base Track** for {domain_name}. Here we orchestrate the data cleaning pipeline using visual node-based workflows.

## Goal
Build an **n8n** workflow that ingests `{domain_key}_dirty_data.csv` (or Google Sheets) and uses a **Google AI Studio (Gemini)** node to clean and structure it.

## Step-by-Step Guide
1. **The Trigger**: Add a Google Sheets Trigger or Manual Trigger node to your n8n canvas.
2. **The Scrubber**: Add a **Google AI Studio** node. Configure it to use the `gemini-1.5-pro` model.
   - **System Prompt**: "You are a {domain_name} data analyst. Parse this messy row and output clean JSON."
3. **The Output**: Add a **Google Sheets** (or Write File) node to save the cleaned data.

*An n8n template `workflow_session_01.json` is provided in this directory to import directly into your instance.*

---
**[Back to Curriculum Hub](../../../README.md)**
"""

session_02_md = """# {domain_label} — Base Track: Narrative Engine (No-Code)

Welcome to the **Base Track** for {domain_name}. We use sovereign reasoning tools to transform clean data into an Executive Narrative.

## Goal
Upload the scrubbed {domain_name} data from Session 01 into **NotebookLM** to autonomously generate a Project Brief and Audio Overview.

## Step-by-Step Guide
1. Open up **NotebookLM** and create a notebook titled "{domain_name} Industry Brief".
2. **Add Source**: Upload your cleaned structured CSV/Sheets data.
3. **Generate Brief**: Click "Project Brief" in the Notebook Guide.
4. **Generate Podcast**: Open the Audio Overview panel and click "Generate".

---
**[Back to Curriculum Hub](../../../README.md)**
"""

session_03_md = """# {domain_label} — Base Track: Multi-Agent Swarm (No-Code)

Welcome to the **Base Track** for {domain_name}. We will build a "Visual Swarm" using individual AI Agent nodes in n8n.

## Goal
Construct an n8n workflow with three parallel or sequential AI Agent nodes: **Analyst**, **Auditor**, and **Reporter**.

## Step-by-Step Guide
1. **The Trigger**: Add a Webhook Trigger node (to accept queries).
2. **The Analyst Node**: An AI Agent node prompted to analyze {domain_name} trends.
3. **The Auditor Node**: An AI Agent node prompted to verify compliance and catch hallucinations.
4. **The Reporter Node**: An AI Agent node that synthesizes the output into a markdown report.
5. **The Response**: Send a Webhook Response back to the user.

*An n8n template `workflow_session_03.json` is provided in this directory.*

---
**[Back to Curriculum Hub](../../../README.md)**
"""

session_04_md = """# {domain_label} — Base Track: Sovereign RAG (No-Code)

Welcome to the **Base Track** for {domain_name}. We will link continuous data folders to a knowledge base.

## Goal
Link Google Drive folders directly to **NotebookLM** for instant Domain RAG.

## Step-by-Step Guide
1. Create a dedicated Google Drive folder for {domain_name} policies, manuals, and datasets.
2. In NotebookLM, click **Add Source** -> **Google Drive**.
3. Select your designated folder. NotebookLM will now automatically sync and ground its answers based on the continually updated files within that folder.

---
**[Back to Curriculum Hub](../../../README.md)**
"""

session_05_md = """# {domain_label} — Base Track: Sovereign Cockpit (No-Code)

Welcome to the **Base Track** for {domain_name}. We will build a 'One-Page Dashboard' web app that connects to our n8n swarm.

## Goal
Use **Lovable** (or v0/Cursor) to generate a sleek React dashboard that talks to your Session 03 n8n Webhook.

## Step-by-Step Guide
1. Log into Lovable.dev and create a new project.
2. **Prompt**: "Build a single-page React dashboard for {domain_name}. It needs a text input for a query, a submit button, and a markdown-rendered response area. Wire the submit button to POST to `http://localhost:5678/webhook/swarm`."
3. **n8n Link**: Ensure your Session 03 n8n Visual Swarm workflow has an active Webhook node listening on that URL.

*An n8n template `workflow_session_05.json` (just the webhook receiver) is provided.*

---
**[Back to Curriculum Hub](../../../README.md)**
"""

n8n_template_json = {
  "nodes": [
    {
      "parameters": {},
      "id": "placeholder-id",
      "name": "Placeholder Base Track Node",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [ 250, 300 ]
    }
  ],
  "connections": {}
}

# ── Generation Loop ──

base_dir = "00_base_track_creators"

for session_idx, md_template in enumerate([session_01_md, session_02_md, session_03_md, session_04_md, session_05_md], start=1):
    session_str = f"session_{session_idx:02d}"
    
    for key, (name, label) in domains.items():
        domain_dir = os.path.join(base_dir, session_str, f"set_{chr(97 + list(domains.keys()).index(key))}_{key}")
        os.makedirs(domain_dir, exist_ok=True)
        
        # Write Markdown
        md_filename = f"{session_idx:02d}_{key}_nocode.md"
        with open(os.path.join(domain_dir, md_filename), "w") as f:
            f.write(md_template.format(domain_name=name, domain_label=label, domain_key=key))
            
        # Write JSON for 1, 3, 5
        if session_idx in [1, 3, 5]:
            json_filename = f"workflow_session_{session_idx:02d}.json"
            n8n_template_json["nodes"][0]["name"] = f"Session {session_idx:02d} {name} Node"
            with open(os.path.join(domain_dir, json_filename), "w") as f:
                json.dump(n8n_template_json, f, indent=2)

print("✅ Successfully generated 25 markdown guides and 15 JSON templates for Sessions 01-05.")
