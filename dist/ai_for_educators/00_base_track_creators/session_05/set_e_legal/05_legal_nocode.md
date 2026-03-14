# Introduction
Welcome to the Base Track for Legal, where we'll build a sleek React dashboard that connects to our n8n swarm.

## Goal
Use Lovable (or v0/Cursor) to generate a React-based One-Page Dashboard application that retrieves data from our Session 03 n8n Webhook and renders it in a markdown-formatted response area. The dashboard will have a text input for user queries, a submit button, and a rendered output area.

## Step-by-Step Guide
1. Log into Lovable.dev and create a new project.
2. **Prompt**: "Build a single-page React dashboard for Legal. It needs a text input for a query, a submit button, and a markdown-rendered response area. Wire the submit button to POST to `http://localhost:5678/webhook/swarm`."
3. **n8n Link**: Ensure your Session 03 n8n Visual Swarm workflow has an active Webhook node listening on that URL.
*An n8n template `workflow_session_05.json` (just the webhook receiver) is provided.*

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window