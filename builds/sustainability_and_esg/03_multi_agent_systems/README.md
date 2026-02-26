## Introduction to Multi-Agent Systems - Setup for Sustainability & ESG

### Prerequisites

Before running any swarm, ensure you have installed the Genkit SDK with the Ollama plugin:

```bash
# From the project root — uses the /tmp venv for sandbox compatibility
python3 -m venv /tmp/genkit_env
/tmp/genkit_env/bin/pip install genkit genkit-plugin-ollama pydantic
```

Verify that Ollama is running with the llama3.2:1b model:

```bash
ollama serve         # starts the local server on port 11434
ollama pull llama3.2:1b
```

### Running a Swarm (CLI — Production Mode)

To run your swarm in production mode, navigate to the swarm directory and execute:

```bash
/tmp/genkit_env/bin/python3 set_a_sustainability_and_esg/logic/swarm.py
```

Alternatively, you can start Genkit with the learner UI to visualize every agent step:

```bash
# Install the Genkit CLI (one-time)
npm install -g genkit-cli

# Launch the Dev UI wired to the Sustainability & ESG swarm
genkit start -- /tmp/genkit_env/bin/python3 set_a_sustainability_and_esg/logic/swarm.py
```

Open `http://localhost:4000` in your browser. Navigate to **Flows → sustainability_and_esg_agent_swarm** to run the flow and inspect each agent step in the trace viewer.

### Packages Used

| Package | Version | Purpose |
|---|---|---|
| `genkit` | ≥0.5.1 | Core flow engine & Developer UI |
| `genkit-plugin-ollama` | ≥0.5.1 | Local Ollama LLM integration |
| `pydantic` | ≥2.0.0 | Input/output schema validation |

### Limitations

The following terms and concepts are excluded from this documentation:

* Financial terminology (banks, investments, etc.)
* Industry-specific business terminology
* Technical jargon not specific to Sustainability & ESG