# Plan 05 — Manifest Schema Validation + token_budget + data_schema Fields

**Model:** Claude Sonnet 4.6 (Amazon Q)
**Files Touched:** `_factory/core/compiler.py`, `_factory/factory_compiler.py`, `.agent/skills/factory/data_synth.py`
**New File:** `_factory/core/manifest_validator.py`
**Priority:** 5 of 7
**Effort:** ~70 lines added, ~5 lines changed

---

## Problem

The current manifest is 2 fields with zero validation:
```yaml
industry: AI for Educators
tracks: [base]
```

This causes:
- No way to control how many tokens a build consumes
- No way to define industry-specific CSV columns (forcing data_synth.py to guess)
- Compiler starts a full build before discovering the manifest is broken
- No budget enforcement means a runaway build can burn unlimited tokens

---

## New Manifest Format

```yaml
# Required fields (unchanged)
industry: AI for Cyber-Security
tracks:
  - base
  - integrated
  - architect

# Optional: Token budget controls
token_budget:
  total_tokens: 50000
  tokens_per_minute: 500
  defer_after_tokens: 30000

# Optional: Data schema for data_synth.py
data_schema:
  columns:
    - log_id
    - timestamp
    - source_ip
    - destination_ip
    - event_type
    - severity
    - bytes_transferred
    - anomaly_flag
  dirty_rate: 0.15
  row_count: 50
```

All fields under `token_budget` and `data_schema` are optional.
If omitted, the system uses safe defaults.

---

## Instructions for Amazon Q

---

### STEP 1 — Create `_factory/core/manifest_validator.py` (new file)

Create class `ManifestValidator` with:

#### `DEFAULTS` class-level dict:
```python
DEFAULTS = {
    "tracks": ["base", "integrated", "architect"],
    "token_budget": {
        "total_tokens": 100000,
        "tokens_per_minute": 1000,
        "defer_after_tokens": 100000
    },
    "data_schema": {
        "columns": ["id", "date", "category", "value", "notes", "status"],
        "dirty_rate": 0.15,
        "row_count": 50
    }
}
```

#### `__init__(self, manifest_dict)`
- Store raw manifest as `self.raw`
- Set `self.errors = []` and `self.warnings = []`

#### `validate(self)`
- `industry` must exist and be non-empty string → error if missing
- `tracks` must be list with at least one of: `base`, `integrated`, `architect` → warning if missing, use default
- `token_budget` fields if present: all must be positive ints, `defer_after_tokens` <= `total_tokens` → error if invalid
- `data_schema` fields if present: `columns` non-empty list of strings, `dirty_rate` float 0.0-1.0, `row_count` int 10-500 → error if invalid
- Return `True` if `self.errors` is empty

#### `get_merged(self)`
- Deep merge `self.raw` with `DEFAULTS` (user values override defaults)
- Return merged dict — compiler always uses this, never raw

#### `report(self)`
- Return formatted string listing all errors and warnings

---

### STEP 2 — Modify `_factory/core/compiler.py`

#### 2a — Import ManifestValidator
```python
try:
    from _factory.core.manifest_validator import ManifestValidator
except ImportError:
    from core.manifest_validator import ManifestValidator
```

#### 2b — Replace manifest loading in `__init__` (lines 39-40)
```python
with open(manifest_path, 'r') as f:
    raw_manifest = yaml.safe_load(f)

validator = ManifestValidator(raw_manifest)
if not validator.validate():
    raise ValueError(f"Invalid manifest:\n{validator.report()}")
if validator.warnings:
    self.logger.log(f"Manifest warnings:\n{validator.report()}", level="WARNING")

self.manifest = validator.get_merged()
```

#### 2c — Expose token_budget and data_schema as instance attributes
```python
self.token_budget = self.manifest.get("token_budget")
self.data_schema = self.manifest.get("data_schema")
```

#### 2d — Pass data_schema to run_data_synth()
```python
columns = ",".join(self.data_schema["columns"])
dirty_rate = str(self.data_schema["dirty_rate"])
row_count = str(self.data_schema["row_count"])

subprocess.run([
    sys.executable, synth_script,
    self.slug, self.industry, columns, dirty_rate, row_count
], check=True)
```

---

### STEP 3 — Modify `.agent/skills/factory/data_synth.py`

Update function signature:
```python
def generate_dirty_data(slug, industry, columns=None, dirty_rate=0.15, row_count=50):
```

- If `columns` passed as comma-separated string: split into list and use in prompt
- If `columns` is None: let LLM choose (Plan 01 fallback behaviour preserved)
- Pass all three values into the prompt

Update `if __name__ == "__main__"` to accept optional argv:
- `sys.argv[1]` = slug
- `sys.argv[2]` = industry
- `sys.argv[3]` = columns (optional)
- `sys.argv[4]` = dirty_rate (optional)
- `sys.argv[5]` = row_count (optional)

---

## TESTING PLAN

### Pre-conditions (verify before running any test)

```bash
# 1. Plans 01-04 complete
grep -c "Retail" .agent/skills/factory/data_synth.py                     # Expected: 0
grep -c "def extract_target_sections" .agent/skills/factory/context_refiner.py  # Expected: 1
ls _factory/core/cache.py _factory/core/queue.py                         # Expected: both found

# 2. manifest_validator.py must exist
ls _factory/core/manifest_validator.py
# Expected: file found
```

---

### Test 1 — ManifestValidator rejects missing industry field

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from _factory.core.manifest_validator import ManifestValidator
except ImportError:
    from _factory.core.manifest_validator import ManifestValidator

# Missing industry
v = ManifestValidator({"tracks": ["base"]})
result = v.validate()
print(f"Validation result: {result}")
print(f"Errors: {v.errors}")
assert result == False, "FAIL: Validator should reject missing industry"
assert any("industry" in e.lower() for e in v.errors), "FAIL: Error message should mention 'industry'"
print("PASS: Missing industry correctly rejected")
EOF
```

**Expected result:** `PASS: Missing industry correctly rejected`

---

### Test 2 — ManifestValidator accepts valid manifest and fills defaults

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from _factory.core.manifest_validator import ManifestValidator
except ImportError:
    from _factory.core.manifest_validator import ManifestValidator

# Minimal valid manifest (no optional fields)
v = ManifestValidator({"industry": "AI for Finance"})
result = v.validate()
assert result == True, f"FAIL: Valid manifest rejected. Errors: {v.errors}"

merged = v.get_merged()
print(f"Merged manifest keys: {list(merged.keys())}")

# Check defaults were applied
assert "token_budget" in merged, "FAIL: token_budget default not applied"
assert "data_schema" in merged, "FAIL: data_schema default not applied"
assert merged["token_budget"]["total_tokens"] == 100000, "FAIL: Wrong default total_tokens"
assert merged["data_schema"]["dirty_rate"] == 0.15, "FAIL: Wrong default dirty_rate"
print(f"token_budget: {merged['token_budget']}")
print(f"data_schema columns: {merged['data_schema']['columns']}")
print("PASS: Valid manifest accepted with defaults filled in")
EOF
```

**Expected result:** `PASS: Valid manifest accepted with defaults filled in`

---

### Test 3 — User values override defaults

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from _factory.core.manifest_validator import ManifestValidator
except ImportError:
    from _factory.core.manifest_validator import ManifestValidator

manifest = {
    "industry": "AI for Cyber-Security",
    "tracks": ["base"],
    "token_budget": {
        "total_tokens": 25000,
        "tokens_per_minute": 200,
        "defer_after_tokens": 10000
    },
    "data_schema": {
        "columns": ["log_id", "timestamp", "source_ip", "severity"],
        "dirty_rate": 0.20,
        "row_count": 30
    }
}

v = ManifestValidator(manifest)
assert v.validate() == True, f"FAIL: Valid manifest rejected: {v.errors}"
merged = v.get_merged()

assert merged["token_budget"]["total_tokens"] == 25000, "FAIL: User value not preserved"
assert merged["data_schema"]["dirty_rate"] == 0.20, "FAIL: User dirty_rate not preserved"
assert merged["data_schema"]["columns"] == ["log_id", "timestamp", "source_ip", "severity"], "FAIL: User columns not preserved"
assert len(merged["tracks"]) == 1, "FAIL: User tracks not preserved"
print("PASS: User values correctly override defaults")
EOF
```

**Expected result:** `PASS: User values correctly override defaults`

---

### Test 4 — Invalid token_budget values are rejected

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from _factory.core.manifest_validator import ManifestValidator
except ImportError:
    from _factory.core.manifest_validator import ManifestValidator

# defer_after_tokens > total_tokens (invalid)
v = ManifestValidator({
    "industry": "Test",
    "token_budget": {"total_tokens": 1000, "tokens_per_minute": 100, "defer_after_tokens": 5000}
})
result = v.validate()
assert result == False, "FAIL: Should reject defer_after_tokens > total_tokens"
print(f"Errors: {v.errors}")
print("PASS: Invalid token_budget correctly rejected")

# Negative total_tokens (invalid)
v2 = ManifestValidator({
    "industry": "Test",
    "token_budget": {"total_tokens": -100, "tokens_per_minute": 100, "defer_after_tokens": 50}
})
result2 = v2.validate()
assert result2 == False, "FAIL: Should reject negative total_tokens"
print("PASS: Negative total_tokens correctly rejected")
EOF
```

**Expected result:** Both PASS lines appear.

---

### Test 5 — Compiler raises ValueError for invalid manifest

```bash
python3 - <<'EOF'
import yaml, tempfile, os, sys
sys.path.insert(0, '.')

# Write invalid manifest (missing industry)
bad_manifest = {"tracks": ["base"]}
with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
    yaml.dump(bad_manifest, f)
    path = f.name

try:
    try:
        from _factory.core.compiler import FactoryCompiler
    except ImportError:
        from core.compiler import FactoryCompiler
    compiler = FactoryCompiler(path)
    print("FAIL: Compiler should have raised ValueError for invalid manifest")
except ValueError as e:
    print(f"PASS: Compiler raised ValueError: {str(e)[:80]}...")
finally:
    os.unlink(path)
EOF
```

**Expected result:** `PASS: Compiler raised ValueError: ...`

---

### Test 6 — data_schema columns passed to data_synth and used in CSV

Add a manifest with explicit cyber-security columns and run a build:

```bash
cat > /tmp/test_cyber_schema.yaml << 'EOF'
industry: AI for Cyber-Security
tracks:
  - base
data_schema:
  columns:
    - log_id
    - timestamp
    - source_ip
    - destination_ip
    - event_type
    - severity
    - bytes_transferred
  dirty_rate: 0.20
  row_count: 30
EOF

python3 _factory/factory_compiler.py /tmp/test_cyber_schema.yaml --mode local --pass 1
```

**Then inspect the CSV:**
```bash
head -2 "_factory/templates/01_data_pipeline_automation/set_{{ industry_slug }}/data/dirty_data.csv"
```

**Expected result:**
- Header row contains the exact columns from the manifest: `log_id`, `timestamp`, `source_ip`, etc.
- Columns match what was specified, not generic defaults

---

### PHASE 5 PASS CRITERIA

| Test | Check | Status |
|---|---|---|
| Pre-conditions | Plans 01-04 done, manifest_validator.py exists | ☐ |
| Test 1 | Missing industry field rejected with clear error | ☐ |
| Test 2 | Valid minimal manifest accepted, defaults applied | ☐ |
| Test 3 | User values override defaults correctly | ☐ |
| Test 4 | Invalid token_budget values rejected | ☐ |
| Test 5 | Compiler raises ValueError for bad manifest before any build starts | ☐ |
| Test 6 | data_schema columns flow through to generated CSV | ☐ |

**If all pass:** Proceed to Plan 06.
**If any fail:** Fix the issue and re-run only the failing test.
