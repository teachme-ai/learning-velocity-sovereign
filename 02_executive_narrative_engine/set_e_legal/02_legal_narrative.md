# Session 02: Legal Narrative Engine

## [INTEGRATOR] Track

### Overview
Legal diligence bridges structured text analysis mapping directly to executive impact summarizing statements. Using `llama3.2:1b`, the application translates clause severities into actionable advice.

### Execution
Generate the final Contract Due Diligence Brief:
```bash
python3 02_executive_narrative_engine/set_e_legal/logic/due_diligence_gen.py
```

## [ARCHITECT] Track

### Validation Pipeline
Successfully integrates the raw findings from `01_legal_pipeline` to format an executive legal report prioritizing liability adjustments via local Ollama.

### Validation Output
Sending Legal Due Diligence summary to Local Ollama model (llama3.2:1b)...
Contract Due Diligence successfully generated and saved to: /tmp/legal_output/due_diligence_brief.md---

# [VALIDATE]
python3 02_executive_narrative_engine/set_e_legal/logic/due_diligence_gen.py
# Confirm local LLM queries the severity map correctly.
