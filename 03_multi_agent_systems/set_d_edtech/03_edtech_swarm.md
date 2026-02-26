# Session 03: Multi-Agent Systems (EdTech Swarm)

## [INTEGRATOR] Track

### Overview
This lab orchestrates an Academic Integrity pipeline using **Google Genkit** (Python SDK). A `Pedagogical Analyst`, `Academic Auditor`, and `Faculty Reporter` process cleaned student log data sequentially to produce a Learning Decay Executive Brief.

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
Open **http://localhost:4000** → **Flows** → `edtech_agent_swarm` → observe how each pedagogical agent evaluates the LMS data.

### Running in CLI Mode
```bash
/tmp/genkit_env/bin/python3 logic/swarm.py
```

---

## [ARCHITECT] Track

### Agent Roles
| Agent | System Role | Input | Output |
|---|---|---|---|
| `Pedagogical Analyst` | Flags scores >100 and negative time values | Cleaned CSV | Anomaly summary |
| `Academic Auditor` | Validates against Academic Integrity Policy | Analyst output | LMS bug vs. cheating determination |
| `Faculty Reporter` | Synthesises a Learning Decay Executive Brief | Auditor output | 2-paragraph brief |

### SDK Pattern
```python
from genkit.ai import Genkit
from genkit.plugins.ollama import Ollama
from genkit.plugins.ollama.models import ModelDefinition

ai = Genkit(plugins=[Ollama(models=[ModelDefinition(name="llama3.2:1b")])])

@ai.flow()
async def edtech_agent_swarm(input: SwarmInput) -> SwarmOutput:
    ...
```

### Validation Output
![SVG Proof](/Users/khalidirfan/projects/Ai Bootcamps/03_multi_agent_systems/set_d_edtech/success.svg)

---

# [VALIDATE]
# /tmp/genkit_env/bin/python3 logic/swarm.py
# Confirm: All agents complete, report saved to /tmp/edtech_output/integrated_report.md

---
**[Back to Curriculum Hub](../../README.md) | [Previous Lab: Session 02](../../02_executive_narrative_engine/set_d_edtech/02_edtech_narrative.md) | [Next Lab: Session 04](../../04_sovereign_knowledge_rag/set_d_edtech/04_edtech_rag.md)**
