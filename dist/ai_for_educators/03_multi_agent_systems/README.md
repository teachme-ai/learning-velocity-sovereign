## Introduction
### AI for Educators Technical Curriculum Expert

As an expert in AI for Educators, I aim to provide a comprehensive and user-friendly technical curriculum that showcases cutting-edge technologies and their applications in education.

### Multi-Agent Systems — Setup
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

## Running a Swarm (CLI — Production Mode)
Run the swarm using the following command:

```bash
/tmp/genkit_env/bin/python3 set_a_ai_for_educators/logic/swarm.py
```

## Running with Genkit Developer UI (Learner Mode)
For learner mode, use the Genkit CLI (one-time):

```bash
# Install the Genkit CLI (one-time)
npm install -g genkit-cli

# Launch the Dev UI wired to the AI for Educators swarm
genkit start -- /tmp/genkit_env/bin/python3 set_a_ai_for_educators/logic/swarm.py
```

Open `http://localhost:4000` in your browser. Navigate to **Flows → ai_for_educators_agent_swarm** to run the flow and inspect each agent step in the trace viewer.

> Replace `set_a_ai_for_educators` with any of the other set directories (`set_b_ai_for_educators`, `set_c_supply_chain`, `set_d_edtech`, `set_e_legal`) to run those swarms.

## Packages Used
| Package | Version | Purpose |
|---|---|---|
| `genkit` | ≥0.5.1 | Core flow engine & Developer UI |
| `genkit-plugin-ollama` | ≥0.5.1 | Local Ollama LLM integration |
| `pydantic` | ≥2.0.0 | Input/output schema validation |

### GUIDELINES
1. Replace generic analogies (e.g., finance, banks, generic business) with AI for Educators specific ones.
2. Keep the technical steps, terminal commands, and code blocks IDENTICAL to maintain consistency across the curriculum.
3. Ensure the tone matches the industry (AI for Educators).
4. Return the ENTIRE rewritten markdown file content.