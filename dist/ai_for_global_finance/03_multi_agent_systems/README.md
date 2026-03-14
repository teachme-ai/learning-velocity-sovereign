Here are the rewritten 'Introduction' and 'Business Value' sections of the lab manual for the AI for Global Finance industry:

## Introduction

**Multi-Agent Systems — Setting Up**

Before diving into the world of AI for Global Finance, it's essential to understand how multiple agents interact with each other in a complex system. This session will guide you through setting up a multi-agent system using the Genkit SDK with the Ollama plugin.

To start, ensure that you have installed the Genkit SDK and the Ollama plugin:

```bash
# From the project root — uses the /tmp venv for sandbox compatibility
python3 -m venv /tmp/genkit_env
/tmp/genkit_env/bin/pip install genkit genkit-plugin-ollama pydantic
```

Next, start the local server on port 11434 with Ollama:

```bash
ollama serve         # starts the local server on port 11434
ollama pull llama3.2:1b
```

## Running a Swarm (CLI — Production Mode)

To run a swarm in production mode, you'll need to create a `set_a_ai_for_global_finance/logic/swarm.py` file:

```bash
/tmp/genkit_env/bin/python3 set_a_ai_for_global_finance/logic/swarm.py
```

Alternatively, you can use the Genkit UI (Learner Mode) to run the swarm. First, install the Genkit CLI and launch it with your desired swarm configuration:

```bash
# Install the Genkit CLI (one-time)
npm install -g genkit-cli

# Launch the Dev UI wired to the AI for Global Finance swarm
genkit start -- /tmp/genkit_env/bin/python3 set_a_ai_for_global_finance/logic/swarm.py
```

Open `http://localhost:4000` in your browser to navigate to **Flows → ai_for_global_finance_agent_swarm** and run the flow.

> Replace `set_a_ai_for_global_finance` with any of the other set directories (`set_b_ai_for_global_finance`, `set_c_supply_chain`, `set_d_edtech`, `set_e_legal`) to run those swarms.

## Packages Used

| Package | Version | Purpose |
|---|---|---|
| `genkit` | ≥0.5.1 | Core flow engine & Developer UI |
| `genkit-plugin-ollama` | ≥0.5.1 | Local Ollama LLM integration |
| `pydantic` | ≥2.0.0 | Input/output schema validation |
# Limit context window