# Lab 05: Advanced UI — LobeChat Sovereign Interface
**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 The Objective
In this final capstone lab, we bring our enterprise AI architecture to life with a comprehensive User Interface. We will deploy **LobeChat**, configuring it as a fully sovereign, open-source AI playground that securely connects directly to our local Ollama models and our backend **Sovereign Agent API**.

This bridges the gap between terminal-based engineering and executive-friendly interactivity.

---

## ⚙️ 1. Environment Setup

Copy and paste this block to prepare your Dockerized LobeChat environment.
*Note: This step requires Docker Desktop to be running on your host system.*

```bash
# 1. Ensure the directory exists
mkdir -p 05_advanced_ui_lobechat
cd 05_advanced_ui_lobechat

# 2. View the Blueprint
cat docker-compose.yml
```

---

## 🛠️ 2. Start the API Bridge

Our Genkit backend agents (from Sessions 03 and 04) are exposed through a unified FastAPI router.

```bash
# Start the Sovereign API Bridge on Port 8000
python3 -m uvicorn logic.multi_domain_api:app --host 0.0.0.0 --port 8000
```

Verify your agents are listening:
```bash
curl -s http://localhost:8000/health | jq
```

---

## 🛠️ 3. Deploy LobeChat

Follow these commands to launch your sovereign ui interface.

### Phase A: Deployment
Spin up the LobeChat Docker container in the background.

```bash
# Execute the deployment
docker compose up -d

# Verify the container is running and healthy
docker ps | grep sovereign-lobechat
```

### Phase B: Register the Sovereign Agents Plugin
Open your browser to `http://localhost:3200`.

LobeChat will automatically detect your local Ollama models (`llama3.2` and `qwen2.5-coder`). Next, we add our 5 custom industry agents as an external tool.

1. In LobeChat, navigate to **Plugins** (the puzzle piece icon).
2. Click **Install Custom Plugin**.
3. In the Plugin URL field, enter the URL to our local manifest:
   `http://localhost:8000/manifest.json` (or your Codespace preview URL appended with `/manifest.json`).
4. Click **Install**.

You will now see the `Sovereign Industry Agents` plugin active. You can now prompt LobeChat to "Ask the Finance agent about travel limits" or "Check the Legal risk of uncapped liabilities," and it will automatically invoke our local Genkit backend!

---

## 📈 [INTEGRATOR] Proof of Work
**Focus**: *Local API routing and validation.*

The API Bridge successfully routes queries across all 5 Sovereign Industry domains.

Below is the verification output from your API router:
![Session 05 API Verification](proof/lobby_test.svg)

---

## 🏗️ [ARCHITECT] Proof of Work
**Focus**: *Plugin Orchestration & Prompt Routing.*

The ultimate architect verification is proving how LobeChat's LLM interprets the `manifest.json`. By examining the manifest, we see the `description_for_model` perfectly guides LobeChat to select the right domain parameter based on natural language intent.

```json
  "description_for_model": "This plugin routes the user's question to one of five professional AI agent swarms... The available domains are: finance, healthcare, supply_chain, edtech, legal."
```

---
**[Back to Curriculum Hub](../README.md)**
