# Introduction

Welcome to the **Base Track** for Sustainability & ESG, specifically tailored for a 'One-Page Dashboard' web app that connects to our n8n swarm. This lab manual focuses on building a sleek React dashboard using Lovable (or v0/Cursor) as the tooling of choice.

## Goal
Use Lovable (or v0/Cursor) to generate a responsive, React-based front-end for a sustainability-focused dashboard. It should seamlessly integrate with our n8n swarm, enabling real-time data updates and streamlined decision-making processes.

## Step-by-Step Guide

1. Log into Lovable.dev and create a new project.
2. **Prompt**: "Build a single-page React dashboard for Sustainability & ESG. It needs an input field for a query, a submit button, and a markdown-rendered response area. Wire the submit button to POST to `http://localhost:5678/webhook/swarm`."
3. **n8n Link**: Ensure your Session 03 n8n Visual Swarm workflow has an active Webhook node listening on that URL.
*An n8n template `workflow_session_05.json` (just the webhook receiver) is provided.*

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window