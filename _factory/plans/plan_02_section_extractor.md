# Plan 02 — Section Extractor in `context_refiner.py` (80% Token Reduction)

**Model:** Claude Sonnet 4.6 (Amazon Q)
**File:** `.agent/skills/factory/context_refiner.py`
**Priority:** 2 of 7
**Effort:** ~30 lines changed

---

## Problem

`context_refiner.py` currently sends the entire first 3000 characters of a
markdown file to the LLM and asks it to rewrite the whole thing. This means:

- ~3000 tokens IN per file (mostly technical steps and code blocks the LLM is told not to change)
- Full file rewrite OUT (high risk of corrupting code blocks and terminal commands)
- For 24 files per build × 5 industries = 120 expensive, risky full-rewrites

The LLM only needs to rewrite 2 sections: **Introduction** and **Business Value**.
Everything else must stay identical.

---

## Instructions for Amazon Q

Open the file: `.agent/skills/factory/context_refiner.py`

### Change 1 — Add `extract_target_sections(content)` function

Add before `refine_markdown`. This function must:

1. Parse the markdown content line by line
2. Identify heading lines (lines starting with `#`, `##`, `###`)
3. Extract the full text block under headings that match these keywords
   (case-insensitive): `introduction`, `business value`, `overview`, `why this matters`
4. Return a list of dicts: `[{ "heading": "## Introduction", "body": "...text..." }]`
5. If no matching sections are found, return an empty list

### Change 2 — Add `patch_sections(original_content, refined_sections)` function

Add after the extractor. This function must:

1. Take the original full markdown content
2. Take a list of `{ "heading": ..., "body": ... }` dicts (refined sections)
3. For each refined section, find the original heading in the content
4. Replace only the text block under that heading with the refined version
5. Stop replacing when it hits the next heading of equal or higher level
6. Return the full patched markdown content
7. If patching fails for any section, return the original content unchanged (safe fallback)

### Change 3 — Add `parse_refined_sections(llm_response)` function

This parses the LLM's structured response:

1. Split response on `## SECTION:` markers
2. Extract heading and body for each block
3. Return list of `{ "heading": ..., "body": ... }` dicts
4. Return empty list if parsing fails

### Change 4 — Rewrite `refine_markdown` to use all new functions

New flow:
1. Call `extract_target_sections(content)` — get only sections to refine
2. If no sections found: log warning, return without LLM call (zero tokens spent)
3. Build compact prompt with ONLY extracted sections (not 3000 chars of full file)
4. Prompt format:
```
You are a technical curriculum expert rewriting sections for the {industry_name} industry.

Rewrite each section below. Rules:
1. Replace generic analogies with {industry_name}-specific ones
2. Keep all technical terms, commands, and code references identical
3. Match the tone and vocabulary of {industry_name} professionals
4. Return ONLY the rewritten sections in this exact format:
   ## SECTION: <original heading>
   <rewritten body>
   ## END_SECTION

Sections to rewrite:
{extracted_sections_text}
```
5. Call LLM with compact prompt
6. Call `parse_refined_sections(llm_response)`
7. Call `patch_sections(original_content, refined_sections)`
8. Write patched content back to file

### Change 5 — Do NOT change

- Function signature: `refine_markdown(file_path, industry_name, industry_slug)`
- The `if __name__ == "__main__"` block
- The safety check (only write if output contains `#` headings)

---

## TESTING PLAN

### Pre-conditions (verify before running any test)

```bash
# 1. Confirm Plan 01 is complete (data_synth uses industry arg)
grep -c "Retail" .agent/skills/factory/data_synth.py
# Expected: 0

# 2. Confirm Ollama is running
curl -s http://localhost:11434/api/tags | python3 -c "import sys,json; d=json.load(sys.stdin); print('Ollama OK:', len(d['models']), 'models')"
# Expected: Ollama OK: N models

# 3. Confirm a real built .md file exists to test against
ls dist/ai_for_global_finance/01_data_pipeline_automation/README.md 2>/dev/null || \
ls dist/ai_for_cyber-security/01_data_pipeline_automation/README.md 2>/dev/null || \
echo "No dist .md found — run a quick compile pass first"
```

If no `.md` file exists in dist, run a minimal build to get a test target:
```bash
python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local
```

---

### Test 1 — New functions exist in the file

```bash
grep -n "def extract_target_sections\|def patch_sections\|def parse_refined_sections" \
  .agent/skills/factory/context_refiner.py
```

**Expected result:** All 3 function definitions appear, each on its own line.

**Fail condition:** Any function missing → implementation is incomplete.

---

### Test 2 — Section extractor finds Introduction section

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.agent/skills/factory')
from context_refiner import extract_target_sections

# Create a test markdown with known sections
test_md = """# Lab Manual

## Introduction
This is a generic introduction about finance and banking.
It uses generic analogies that need replacing.

## Prerequisites
- Python 3.9+
- Ollama installed

## Business Value
This lab demonstrates business value through generic enterprise examples.

## Step 1: Setup
Run the following commands to get started.
"""

sections = extract_target_sections(test_md)
print(f"Found {len(sections)} sections")
for s in sections:
    print(f"  - Heading: {s['heading']}")
    print(f"    Body preview: {s['body'][:60]}...")

assert len(sections) >= 2, f"FAIL: Expected 2 sections, got {len(sections)}"
assert any("Introduction" in s['heading'] for s in sections), "FAIL: Introduction not found"
assert any("Business Value" in s['heading'] for s in sections), "FAIL: Business Value not found"
print("PASS: Section extractor works correctly")
EOF
```

**Expected result:** `PASS: Section extractor works correctly`

---

### Test 3 — Patch sections restores full file with replacements

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.agent/skills/factory')
from context_refiner import extract_target_sections, patch_sections

original = """# Lab Manual

## Introduction
This is a generic introduction about finance and banking.

## Prerequisites
- Python 3.9+

## Business Value
Generic enterprise business value statement.

## Step 1: Setup
Run commands here.
"""

refined_sections = [
    {"heading": "## Introduction", "body": "This is a cyber-security focused introduction about threat detection."},
    {"heading": "## Business Value", "body": "Cyber-security teams save millions by detecting intrusions early."}
]

patched = patch_sections(original, refined_sections)

# Verify technical sections are untouched
assert "## Prerequisites" in patched, "FAIL: Prerequisites section missing"
assert "Python 3.9+" in patched, "FAIL: Prerequisites content corrupted"
assert "## Step 1: Setup" in patched, "FAIL: Step 1 section missing"
assert "Run commands here." in patched, "FAIL: Step 1 content corrupted"

# Verify refined content is present
assert "cyber-security focused introduction" in patched, "FAIL: Refined intro not patched in"
assert "Cyber-security teams save millions" in patched, "FAIL: Refined business value not patched in"

# Verify old content is gone
assert "generic introduction about finance" not in patched, "FAIL: Old intro content still present"
print("PASS: Patch sections works correctly")
print(f"Patched file length: {len(patched)} chars (original: {len(original)} chars)")
EOF
```

**Expected result:** `PASS: Patch sections works correctly`

---

### Test 4 — Files with no target sections are skipped (zero LLM calls)

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.agent/skills/factory')
from context_refiner import extract_target_sections

# Markdown with NO Introduction or Business Value headings
test_md = """# Lab Manual

## Prerequisites
- Python 3.9+

## Step 1: Install
Run pip install

## Step 2: Configure
Edit config.yaml
"""

sections = extract_target_sections(test_md)
print(f"Sections found: {len(sections)}")
assert len(sections) == 0, f"FAIL: Expected 0 sections, got {len(sections)}"
print("PASS: Files without target sections correctly return empty list (no LLM call will be made)")
EOF
```

**Expected result:** `PASS: Files without target sections correctly return empty list`

---

### Test 5 — Live end-to-end refinement on a real file

Pick a real markdown file from a build:
```bash
# Make a backup first
cp dist/ai_for_global_finance/01_data_pipeline_automation/README.md /tmp/readme_backup.md

# Run refiner for a different industry
python3 .agent/skills/factory/context_refiner.py \
  dist/ai_for_global_finance/01_data_pipeline_automation/README.md \
  "AI for Cyber-Security" \
  ai_for_cyber_security
```

**Expected terminal output:**
- `✨ Refining analogies in README.md for AI for Cyber-Security...`
- `✅ Refined README.md`
- No Python errors

**Then verify surgical patch (code blocks untouched):**
```bash
python3 - <<'EOF'
with open("dist/ai_for_global_finance/01_data_pipeline_automation/README.md") as f:
    refined = f.read()
with open("/tmp/readme_backup.md") as f:
    original = f.read()

# Code blocks must be identical
import re
orig_code = re.findall(r'```[\s\S]*?```', original)
ref_code = re.findall(r'```[\s\S]*?```', refined)

print(f"Original code blocks: {len(orig_code)}")
print(f"Refined code blocks: {len(ref_code)}")
assert len(orig_code) == len(ref_code), "FAIL: Code block count changed"

for i, (o, r) in enumerate(zip(orig_code, ref_code)):
    assert o == r, f"FAIL: Code block {i+1} was modified"

print("PASS: All code blocks preserved intact")
print(f"File length change: {len(original)} -> {len(refined)} chars")
EOF
```

**Expected result:** `PASS: All code blocks preserved intact`

---

### Test 6 — Token count is reduced vs original approach

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.agent/skills/factory')
from context_refiner import extract_target_sections

with open("dist/ai_for_global_finance/01_data_pipeline_automation/README.md") as f:
    content = f.read()

# Old approach: first 3000 chars
old_tokens = len(content[:3000]) // 4
print(f"Old approach tokens (estimate): {old_tokens}")

# New approach: extracted sections only
sections = extract_target_sections(content)
extracted_text = "\n".join(s['heading'] + "\n" + s['body'] for s in sections)
new_tokens = len(extracted_text) // 4
print(f"New approach tokens (estimate): {new_tokens}")

if len(sections) > 0:
    reduction = (1 - new_tokens/old_tokens) * 100
    print(f"Token reduction: {reduction:.0f}%")
    assert new_tokens < old_tokens, "FAIL: New approach uses more tokens than old"
    print("PASS: Token reduction confirmed")
else:
    print("INFO: No target sections found in this file — LLM call skipped entirely (100% savings)")
EOF
```

**Expected result:** Token reduction of 50-90% shown, or "LLM call skipped entirely"

---

### Restore backup after testing

```bash
cp /tmp/readme_backup.md dist/ai_for_global_finance/01_data_pipeline_automation/README.md
echo "Backup restored"
```

---

### PHASE 2 PASS CRITERIA

All tests must pass before moving to Plan 03:

| Test | Check | Status |
|---|---|---|
| Pre-conditions | Ollama running, Plan 01 done, .md file exists | ☐ |
| Test 1 | All 3 new functions exist in file | ☐ |
| Test 2 | Section extractor finds Introduction + Business Value | ☐ |
| Test 3 | Patch sections preserves code blocks and technical content | ☐ |
| Test 4 | Files with no target sections return empty (skip LLM) | ☐ |
| Test 5 | Live refinement runs, code blocks untouched | ☐ |
| Test 6 | Token count reduced vs old approach | ☐ |

**If all pass:** Proceed to Plan 03.
**If any fail:** Fix the failing function and re-run that specific test only.
