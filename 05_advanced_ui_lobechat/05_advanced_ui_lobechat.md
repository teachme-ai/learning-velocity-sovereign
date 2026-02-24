# Lab 05: Advanced UI — LobeChat Sovereign Interface
**Persona**: Supportive Facilitator (Empathetic, clear, enterprise-focused)

## 🎯 The Objective
In this final capstone lab, we bring our enterprise AI architecture to life with a comprehensive User Interface. We will deploy **LobeChat**, configuring it as a fully sovereign, open-source AI playground that securely connects directly to our local Ollama models. 

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

## 🛠️ 2. Step-by-Step Execution

Follow these commands to launch your sovereign interface and verify the connections.

### Phase A: Deployment
Spin up the LobeChat Docker container in the background.

```bash
# Execute the deployment
docker compose up -d

# Verify the container is running and healthy
docker ps | grep sovereign-lobechat
```

### Phase B: Connection Verification
Confirm that the Docker container can successfully tunnel into your host machine's Ollama instance.

```bash
# Check the host Ollama connection (from outside the container)
curl -s http://localhost:11434/api/tags | head -c 200

# Access the LobeChat web server directly
curl -s -o /dev/null -w "%{http_code}" http://localhost:3200/chat
# Expected output: 200
```

---

## 📈 [INTEGRATOR] Proof of Work
**Focus**: *Sovereign Deployment and Container orchestration.*

A successful execution confirms the `lobehub/lobe-chat` container is running and listening on Port 3200, completely detached from external cloud providers.

Below is your target terminal proof:
```text
docker ps | grep sovereign-lobechat

CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS          PORTS                                                                              NAMES
f930389af307   lobehub/lobe-chat   "/bin/node /app/star…"   5 minutes ago    Up 5 minutes    0.0.0.0:3200->3200/tcp, [::]:3200->3200/tcp                                        sovereign-lobechat
```

---

## 🏗️ [ARCHITECT] Proof of Work
**Focus**: *Local Model Tunneling.*

The ultimate architect verification is proving that LobeChat can *see* the local LLMs. The `docker-compose.yml` bridges this gap using `host.docker.internal`.

```yaml
# ARCHITECT EVIDENCE: Sovereign Configuration Block
      # ── SOVEREIGN CONFIGURATION ──
      # Disable cloud provider integrations
      - OPENAI_API_KEY=
      - ACCESS_CODE=sovereign2026

      # ── OLLAMA INTEGRATION ──
      # Enable the Ollama provider
      - OLLAMA_PROXY_URL=http://host.docker.internal:11434/v1
```

**Target Result**:
Open your browser to `http://localhost:3200`. 
Click on the Model Selection dropdown in the chat bar. You should see `llama3.2` and `qwen2.5-coder` available for immediate, sovereign use!
