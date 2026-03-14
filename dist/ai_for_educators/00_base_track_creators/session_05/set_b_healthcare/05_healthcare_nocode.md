# AI for Educators (Set B) — Base Track: Sovereign Cockpit (No-Code)

Welcome to the **Base Track** for AI for Educators. We will build a 'One-Page Dashboard' web app that connects to our n8n swarm.

## Goal
Use **Lovable** (or v0/Cursor) to generate a sleek React dashboard that talks to your Session 03 n8n Webhook.

## Step-by-Step Guide

1. Log into Lovable.dev and create a new project.
2. Prompt: "Build a single-page React dashboard for AI for Educators, incorporating features such as user authentication, query input, and response rendering using markdown."
3. Ensure the following no-code components are integrated:
* A login button that POSTs to `http://localhost:5678/webhook/swarm` with user credentials
* A submit button that triggers a POST request to `http://localhost:5678/webhook/swarm` with a query string containing user input
* A markdown-rendered response area displaying the received query result

**n8n Link:** Ensure your Session 03 n8n Visual Swarm workflow has an active Webhook node listening on that URL.

An n8n template `workflow_session_05.json` (just the webhook receiver) is provided.

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window