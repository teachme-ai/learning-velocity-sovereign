# Session 03: Multi-Agent Systems — Setup

## Prerequisites

Before running any swarm, install the Genkit SDK with the Ollama plugin:

```bash
# From the project root — uses the /tmp venv for sandbox compatibility
python3 -m venv /tmp/genkit_env
/tmp/genkit_env/bin/pip install genkit genkit-plugin-ollama pydantic
```

Ensure Ollama is running with the llama3.2:1b model:

```bash
ollama serve         # starts the local server on port 11434
ollama pull llama3.2:1b
```

## Running a Swarm (CLI — Production Mode)

```bash
/tmp/genkit_env/bin/python3 set_a_finance/logic/swarm.py
```

## Running with Genkit Developer UI (Learner Mode)

The Genkit UI lets you visualise every agent step, prompt, and response trace in the browser:

```bash
# Install the Genkit CLI (one-time)
npm install -g genkit-cli

# Launch the Dev UI wired to the Finance swarm
genkit start -- /tmp/genkit_env/bin/python3 set_a_finance/logic/swarm.py
```

Open `http://localhost:4000` in your browser. Navigate to **Flows → finance_agent_swarm** to run the flow and inspect each agent step in the trace viewer.

> Replace `set_a_finance` with any of the other set directories (`set_b_healthcare`, `set_c_supply_chain`, `set_d_edtech`, `set_e_legal`) to run those swarms.

## Packages Used

| Package | Version | Purpose |
|---|---|---|
| `genkit` | ≥0.5.1 | Core flow engine & Developer UI |
| `genkit-plugin-ollama` | ≥0.5.1 | Local Ollama LLM integration |
| `pydantic` | ≥2.0.0 | Input/output schema validation |
