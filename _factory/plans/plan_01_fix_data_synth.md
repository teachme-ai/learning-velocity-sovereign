# Plan 01 — Fix `data_synth.py` (Industry-Aware Data Generation)

**Model:** Claude Sonnet 4.6 (Amazon Q)
**File:** `.agent/skills/factory/data_synth.py`
**Priority:** 1 of 7
**Effort:** ~5 lines changed

---

## Problem

The function `generate_dirty_data(slug, industry)` receives an `industry`
argument but the prompt on line 12 ignores it entirely — it is hardcoded
to "Retail industry expense data". Every industry (Finance, Healthcare,
Cyber-Security, EdTech) generates identical Retail CSV output.

---

## Instructions for Amazon Q

Open the file: `.agent/skills/factory/data_synth.py`

### Change 1 — Replace the hardcoded prompt (line 11–21)

Replace the hardcoded prompt string with a dynamic one that uses the
`industry` variable. The new prompt must instruct the LLM to:

- Generate 50 rows of CSV data relevant to the specific `industry`
- Choose column names appropriate for that industry
- Always include: an id column, a date column, and an amount/value column
- Inject intentional dirty data at ~15% of rows (nulls, duplicates, format errors, misspellings)
- Return only the CSV starting with the header row — no preamble, no explanation

### Change 2 — Fix the CSV extraction logic (line 31)

The current code looks for the string `"transaction_id"` to find where
the CSV starts. This breaks for any industry that doesn't use that column name.

Replace this with a generic check: find the first line that contains a comma.
That is the header row regardless of industry.

### Change 3 — Do NOT change anything else

- Function signature stays: `generate_dirty_data(slug, industry)`
- File write paths stay the same (both `dirty_data.csv` and `corporate_expenses.csv`)
- The `if __name__ == "__main__"` block stays the same

---

## Expected Outcome

| Industry | Expected Columns (examples) |
|---|---|
| Finance | transaction_id, date, account_id, category, amount_usd, anomaly_flag |
| Healthcare | record_id, date, patient_id, diagnosis_code, treatment, cost_usd |
| Cyber-Security | log_id, timestamp, source_ip, event_type, severity, bytes_transferred |
| EdTech | session_id, date, student_id, course, completion_pct, score |
| Retail | transaction_id, date, employee_id, department, category, amount_usd |

---

## TESTING PLAN

### Pre-conditions (verify before running any test)

```bash
# 1. Confirm Ollama is running
curl http://localhost:11434/api/tags
# Expected: JSON response listing available models

# 2. Confirm llama3.2:1b is available
ollama list | grep llama3.2
# Expected: llama3.2:1b appears in the list

# 3. Confirm the file exists
ls .agent/skills/factory/data_synth.py
# Expected: file found, no error
```

If any pre-condition fails — STOP. Fix the environment before proceeding.

---

### Test 1 — Word "Retail" must not appear in the prompt

```bash
grep -n "Retail" .agent/skills/factory/data_synth.py
```

**Expected result:** No output (zero matches)

**Fail condition:** If "Retail" appears on any line inside the prompt string — the change was not applied correctly. Re-read the file and fix.

---

### Test 2 — Variable `industry` must appear in the prompt string

```bash
grep -n "industry" .agent/skills/factory/data_synth.py
```

**Expected result:** At least one match inside the prompt string block (not just the function signature)

**Fail condition:** If `industry` only appears in the function signature (`def generate_dirty_data(slug, industry)`) but not inside the prompt — the fix is incomplete.

---

### Test 3 — Run with Cyber-Security industry

```bash
python3 .agent/skills/factory/data_synth.py ai_for_cyber_security "AI for Cyber-Security"
```

**Expected result:**
- Terminal prints: `🧬 Generating 50 rows of synthetic data for AI for Cyber-Security...`
- Terminal prints: `✅ Data written to ...`
- No Python errors or tracebacks

**Then inspect the output file:**
```bash
head -5 "_factory/templates/01_data_pipeline_automation/set_{{ industry_slug }}/data/dirty_data.csv"
```

**Expected result:**
- First line is a header row with comma-separated column names
- Column names relate to Cyber-Security (e.g. log_id, ip_address, severity, event_type)
- Column names do NOT include "employee_id", "department", "SKU" (retail columns)

**Fail condition:** Output contains retail columns → prompt is not using `industry` variable correctly.

---

### Test 4 — Run with Finance industry

```bash
python3 .agent/skills/factory/data_synth.py ai_for_global_finance "AI for Global Finance"
```

**Then inspect:**
```bash
head -5 "_factory/templates/01_data_pipeline_automation/set_{{ industry_slug }}/data/dirty_data.csv"
```

**Expected result:**
- Column names relate to Finance (e.g. transaction_id, account_id, amount_usd, currency)
- Different columns to the Cyber-Security run above

**Fail condition:** Identical columns to Test 3 → industry variable not being used in prompt.

---

### Test 5 — Confirm dirty data rows exist

```bash
python3 - <<'EOF'
import csv
with open("_factory/templates/01_data_pipeline_automation/set_{{ industry_slug }}/data/dirty_data.csv") as f:
    rows = list(csv.reader(f))

total = len(rows) - 1  # minus header
print(f"Total rows: {total}")

# Count rows with empty fields
dirty = sum(1 for row in rows[1:] if any(cell.strip() == '' for cell in row))
print(f"Rows with empty fields (dirty): {dirty}")
print(f"Dirty rate: {dirty/total:.0%}")

assert total >= 40, f"FAIL: Expected 50 rows, got {total}"
assert dirty > 0, "FAIL: No dirty rows found — dirty data injection not working"
print("PASS: Data schema and dirty rows validated")
EOF
```

**Expected result:** `PASS: Data schema and dirty rows validated`

---

### Test 6 — Confirm both output files exist

```bash
ls -la "_factory/templates/01_data_pipeline_automation/set_{{ industry_slug }}/data/"
```

**Expected result:** Both files present:
- `dirty_data.csv`
- `corporate_expenses.csv`

---

### PHASE 1 PASS CRITERIA

All 6 tests must pass before moving to Plan 02:

| Test | Check | Status |
|---|---|---|
| Pre-conditions | Ollama running, model available, file exists | ☐ |
| Test 1 | "Retail" not in prompt | ☐ |
| Test 2 | `industry` variable used in prompt | ☐ |
| Test 3 | Cyber-Security run succeeds, columns relevant | ☐ |
| Test 4 | Finance run succeeds, different columns to Test 3 | ☐ |
| Test 5 | 40+ rows, dirty data present | ☐ |
| Test 6 | Both CSV files written | ☐ |

**If all pass:** Proceed to Plan 02.
**If any fail:** Fix the issue in `data_synth.py` and re-run the failing test before proceeding.
