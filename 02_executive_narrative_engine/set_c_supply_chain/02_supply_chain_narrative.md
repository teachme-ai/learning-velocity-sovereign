# Session 02: Supply Chain Narrative Engine

## [INTEGRATOR] Track

### Overview
This pipeline builds a bridge between structured automated warehouse anomaly metadata and high-level operational reporting using a local LLM proxy. 

### Execution
Run the risk memo generator to formulate a professional summary using `llama3.2:1b`:
```bash
python3 02_executive_narrative_engine/set_c_supply_chain/logic/risk_memo_gen.py
```

## [ARCHITECT] Track

### Validation Pipeline
The script aggregates metrics across missing item SKUs, stockout realities, and pricing limits, proxying the output to Ollama to create an executive brief on Logistics Risk. 

### Validation Output
Sending supply chain summary to Local Ollama model (llama3.2:1b)...
Logistics Risk Memo successfully generated and saved to: /tmp/supply_chain_output/risk_memo.md---

# [VALIDATE]
python3 02_executive_narrative_engine/set_c_supply_chain/logic/risk_memo_gen.py
# Check that the logic correctly aggregates anomalies and queries Local Ollama.
