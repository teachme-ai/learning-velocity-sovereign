# AI for Global Finance Industry Lab Manual: EdTech - Base Track: Multi-Agent Swarm (No-Code)

## Introduction
Welcome to the **Base Track** for EdTech, a set of no-code templates designed for building scalable and efficient AI workflows in the field of global finance. This module focuses on constructing a simple workflow with three parallel or sequential AI Agent nodes: **Analyst**, **Auditor**, and **Reporter**.

## Goal
Construct an n8n workflow with three parallel or sequential AI Agent nodes: **Analyst**, **Auditor**, and **Reporter**.

## Step-by-Step Guide
1. **The Trigger**: Add a Webhook Trigger node (to accept queries).
2. **The Analyst Node**: An AI Agent node prompted to analyze EdTech trends using publicly available datasets.
3. **The Auditor Node**: An AI Agent node prompting the Analyst Node to verify compliance and detect potential hallucinations in the data.
4. **The Reporter Node**: An AI Agent node that synthesizes the output into a markdown report highlighting key findings and recommendations.
5. **The Response**: Send a Webhook Response back to the user.

*An n8n template `workflow_session_03.json` is provided in this directory.*

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window