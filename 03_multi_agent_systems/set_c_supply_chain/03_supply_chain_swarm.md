# Session 03: Multi-Agent Systems (Supply Chain Swarm)

## [INTEGRATOR] Track

### Overview
This lab runs a three-agent logistics intelligence pipeline using **Google Genkit** (Python SDK). A `Logistics Analyst`, `Warehouse Auditor`, and `Executive Reporter` process scrubbed inventory data sequentially to produce a Logistics Risk Memo outlining operational threats.

### Environment Setup
```bash
python3 -m venv /tmp/genkit_env
/tmp/genkit_env/bin/pip install genkit genkit-plugin-ollama pydantic
ollama pull llama3.2:1b
```

### Running the Genkit Developer UI
```bash
npm install -g genkit-cli
genkit start -- /tmp/genkit_env/bin/python3 logic/swarm.py
```
Open **http://localhost:4000** → **Flows** → `supply_chain_agent_swarm` → trace inventory anomaly propagation across agents.

### Running in CLI Mode
```bash
/tmp/genkit_env/bin/python3 logic/swarm.py
```

---

## [ARCHITECT] Track

### Agent Roles
| Agent | System Role | Input | Output |
|---|---|---|---|
| `Logistics Analyst` | Flags stock anomalies and SKU errors | Scrubbed CSV | Anomaly summary |
| `Warehouse Auditor` | Validates against Warehouse Integrity Protocols | Analyst output | Risk-prioritised findings |
| `Executive Reporter` | Synthesises a Logistics Risk Memo | Auditor output | 2-paragraph memo |

### SDK Pattern
```python
from genkit.ai import Genkit
from genkit.plugins.ollama import Ollama
from genkit.plugins.ollama.models import ModelDefinition

ai = Genkit(plugins=[Ollama(models=[ModelDefinition(name="llama3.2:1b")])])

@ai.flow()
async def supply_chain_agent_swarm(input: SwarmInput) -> SwarmOutput:
    ...
```

### Validation Output
![SVG Proof](/Users/khalidirfan/projects/Ai Bootcamps/03_multi_agent_systems/set_c_supply_chain/success.svg)

---

# [VALIDATE]
# /tmp/genkit_env/bin/python3 logic/swarm.py
# Confirm: All agents complete, report saved to /tmp/supply_chain_output/integrated_report.md

---
**[Back to Curriculum Hub](../../README.md) | [Previous Lab: Session 02](../../02_executive_narrative_engine/set_c_supply_chain/02_supply_chain_narrative.md) | [Next Lab: Session 04](../../04_sovereign_knowledge_rag/set_c_supply_chain/04_supply_chain_rag.md)**
