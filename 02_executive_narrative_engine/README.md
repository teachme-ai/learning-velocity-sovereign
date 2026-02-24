# Session 02: Executive Narrative Engine

## Overview
<!-- One-paragraph summary of what this session covers. -->

## Learning Outcomes
- [ ] LO1: Identify systemic patterns in flagged data.
- [ ] LO2: Automate executive-level narrative synthesis.
- [ ] LO3: Design "Human-in-the-loop" review protocols.

## [INTEGRATOR] Lab: Rapid Knowledge Digestion with NotebookLM

**Objective:** Transform raw flagged data into an audio briefing and a structured study guide — no coding required.

**Step 1: Upload your sources to NotebookLM**
- Go to [notebooklm.google.com](https://notebooklm.google.com) and create a new Notebook titled `Session 02 — Audit Analysis`.
- Upload both source files:
  - `01_data_pipeline_automation/data/flagged_expenses.csv`
  - `assets/data/corporate_expense_policy.pdf`
- Wait for NotebookLM to index both documents.

**Step 2: Generate a Deep Dive Audio Briefing**
- In the **Notebook Guide** panel, click **"Audio Overview"** → **"Generate"**.
- NotebookLM will produce a conversational Deep Dive summarising the primary policy violations found in the flagged transactions.
- Download the audio file and save it to `02_executive_narrative_engine/assets/audio_briefing.mp3`.

**Step 3: Create a Study Guide**
- In the same Notebook, click **"Study Guide"** → **"Generate"**.
- Prompt NotebookLM with: *"Which department appears to have the most policy violations, and what training would address this?"*
- Export the Study Guide and save it to `02_executive_narrative_engine/prompts/study_guide.md`.


## [ARCHITECT] Lab
<!-- Design & internals tasks for architecture-focused learners. -->

## Governance Notes
<!-- Compliance, security, and enterprise governance considerations. -->
