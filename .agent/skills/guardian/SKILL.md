---
name: Codespace Guardian
description: 'Full-suite health check across all sessions and domains. Confirms Ollama is live, all logic scripts exit cleanly, and generates HEALTH_CHECK.md.'
triggers:
  - 'validate system'
  - 'health check'
  - 'run guardian'
  - 'codespace check'
---

# Codespace Guardian Skill

## Purpose
Performs **live smoke tests** in the actual terminal environment (local or Codespace).  
Unlike the Systems Validator (static syntax checks), the Guardian actually **executes** each script and captures real output or failures.

**Rule:** No session may be marked `✅ VALIDATED` in `PROJECT_MANIFEST.md` until the Guardian shows `[PASS]` for that smoke test.

## Instructions
1. Verify the Genkit Python virtual environment at `/tmp/genkit_env` is present and has the required packages.
2. Confirm the Ollama service is reachable at `http://localhost:11434`.
3. Run a live Smoke Test for each configured session of Set A (Finance) by default — outputs are captured to detect runtime failures.
4. Write a `CODESPACE_STATUS.md` to the project root with `[PASS]` / `[FAIL]` per test, including the captured terminal error for any failure.

## Bundled Scripts
- Use `scripts/verify_env.py` to run all checks.

## Usage
```bash
# Standard smoke test (Set A — Finance)
python3 .agent/skills/guardian/scripts/verify_env.py

# Full matrix (all 5 domains)
python3 .agent/skills/guardian/scripts/verify_env.py --all
```

## Standard: Pre-Validation Gate
Before marking any session as `✅ VALIDATED`:
1. Run `verify_env.py`
2. Confirm the relevant row shows `[PASS]`
3. Only then update `PROJECT_MANIFEST.md`
