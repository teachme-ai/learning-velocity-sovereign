# CODESPACE_STATUS.md

> Generated: 2026-02-26 16:54:35
> Mode: Full Matrix (--all)

## Overall: ⚠️  14/20 PASSED

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
| Session 01 — Data Pipeline | ✅ `[PASS]` | Clean exit · output verified |
| Session 02 — Narrative Engine | ⚠️ `[CONDITIONAL_PASS]` | Requires env setup: Run Session 01 |
| Session 03 — Multi-Agent Swarm | ✅ `[PASS]` | Clean exit · output verified |
| Session 06 — Trace Quality | ❌ `[FAIL]` | No trace JSON files found in /Users/khalidirfan/projects/Ai Bootcamps/06_observability/audit_logs/finance |
### Healthcare

| Test | Result | Detail |
|:---|:---:|:---|
| Session 01 — Data Pipeline | ✅ `[PASS]` | Clean exit · output verified |
| Session 02 — Narrative Engine | ✅ `[PASS]` | Clean exit · output verified |
| Session 03 — Multi-Agent Swarm | ✅ `[PASS]` | Clean exit · output verified |
| Session 06 — Trace Quality | ❌ `[FAIL]` | No trace JSON files found in /Users/khalidirfan/projects/Ai Bootcamps/06_observability/audit_logs/healthcare |
### Supply Chain

| Test | Result | Detail |
|:---|:---:|:---|
| Session 01 — Data Pipeline | ✅ `[PASS]` | Clean exit · output verified |
| Session 02 — Narrative Engine | ✅ `[PASS]` | Clean exit · output verified |
| Session 03 — Multi-Agent Swarm | ✅ `[PASS]` | Clean exit · output verified |
| Session 06 — Trace Quality | ❌ `[FAIL]` | No trace JSON files found in /Users/khalidirfan/projects/Ai Bootcamps/06_observability/audit_logs/supply_chain |
### EdTech

| Test | Result | Detail |
|:---|:---:|:---|
| Session 01 — Data Pipeline | ✅ `[PASS]` | Clean exit · output verified |
| Session 02 — Narrative Engine | ✅ `[PASS]` | Clean exit · output verified |
| Session 03 — Multi-Agent Swarm | ✅ `[PASS]` | Clean exit · output verified |
| Session 06 — Trace Quality | ❌ `[FAIL]` | No trace JSON files found in /Users/khalidirfan/projects/Ai Bootcamps/06_observability/audit_logs/edtech |
### Legal

| Test | Result | Detail |
|:---|:---:|:---|
| Session 01 — Data Pipeline | ✅ `[PASS]` | Clean exit · output verified |
| Session 02 — Narrative Engine | ✅ `[PASS]` | Clean exit · output verified |
| Session 03 — Multi-Agent Swarm | ✅ `[PASS]` | Clean exit · output verified |
| Session 06 — Trace Quality | ❌ `[FAIL]` | No trace JSON files found in /Users/khalidirfan/projects/Ai Bootcamps/06_observability/audit_logs/legal |

---

## ⚠️ Conditional Details (env setup required)

### [Finance] Session 02 — Narrative Engine
```
executive_narrative_engine/01_data_pipeline_automation/data/flagged_expenses.csv
[ERROR] Flagged expenses CSV not found at:
  /Users/khalidirfan/projects/Ai Bootcamps/02_executive_narrative_engine/01_data_pipeline_automation/data/flagged_expenses.csv
Run Session 01's cleaner.py first to generate it.
```


---

## ❌ Failure Details

### [Finance] Session 06 — Trace Quality
```

```

### [Healthcare] Session 06 — Trace Quality
```

```

### [Supply Chain] Session 06 — Trace Quality
```

```

### [EdTech] Session 06 — Trace Quality
```

```

### [Legal] Session 06 — Trace Quality
```

```

---

## Pre-Validation Gate

A session may be marked `✅ VALIDATED` in `PROJECT_MANIFEST.md` only when:
- This report shows `[PASS]` for that session + domain
- `HEALTH_CHECK.md` (Systems Validator) also shows `✅`
- An SVG proof exists (Forensic Documentarian)