Here's a rewritten version of the 'Introduction' and 'Business Value' sections for the Sustainability & ESG industry, following the same format as your original lab manual:

## Session 03: Multi-Agent Systems (Sustainability & ESG Swarm)

### [INTEGRATOR] Track

#### Overview
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

# Launch the Dev UI wired to the Sustainability & ESG Swarm
genkit start -- /tmp/genkit_env/bin/python3 logic/swarm.py
```
Open **http://localhost:4000** → **Flows** → `sustainability_and_esg_agent_swarm` → **Run** → inspect each agent step in the trace viewer.

### Running in CLI Mode (no UI)

```bash
/tmp/genkit_env/bin/python3 logic/swarm.py
```

---

## [ARCHITECT] Track

#### Agent Roles
| Agent | System Role | Input | Output |
|---|---|---|---|
| `Financial Analyst` | Identifies out-of-bounds expense violations | Raw CSV | Bulleted anomaly list |
| `Corporate Auditor` | Validates findings against Corporate Travel Policy | Analyst output | Prioritised risk list |
| `Executive Reporter` | Synthesises an Investigation Memo | Auditor output | 2-paragraph memo |

#### SDK Pattern
```python
from genkit.ai import Genkit
from genkit.plugins.ollama import Ollama
from genkit.plugins.ollama.models import ModelDefinition
from pydantic import BaseModel, Field

ai = Genkit(plugins=[Ollama(models=[ModelDefinition(name="llama3.2:1b")])])

@ai.flow()
async def sustainability_and_esg_agent_swarm(input: SwarmInput) -> SwarmOutput:
    ...

ai.run_main(main())
```

#### Validation Output
![SVG Proof](/Users/khalidirfan/projects/Ai Bootcamps/03_multi_agent_systems/set_a_sustainability_and_esg/success.svg)

---

# [VALIDATE]
# /tmp/genkit_env/bin/python3 logic/swarm.py
# Confirm: All 3 agents process sequentially, Final Report saved to /tmp/sustainability_and_esg_output/integrated_report.md

---
**[Back to Curriculum Hub](../../README.md) | [Previous Lab: Session 02](../../02_executive_narrative_engine/set_a_sustainability_and_esg/02_sustainability_and_esg_narrative.md) | [Next Lab: Session 04](../../04_sovereign_knowledge_rag/set_a_sustainability_and_esg/04_sustainability_and_esg_rag.md)**

### Business Value
The implementation of the three-agent system demonstrates a key advantage in the Sustainability & ESG industry:

* **Improved accuracy**: The combination of the `Financial Analyst`, `Corporate Auditor`, and `Executive Reporter` agents ensures that out-of-bounds expense violations are identified accurately, reducing the risk of reputational damage.
* **Enhanced efficiency**: By sequentially processing input data from each agent, the system streamlines the investigative process, enabling faster and more accurate results.
* **Increased transparency**: The use of visual debugging tools in the Genkit Dev UI provides a clear understanding of the flow of information through the system, facilitating collaboration among stakeholders.

By leveraging this multi-agent system, organizations can:

* Enhance their ability to identify and address sustainability and ESG-related issues
* Improve decision-making by providing a more complete picture of complex data sets
* Strengthen relationships with stakeholders by demonstrating a commitment to transparency and accountability.