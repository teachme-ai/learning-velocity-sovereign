# Session 06 — Base Track: Sovereign Observability (No-Code)

Welcome to the **Base Track** for Session 06. So far, you've built pipelines, generated narratives, orchestrated swarms, and hooked up bespoke dashboards. But how do we know our AI isn't misbehaving? We need an audit trail. We need the **Flight Recorder**.

## Goal
Learn how to track, audit, and debug AI executions without writing code by leveraging the built-in observability features of [n8n](https://n8n.io).

## Step-by-Step Guide
1. **Trigger your Workflow**: Go to your Lovable dashboard (from Session 05) or use a direct webhook call to trigger your n8n Visual Swarm from Session 03.
2. **Open Execution History**: Navigate to your n8n dashboard and click on the "Executions" tab on the left sidebar for your swarm workflow.
3. **Trace the Path**: Click on the most recent "Success" execution. You will see a structural trace of exactly which nodes were activated, how long they took, and the raw JSON data that flowed between them.
4. **Audit the AI Prompt**: Click into the specific AI Agent node (e.g., the Auditor). Switch to the "Input" and "Output" tabs to see exactly what instructions the LLM used and the direct strings it outputted.
5. **Binary Data (Optional)**: If you are processing documents, you can click on any node that reads files to inspect the binary data stream and confirm that the OCR/parsing worked correctly at that specific point in the chain.

By mastering Execution History, you have a completely transparent, sovereign audit trail of exactly what your agentic swarm is deciding.

---
**[Back to Curriculum Hub](../../README.md)**
