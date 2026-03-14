# Introduction
Welcome to the AI for Educators Supply Chain course, focusing on building a Visual Swarm using individual AI Agent nodes in n8n. This course will guide you through constructing an automated workflow that analyzes and reports on supply chain trends.

## Goal
Construct an n8n workflow with three parallel or sequential AI Agent nodes: **Analyst**, **Auditor**, and **Reporter** to automate the supply chain process, providing insights into trends and potential issues.

## Step-by-Step Guide
1. **The Trigger**: Add a Webhook Trigger node (to accept queries) that sends data from an external API or a cloud-based platform.
2. **The Analyst Node**: An AI Agent node prompted to analyze Supply Chain trends using pre-trained models such as those based on natural language processing (NLP), computer vision, or predictive analytics techniques.
3. **The Auditor Node**: An AI Agent node prompted to verify compliance and catch hallucinations in the supply chain data by comparing it with industry standards or regulatory requirements.
4. **The Reporter Node**: An AI Agent node that synthesizes the output into a markdown report highlighting potential issues, trends, and recommendations for improvement.

*An n8n template `workflow_session_03.json` is provided in this directory.*

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window