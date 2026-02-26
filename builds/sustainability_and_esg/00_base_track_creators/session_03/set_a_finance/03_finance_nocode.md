# Sustainability & ESG (Set A) — Base Track: Multi-Agent Swarm (No-Code)

## Introduction
In the realm of Sustainability and ESG, a complex interplay between various stakeholders requires effective collaboration and data-driven insights to drive decision-making. This no-code workflow in n8n enables three parallel AI Agent nodes to synergize their expertise: Analyst, Auditor, and Reporter.

## Goal
Construct an n8n workflow with three parallel or sequential AI Agent nodes: **Analyst**, **Auditor**, and **Reporter** for a comprehensive Sustainability & ESG solution.

## Step-by-Step Guide
1. **The Trigger**: Add a Webhook Trigger node (to accept queries).
2. **The Analyst Node**: An AI Agent node prompted to analyze Sustainability & ESG trends using relevant data sources.
3. **The Auditor Node**: An AI Agent node prompted to verify compliance and catch hallucinations in the analyzed data.
4. **The Reporter Node**: An AI Agent node that synthesizes the output into a markdown report, providing actionable recommendations for stakeholders.
5. **The Response**: Send a Webhook Response back to the user with the final assessment.

*An n8n template `workflow_session_03.json` is provided in this directory.*

---
### Limitations
This workflow assumes you have:
- An understanding of AI Agent nodes and their capabilities
- Access to relevant data sources for analysis (e.g., datasets, APIs)
- Familiarity with Webhook Triggers and n8n's configuration options

Please ensure you consult the official documentation before proceeding.