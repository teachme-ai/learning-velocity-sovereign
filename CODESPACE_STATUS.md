# CODESPACE_STATUS.md

> Generated: 2026-02-27 00:41:26
> Mode: Full Matrix (--all)

## Overall: ⚠️  2/12 PASSED

## Environment

| Component | Status | Detail |
|:---|:---:|:---|
| Genkit venv (`/tmp/genkit_env`) | ✅ | venv OK  (/tmp/genkit_env/bin/python3) |
| Ollama + llama3.2:1b | ✅ | Ollama running · llama3.2:1b ready |
| FastAPI API Bridge | ✅ | API Bridge running on port 8000 |

---

## Smoke Test Results

### Finance

| Test | Result | Detail |
|:---|:---:|:---|
| Session 01 — Data Pipeline | ❌ `[FAIL]` | Exit code 1 |
| Session 02 — Narrative Engine | ⚠️ `[CONDITIONAL_PASS]` | Requires env setup: Run Session 01 |
| Session 03 — Multi-Agent Swarm | ❌ `[FAIL]` | Expected 'Final Integrated Report' not found in output |
| Session 06 — Trace Quality | ❌ `[FAIL]` | Trace incomplete: missing 'success' state for 'finance_agent_swarm'. |
### Healthcare

| Test | Result | Detail |
|:---|:---:|:---|
| Session 01 — Data Pipeline | ❌ `[FAIL]` | Exit code 1 |
| Session 02 — Narrative Engine | ⚠️ `[CONDITIONAL_PASS]` | Requires env setup: Run Session 01 |
| Session 03 — Multi-Agent Swarm | ❌ `[FAIL]` | Expected 'Final Integrated Report' not found in output |
| Session 06 — Trace Quality | ✅ `[PASS]` | Trace verified: healthcare_agent_swarm completed successfully. |
### Supply Chain

| Test | Result | Detail |
|:---|:---:|:---|
| Session 01 — Data Pipeline | ❌ `[FAIL]` | Timed out after 120s |
| Session 02 — Narrative Engine | ⚠️ `[CONDITIONAL_PASS]` | Requires env setup: Run Session 01 |
| Session 03 — Multi-Agent Swarm | ❌ `[FAIL]` | Expected 'Final Integrated Report' not found in output |
| Session 06 — Trace Quality | ✅ `[PASS]` | Trace verified: supply_chain_agent_swarm completed successfully. |

---

## ⚠️ Conditional Details (env setup required)

### [Finance] Session 02 — Narrative Engine
```
01_data_pipeline_automation/data/flagged_expenses.csv
[ERROR] Flagged expenses CSV not found at:
  /Users/khalidirfan/projects/Ai Bootcamps/dist/ai_for_global_finance/02_executive_narrative_engine/01_data_pipeline_automation/data/flagged_expenses.csv
Run Session 01's cleaner.py first to generate it.
```

### [Healthcare] Session 02 — Narrative Engine
```
pipeline_automation/data/flagged_expenses.csv
[ERROR] Flagged expenses CSV not found at:
  /Users/khalidirfan/projects/Ai Bootcamps/builds/ai_in_retail_and_e-commerce/02_executive_narrative_engine/01_data_pipeline_automation/data/flagged_expenses.csv
Run Session 01's cleaner.py first to generate it.
```

### [Supply Chain] Session 02 — Narrative Engine
```
data_pipeline_automation/data/flagged_expenses.csv
[ERROR] Flagged expenses CSV not found at:
  /Users/khalidirfan/projects/Ai Bootcamps/builds/sustainability_and_esg/02_executive_narrative_engine/01_data_pipeline_automation/data/flagged_expenses.csv
Run Session 01's cleaner.py first to generate it.
```


---

## ❌ Failure Details

### [Finance] Session 01 — Data Pipeline
```
/01_data_pipeline_automation/set_ai_for_global_finance/logic/cleaner.py", line 143, in flag_high_value
    flagged = df[df["amount_usd"] > threshold].copy()
                 ~~^^^^^^^^^^^^^^
  File "/private/tmp/genkit_env/lib/python3.13/site-packages/pandas/core/frame.py", line 4113, in __getitem__
    indexer = self.columns.get_loc(key)
  File "/private/tmp/genkit_env/lib/python3.13/site-packages/pandas/core/indexes/range.py", line 417, in get_loc
    raise KeyError(key)
KeyError: 'amount_usd'
```

### [Finance] Session 03 — Multi-Agent Swarm
```
" shadows an attribute in parent "BaseModel"
  class PromptInputConfig(BaseModel):
/private/tmp/genkit_env/lib/python3.13/site-packages/dotpromptz/typing.py:256: UserWarning: Field name "schema" in "PromptOutputConfig" shadows an attribute in parent "BaseModel"
  class PromptOutputConfig(BaseModel):
```

### [Finance] Session 06 — Trace Quality
```

```

### [Healthcare] Session 01 — Data Pipeline
```
ta_pipeline_automation/set_ai_in_retail_and_e-commerce/logic/cleaner.py", line 143, in flag_high_value
    flagged = df[df["amount_usd"] > threshold].copy()
                 ~~^^^^^^^^^^^^^^
  File "/private/tmp/genkit_env/lib/python3.13/site-packages/pandas/core/frame.py", line 4113, in __getitem__
    indexer = self.columns.get_loc(key)
  File "/private/tmp/genkit_env/lib/python3.13/site-packages/pandas/core/indexes/range.py", line 417, in get_loc
    raise KeyError(key)
KeyError: 'amount_usd'
```

### [Healthcare] Session 03 — Multi-Agent Swarm
```
" shadows an attribute in parent "BaseModel"
  class PromptInputConfig(BaseModel):
/private/tmp/genkit_env/lib/python3.13/site-packages/dotpromptz/typing.py:256: UserWarning: Field name "schema" in "PromptOutputConfig" shadows an attribute in parent "BaseModel"
  class PromptOutputConfig(BaseModel):
```

### [Supply Chain] Session 01 — Data Pipeline
```
Process killed — exceeded timeout.
```

### [Supply Chain] Session 03 — Multi-Agent Swarm
```
" shadows an attribute in parent "BaseModel"
  class PromptInputConfig(BaseModel):
/private/tmp/genkit_env/lib/python3.13/site-packages/dotpromptz/typing.py:256: UserWarning: Field name "schema" in "PromptOutputConfig" shadows an attribute in parent "BaseModel"
  class PromptOutputConfig(BaseModel):
```

---

## Pre-Validation Gate

A session may be marked `✅ VALIDATED` in `PROJECT_MANIFEST.md` only when:
- This report shows `[PASS]` for that session + domain
- `HEALTH_CHECK.md` (Systems Validator) also shows `✅`
- An SVG proof exists (Forensic Documentarian)