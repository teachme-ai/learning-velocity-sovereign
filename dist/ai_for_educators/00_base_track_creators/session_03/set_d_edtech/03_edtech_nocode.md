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
# Technical Details

**Technical Components**

*   n8n: No-Code workflow automation platform
*   AI Agent nodes: Individual nodes for analyzing EdTech trends, verifying compliance, and reporting
*   Webhook Trigger node: Prompts users to submit queries
*   Markdown Reporter: Produces a report based on the output of the other nodes

**System Requirements**

*   n8n version 1.0 or later
*   AI Agent nodes installed and running in a suitable environment

## Business Value

The **Base Track** for EdTech introduces a novel approach to creating interactive, dynamic, and personalized educational content. By combining the power of AI with workflow automation, we can:

*   Enhance user engagement and participation in EdTech
*   Automate repetitive tasks and reduce manual effort
*   Create customized learning paths and recommendations based on individual needs

This base track provides a foundation for more advanced applications that leverage AI for Educators to analyze complex educational data, identify trends, and make informed decisions.