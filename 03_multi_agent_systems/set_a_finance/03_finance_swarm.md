# Session 03: Multi-Agent Systems (Finance Swarm)

## [INTEGRATOR] Track

### Overview
This lab introduces an enterprise-grade, three-agent orchestration pipeline using **Google Genkit** (Python SDK). A `Financial Analyst`, `Corporate Auditor`, and `Executive Reporter` operate sequentially — each agent consuming the previous agent's output — to produce a final Corporate Investigation Memo from flagged expense data.

### Environment Setup
```bash
# Create the Genkit virtual environment (one-time)
python3 -m venv /tmp/genkit_env
/tmp/genkit_env/bin/pip install genkit genkit-plugin-ollama pydantic

# Ensure Ollama is running with the required model
ollama pull llama3.2:1b
```

### Running the Genkit Developer UI
The Genkit Dev UI lets you visually trace every agent prompt, handoff, and response in the browser:
```bash
# Install the Genkit CLI (one-time)
npm install -g genkit-cli

# Launch the Dev UI wired to the Finance Swarm
genkit start -- /tmp/genkit_env/bin/python3 logic/swarm.py
```
Open **http://localhost:4000** → **Flows** → `finance_agent_swarm` → **Run** → inspect each agent step in the trace viewer.

### Running in CLI Mode (no UI)
```bash
/tmp/genkit_env/bin/python3 logic/swarm.py
```

---

## [ARCHITECT] Track

### Agent Roles
| Agent | System Role | Input | Output |
|---|---|---|---|
| `Financial Analyst` | Identifies out-of-bounds expense violations | Raw CSV | Bulleted anomaly list |
| `Corporate Auditor` | Validates findings against Corporate Travel Policy | Analyst output | Prioritised risk list |
| `Executive Reporter` | Synthesises an Investigation Memo | Auditor output | 2-paragraph memo |

### SDK Pattern
```python
from genkit.ai import Genkit
from genkit.plugins.ollama import Ollama
from genkit.plugins.ollama.models import ModelDefinition
from pydantic import BaseModel, Field

ai = Genkit(plugins=[Ollama(models=[ModelDefinition(name="llama3.2:1b")])])

@ai.flow()
async def finance_agent_swarm(input: SwarmInput) -> SwarmOutput:
    ...

ai.run_main(main())
```

### Validation Output
![SVG Proof](/Users/khalidirfan/projects/Ai Bootcamps/03_multi_agent_systems/set_a_finance/success.svg)

---

# [VALIDATE]
# /tmp/genkit_env/bin/python3 logic/swarm.py
# Confirm: All 3 agents process sequentially, Final Report saved to /tmp/finance_output/integrated_report.md

---
**[Back to Curriculum Hub](../../README.md) | [Previous Lab: Session 02](../../02_executive_narrative_engine/set_a_finance/02_finance_narrative.md) | [Next Lab: Session 04](../../04_sovereign_knowledge_rag/set_a_finance/04_finance_rag.md)**
