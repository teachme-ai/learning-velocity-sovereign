# Sustainability & ESG EdTech Base Track: One-Page Dashboard

## Introduction
Welcome to the **Base Track** for Sustainability & ESG EdTech. We will build a comprehensive, no-code React dashboard that connects to our n8n swarm, enabling users to generate sleek and interactive reports on sustainability performance.

## Goal
Use Lovable (or v0/Cursor) to create an enterprise-grade one-page React dashboard with real-time data visualization capabilities for Sustainability & ESG professionals. The dashboard will integrate seamlessly with our Session 03 n8n Webhook, facilitating timely and informed decision-making.

## Step-by-Step Guide

1. Log into Lovable.dev and create a new project.
2. **Prompt**: "Build a comprehensive, no-code React dashboard for Sustainability & ESG. It needs a text input for a query, a submit button, and a markdown-rendered response area. Wire the submit button to POST to `http://localhost:5678/webhook/swarm`."
3. **n8n Link**: Ensure your Session 03 n8n Visual Swarm workflow has an active Webhook node listening on that URL.

*An n8n template `workflow_session_05.json` (just the webhook receiver) is provided.*

---
### Sustainability Dashboard

*   Real-time data visualization of key sustainability metrics, such as greenhouse gas emissions and renewable energy usage.
*   Customizable dashboard design to accommodate specific user needs and reporting requirements.
*   Integration with relevant ESG data sources, enabling accurate and up-to-date insights.

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window