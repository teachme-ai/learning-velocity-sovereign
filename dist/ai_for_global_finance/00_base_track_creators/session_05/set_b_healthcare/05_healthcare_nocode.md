# AI for Global Finance (Set B) — Base Track: Sovereign Cockpit (No-Code)

Welcome to the **Base Track** for AI for Global Finance. We will build a 'One-Page Dashboard' web app that connects to our n8n swarm.

## Goal
Use **Lovable** (or v0/Cursor) to generate a sleek React dashboard that talks to your Session 03 n8n Webhook, serving as the central hub for AI-driven financial analysis and insights.

## Step-by-Step Guide
1. Log into Lovable.dev and create a new project.
2. **Prompt**: "Build a single-page React dashboard for AI for Global Finance. It needs a text input for a query, a submit button, and a markdown-rendered response area. Wire the submit button to POST to `http://localhost:5678/webhook/swarm`."
3. **n8n Link**: Ensure your Session 03 n8n Visual Swarm workflow has an active Webhook node listening on that URL.

*An n8n template `workflow_session_05.json` (just the webhook receiver) is provided.*

---
# Limit context window

## AI for Global Finance Industry Application
This No-Code project leverages **Lovable** to build a data-driven interface connecting to our n8n swarm. The resulting dashboard provides real-time insights and analysis, empowering financial professionals to make informed decisions.

## Business Value
The following benefits arise from implementing this solution:
* 
  * Efficient Data Flow: Automate business logic by connecting to n8n Swarm.
  * Real-time Insights: Receive accurate data feed in response to user queries.
  * Scalable Architecture: Easily extend the dashboard as needed, supporting various use cases and workflows.