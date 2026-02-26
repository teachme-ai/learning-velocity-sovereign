# Session 03: Multi-Agent Systems (Legal Swarm)

## [INTEGRATOR] Track

### Overview
This lab runs an M&A contract intelligence pipeline using **Google Genkit** (Python SDK). A `Paralegal Agent`, `Compliance Auditor`, and `Counsel Reporter` process scanned contract risk data sequentially to produce a Contract Due Diligence Brief for the Legal Board.

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
Open **http://localhost:4000** → **Flows** → `legal_agent_swarm` → trace M&A liability escalation across the three legal agents.

### Running in CLI Mode
```bash
/tmp/genkit_env/bin/python3 logic/swarm.py
```

---

## [ARCHITECT] Track

### Agent Roles
| Agent | System Role | Input | Output |
|---|---|---|---|
| `Paralegal Agent` | Summarises HIGH and MEDIUM liability markers | Scanned JSON | Liability summary |
| `Compliance Auditor` | Cross-checks against M&A law standards | Analyst output | Risk level determination |
| `Counsel Reporter` | Synthesises a Due Diligence Brief | Auditor output | 2-paragraph renegotiation brief |

### SDK Pattern
```python
from genkit.ai import Genkit
from genkit.plugins.ollama import Ollama
from genkit.plugins.ollama.models import ModelDefinition

ai = Genkit(plugins=[Ollama(models=[ModelDefinition(name="llama3.2:1b")])])

@ai.flow()
async def legal_agent_swarm(input: SwarmInput) -> SwarmOutput:
    ...
```

### Validation Output
![SVG Proof](/Users/khalidirfan/projects/Ai Bootcamps/03_multi_agent_systems/set_e_legal/success.svg)

---

# [VALIDATE]
# /tmp/genkit_env/bin/python3 logic/swarm.py
# Confirm: All agents complete, report saved to /tmp/legal_output/integrated_report.md
