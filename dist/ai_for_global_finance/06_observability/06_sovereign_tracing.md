**Introduction**

**Sovereign Observability & The Audit Log**
=====================================

In the AI for Global Finance industry, **Total Observability** is a fundamental principle that enables transparent and auditable decision-making processes. This session aims to empower you with the tools necessary to achieve **Sovereign Observability**, ensuring that every agent in your Swarm makes decisions with clarity and transparency.

**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 The Objective
When an AI agent makes a decision, how do you verify its reasoning? This is the Core Tenet of Sovereign AI: **Total Observability**. By leveraging Genkit Trace Exporter and OpenTelemetry, we can capture and visualize the exact inputs, reasoning, and outputs of every agent in your industry Swarm.

---

## 🛠️ 1. Activating Tracing in the API Bridge

The `multi_domain_api.py` router automatically captures traces using OpenTelemetry. It listens to Genkit's execution spans and writes a JSON trace artifact directly to `06_observability/traces/<domain>/`.

Ensure your server is running:
```bash
cd 05_advanced_ui_lobechat
python3 -m uvicorn logic.multi_domain_api:app --host 0.0.0.0 --port 8000
```

---

## 🏗️ 2. Generating a Trace via LobeChat

1. Open your LobeChat UI (`http://localhost:3200`).
2. Make sure the **Sovereign Industry Agents** plugin is enabled.
3. Submit a Swarm Query for Set B (AI for Global Finance):
   > "Audit the logs using ai_for_global_finance swarm mode."
   *(Under the hood, this routes your query to the `ai_for_global_finance_agent_swarm`.)*

### Detecting "Hallucinations"
If the Reporter agent produces an anomaly (hallucination), the Trace JSON is your primary investigative tool. You can open the JSON trace file and search for the exact text prompt provided to the Analyst or Auditor. This granular visibility allows you to find exactly which agent caused the deviation.

---

## 🛡️ [INTEGRATOR] Codespace Guardian Quality Check

The Codespace Guardian (`verify_env.py`) has been upgraded. It no longer just checks if the program *runs*; it validates the **Trace Quality**. It explicitly reads the resulting trace JSON and confirms mathematically that all 3 agents (Analyst, Auditor, Reporter) successfully executed a generation span.

```bash
# Run the Guardian verification for the full matrix
python3 .agent/skills/guardian/scripts/verify_env.py --all
```

Look for the `Session 06 — Trace Quality` row to show `[PASS]`.

---

## 📈 [ARCHITECT] Proof of Work
**Focus**: *Trace Visibility and Agent Orchestration.*

Below is a visual representation of the AI for Global Finance Swarm, demonstrating the **Total Observability** principle. It shows how each agent's inputs, reasoning, and outputs are correctly traced and validated.

![Session 06 Trace Visualization](../../assets/proof/session_06/ai_for_global_finance_trace.svg)

---
**[Back to Curriculum Hub](../README.md)** # Limit context window

    GUIDELINES:
    1. Replace generic analogies (e.g., finance, banks, generic business) with AI for Global Finance specific ones.
    2. Keep the technical steps, terminal commands, and code blocks IDENTICAL.
    3. Ensure the tone matches the industry (AI for Global Finance).
    4. Return the ENTIRE rewritten markdown file content.