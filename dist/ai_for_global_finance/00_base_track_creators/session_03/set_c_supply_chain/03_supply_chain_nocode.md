# Introduction
Welcome to the AI for Global Finance Industry: Supply Chain Module. This module will guide you through constructing an N8N workflow using three parallel or sequential AI Agent nodes for a Supply Chain scenario.

## Goal
Construct an N8N workflow with three parallel or sequential AI Agent nodes: **Analyst**, **Auditor**, and **Reporter**.

## Step-by-Step Guide
1. **The Trigger**: Add a Webhook Trigger node (to accept queries).
2. **The Analyst Node**: An AI Agent node prompted to analyze Supply Chain trends.
3. **The Auditor Node**: An AI Agent node prompted to verify compliance and catch hallucinations.
4. **The Reporter Node**: An AI Agent node that synthesizes the output into a markdown report.
5. **The Response**: Send a Webhook Response back to the user.

*An N8N template `workflow_session_03.json` is provided in this directory.*

---
# Business Value
**Business Value**

This module has the following business value:

* **Improved Supply Chain Visibility**: The Analyst node provides real-time insights into supply chain trends, enabling better decision-making.
* **Enhanced Compliance Compliance**: The Auditor node ensures that compliance regulations are met, reducing the risk of non-compliance and associated costs.
* **Increased Efficiency**: The Reporter node automates the report generation process, saving time for users and enhancing overall efficiency.