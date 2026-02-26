# EdTech (Set D) — Base Track: Multi-Agent Swarm (No-Code)

Welcome to the **Base Track** for EdTech. We will build a "Visual Swarm" using individual AI Agent nodes in n8n.

## Goal
Construct an n8n workflow with three parallel or sequential AI Agent nodes: **Analyst**, **Auditor**, and **Reporter**.

## Step-by-Step Guide
1. **The Trigger**: Add a Webhook Trigger node (to accept queries).
2. **The Analyst Node**: An AI Agent node prompted to analyze EdTech trends.
3. **The Auditor Node**: An AI Agent node prompted to verify compliance and catch hallucinations.
4. **The Reporter Node**: An AI Agent node that synthesizes the output into a markdown report.
5. **The Response**: Send a Webhook Response back to the user.

*An n8n template `workflow_session_03.json` is provided in this directory.*

---
**[Back to Curriculum Hub](../../../README.md)**
