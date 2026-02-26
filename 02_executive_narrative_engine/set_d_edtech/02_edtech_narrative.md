# Session 02: EdTech Narrative Engine

## [INTEGRATOR] Track

### Overview
Leveraging the anomaly aggregations established in Session 01, this script utilizes the `llama3.2:1b` model to inform faculty administrators precisely where and how student metrics are logging falsely on the LMS.

### Execution
Extract the insights via a 'Learning Velocity Memo':
```bash
python3 02_executive_narrative_engine/set_d_edtech/logic/velocity_memo_gen.py
```

## [ARCHITECT] Track

### Validation Pipeline
The LLM accurately correlates the volume and distribution of the outlier records into a concise strategy to patch the core LMS infrastructure. 

### Validation Output
Sending EdTech summary to Local Ollama model (llama3.2:1b)...
Learning Velocity Memo successfully generated and saved to: /tmp/edtech_output/velocity_memo.md---

# [VALIDATE]
python3 02_executive_narrative_engine/set_d_edtech/logic/velocity_memo_gen.py
# Confirm LLM triggers and writes memo logic explicitly for the faulty module codes.
