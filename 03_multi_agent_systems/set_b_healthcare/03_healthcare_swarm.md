# Session 03: Multi-Agent Systems (Healthcare Swarm)

## [INTEGRATOR] Track

### Overview
This lab orchestrates a HIPAA-aware, three-agent clinical compliance pipeline using **Google Genkit** (Python SDK). A `Clinical Analyst`, `Compliance Auditor`, and `Hospital Reporter` process scrubbed patient billing data sequentially to produce a Clinical Compliance Memo.

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
Open **http://localhost:4000** → **Flows** → `healthcare_agent_swarm` → trace each agent's HIPAA validation steps.

### Running in CLI Mode
```bash
/tmp/genkit_env/bin/python3 logic/swarm.py
```

---

## [ARCHITECT] Track

### Agent Roles
| Agent | System Role | Input | Output |
|---|---|---|---|
| `Clinical Analyst` | Flags billing anomalies and malformed ICD-10 codes | Scrubbed CSV | Anomaly summary |
| `Compliance Auditor` | Validates against HIPAA billing standards | Analyst output | Risk-prioritised findings |
| `Hospital Reporter` | Synthesises a Clinical Compliance Memo | Auditor output | 2-paragraph memo |

### SDK Pattern
```python
from genkit.ai import Genkit
from genkit.plugins.ollama import Ollama
from genkit.plugins.ollama.models import ModelDefinition

ai = Genkit(plugins=[Ollama(models=[ModelDefinition(name="llama3.2:1b")])])

@ai.flow()
async def healthcare_agent_swarm(input: SwarmInput) -> SwarmOutput:
    ...
```

### Validation Output
![SVG Proof](/Users/khalidirfan/projects/Ai Bootcamps/03_multi_agent_systems/set_b_healthcare/success.svg)

---

# [VALIDATE]
# /tmp/genkit_env/bin/python3 logic/swarm.py
# Confirm: Clinical Analyst → Compliance Auditor → Hospital Reporter, report saved to /tmp/healthcare_output/integrated_report.md
