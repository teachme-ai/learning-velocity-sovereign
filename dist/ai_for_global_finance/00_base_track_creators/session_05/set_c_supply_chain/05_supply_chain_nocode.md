# Introduction
Welcome to the Base Track for Supply Chain in AI for Global Finance. This lab manual will guide you through building a sleek React dashboard that interacts with your n8n swarm, leveraging Lovable (or v0/Cursor) to provide real-time insights into financial markets and trends.

## Goal
Use Lovable (or v0/Cursor) to generate a beautiful React dashboard that queries our Session 03 n8n Webhook, which will serve as the central hub for integrating AI-driven finance intelligence. This dashboard should respond with markdown-rendered output, giving users an immediate visual understanding of market data and analysis.

## Step-by-Step Guide
1. Log into Lovable.dev and create a new project.
2. **Prompt**: "Build a single-page React dashboard for Supply Chain that takes a financial query as input, processes it using n8n, and displays the result in markdown format."
3. **n8n Link**: Ensure your Session 03 n8n Visual Swarm workflow has an active Webhook node listening on `http://localhost:5678/webhook/swarm`. This will be our central hub for AI-driven finance intelligence.

*An n8n template `workflow_session_05.json` (just the webhook receiver) is provided.*

---
**[Back to Curriculum Hub](../../../README.md)** # Limit context window 

    GUIDELINES:
    1. Replace generic analogies (e.g., finance, banks, generic business) with AI for Global Finance specific ones.
    2. Keep the technical steps, terminal commands, and code blocks IDENTICAL.
    3. Ensure the tone matches the industry (AI for Global Finance).
    4. Return the ENTIRE rewritten markdown file content.
    5. Start immediately with the markdown content. No conversational filler.