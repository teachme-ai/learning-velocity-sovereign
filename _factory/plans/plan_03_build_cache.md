# Plan 03 — Build Cache (SHA256 Hash Per File, Incremental Rebuilds)

**Model:** Claude Sonnet 4.6 (Amazon Q)
**Files Touched:** `_factory/core/compiler.py`, `_factory/factory_compiler.py`
**New File:** `_factory/core/cache.py`
**Priority:** 3 of 7
**Effort:** ~60 lines added, ~10 lines changed

---

## Problem

Every `compile()` run starts with `shutil.rmtree(self.build_dir)` — wiping
everything and rebuilding from scratch. This means:

- 24 LLM refinement calls fire every single run, even if nothing changed
- A 1-line template fix triggers a full 5-minute industry rebuild
- 5 industries × full rebuild = 120 LLM calls every time
- Zero ability to iterate cheaply during development

---

## Instructions for Amazon Q

---

### STEP 1 — Create `_factory/core/cache.py` (new file)

Create a single class `BuildCache` with these methods:

#### `__init__(self, cache_dir="_factory/cache")`
- Set `self.cache_file = {cache_dir}/hashes.json`
- Create cache_dir if it does not exist
- Load existing hashes from JSON file into `self.hashes` dict
- If file missing or corrupt: set `self.hashes = {}`

#### `_compute_hash(self, template_path, context)`
- Read raw template file content
- Serialise context dict to stable JSON string (sorted keys)
- Concatenate both strings
- Return SHA256 hex digest
- Same template + same context = same hash (cache hit)
- Either changes = new hash (cache miss)

#### `is_cached(self, rel_path, template_path, context)`
- Compute hash for this file+context
- Return `True` only if `self.hashes[rel_path]` matches computed hash
- Return `False` for any miss, new file, or error

#### `mark_cached(self, rel_path, template_path, context)`
- Store computed hash in `self.hashes[rel_path]`
- Do NOT write to disk yet (batched — save once at end of build)

#### `save(self)`
- Write `self.hashes` to `hashes.json` as formatted JSON
- Called once at end of compile(), not per file

#### `invalidate(self, rel_path=None)`
- If rel_path given: delete that single entry
- If None: clear all hashes (full cache bust)
- Call `save()` after

---

### STEP 2 — Modify `_factory/core/compiler.py`

#### 2a — Import BuildCache at top of file
Use the same try/except import pattern already in the file:
```python
try:
    from _factory.core.cache import BuildCache
except ImportError:
    from core.cache import BuildCache
```

#### 2b — Initialise cache in `__init__` after line 55
```python
self.cache = BuildCache()
```

#### 2c — Replace `shutil.rmtree` block in `compile()` (lines 141-143)
- Old: always wipe build_dir
- New: only create build_dir if it does not exist. If it exists, leave it.
- Add log: `"Incremental build: cache active for {self.industry}"`

#### 2d — Add cache check inside the file loop (after `dest_path` is computed)
Before the render block, add:
```
if self.cache.is_cached(rendered_rel_path, full_template_path, self.context):
    log DEBUG: "CACHE HIT: skipping {rendered_rel_path}"
    continue
```

#### 2e — Mark file cached after successful write
After `f.write(rendered)` succeeds, call:
```python
self.cache.mark_cached(rendered_rel_path, full_template_path, self.context)
```
Do NOT mark cached if an exception was caught — failed renders must always retry.

#### 2f — Save cache at end of `compile()`
After `self.generate_build_tests()`, add:
```python
self.cache.save()
self.logger.log(f"Cache saved: {len(self.cache.hashes)} entries indexed.")
```

---

### STEP 3 — Modify `_factory/factory_compiler.py`

Add `--force` CLI flag support:
- If `--force` in sys.argv: call `compiler.cache.invalidate()` before `compiler.compile()`
- Log: `"Force rebuild: cache cleared"`

---

## Cache File Location

```
_factory/cache/hashes.json
```

Add `_factory/cache/` to `.gitignore` — cache is machine-local, never committed.

---

## TESTING PLAN

### Pre-conditions (verify before running any test)

```bash
# 1. Plans 01 and 02 must be complete
grep -c "Retail" .agent/skills/factory/data_synth.py
# Expected: 0

grep -c "def extract_target_sections" .agent/skills/factory/context_refiner.py
# Expected: 1

# 2. cache.py must exist
ls _factory/core/cache.py
# Expected: file found

# 3. Ollama running
curl -s http://localhost:11434/api/tags > /dev/null && echo "Ollama OK"
```

---

### Test 1 — BuildCache class has all required methods

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from _factory.core.cache import BuildCache
except ImportError:
    from _factory.core.cache import BuildCache

cache = BuildCache(cache_dir="/tmp/test_cache")

# Verify all methods exist
assert hasattr(cache, 'is_cached'), "FAIL: is_cached missing"
assert hasattr(cache, 'mark_cached'), "FAIL: mark_cached missing"
assert hasattr(cache, 'save'), "FAIL: save missing"
assert hasattr(cache, 'invalidate'), "FAIL: invalidate missing"
assert hasattr(cache, '_compute_hash'), "FAIL: _compute_hash missing"

print("PASS: All BuildCache methods exist")
EOF
```

**Expected result:** `PASS: All BuildCache methods exist`

---

### Test 2 — Hash is consistent for same inputs, different for changed inputs

```bash
python3 - <<'EOF'
import tempfile, os, sys
sys.path.insert(0, '.')
try:
    from _factory.core.cache import BuildCache
except ImportError:
    from _factory.core.cache import BuildCache

cache = BuildCache(cache_dir="/tmp/test_cache")

# Write a temp template file
with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
    f.write("# Hello {{ industry_name }}")
    path = f.name

context = {"industry_name": "Finance", "industry_slug": "finance"}

hash1 = cache._compute_hash(path, context)
hash2 = cache._compute_hash(path, context)
assert hash1 == hash2, "FAIL: Same inputs produced different hashes"
print(f"PASS: Consistent hash for same inputs: {hash1[:16]}...")

# Change context
context2 = {"industry_name": "Healthcare", "industry_slug": "healthcare"}
hash3 = cache._compute_hash(path, context2)
assert hash1 != hash3, "FAIL: Different context produced same hash"
print(f"PASS: Different hash for different context: {hash3[:16]}...")

# Change file content
with open(path, 'w') as f:
    f.write("# Updated {{ industry_name }}")
hash4 = cache._compute_hash(path, context)
assert hash1 != hash4, "FAIL: Different file content produced same hash"
print(f"PASS: Different hash for changed file: {hash4[:16]}...")

os.unlink(path)
print("PASS: All hash consistency tests passed")
EOF
```

**Expected result:** All 3 PASS lines appear.

---

### Test 3 — Cache miss on first call, hit on second call

```bash
python3 - <<'EOF'
import tempfile, os, sys
sys.path.insert(0, '.')
try:
    from _factory.core.cache import BuildCache
except ImportError:
    from _factory.core.cache import BuildCache

cache = BuildCache(cache_dir="/tmp/test_cache_fresh")

with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
    f.write("# Hello {{ industry_name }}")
    path = f.name

context = {"industry_name": "Finance"}
rel = "session_01/README.md"

# First call — should be a miss
result = cache.is_cached(rel, path, context)
assert result == False, f"FAIL: Expected cache miss on first call, got hit"
print("PASS: Cache miss on first call (cold)")

# Mark it cached
cache.mark_cached(rel, path, context)

# Second call — should be a hit
result = cache.is_cached(rel, path, context)
assert result == True, f"FAIL: Expected cache hit after mark_cached, got miss"
print("PASS: Cache hit after mark_cached")

# Save and reload
cache.save()
cache2 = BuildCache(cache_dir="/tmp/test_cache_fresh")
result = cache2.is_cached(rel, path, context)
assert result == True, "FAIL: Cache hit lost after save+reload"
print("PASS: Cache persists across save and reload")

os.unlink(path)
import shutil; shutil.rmtree("/tmp/test_cache_fresh")
EOF
```

**Expected result:** All 3 PASS lines appear.

---

### Test 4 — Cold build populates cache

```bash
# Remove any existing cache
rm -f _factory/cache/hashes.json

# Time a full build
time python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local
```

**Expected result:**
- Build completes successfully
- `_factory/cache/hashes.json` now exists
- Log contains: `"Cache saved: N entries indexed"` where N > 0
- Inspect the file:

```bash
python3 -c "
import json
with open('_factory/cache/hashes.json') as f:
    h = json.load(f)
print(f'Cache entries: {len(h)}')
assert len(h) > 0, 'FAIL: Cache is empty after build'
print('PASS: Cache populated after cold build')
"
```

---

### Test 5 — Warm build skips all files (zero renders)

```bash
# Run the exact same build again immediately
time python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local
```

**Expected result:**
- Build completes in **under 10 seconds** (vs 3-5 minutes for cold build)
- Log shows `CACHE HIT: skipping ...` for every file
- Log does NOT show any `"Refining manual"` lines (no LLM calls)
- No files in dist/ were modified (check with git):

```bash
git diff --name-only dist/ai_for_cyber-security/
# Expected: no output (nothing changed)
```

---

### Test 6 — Changing one template busts only that file's cache

```bash
# Touch one template file to change its content
echo "" >> _factory/templates/01_data_pipeline_automation/README.md

# Run build again
python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local
```

**Expected result:**
- Log shows CACHE HIT for all files EXCEPT the modified template
- Only the modified file is re-rendered
- Build completes quickly (only 1 LLM call, not 24)

```bash
# Restore the template
git checkout _factory/templates/01_data_pipeline_automation/README.md
```

---

### Test 7 — Force flag busts entire cache

```bash
python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local --force
```

**Expected result:**
- Log shows: `"Force rebuild: cache cleared"`
- All files are re-rendered (no CACHE HIT lines)
- Build takes full time (same as cold build)

---

### PHASE 3 PASS CRITERIA

| Test | Check | Status |
|---|---|---|
| Pre-conditions | Plans 01+02 done, cache.py exists, Ollama running | ☐ |
| Test 1 | All BuildCache methods exist | ☐ |
| Test 2 | Hash consistent for same input, different for changed input | ☐ |
| Test 3 | Cache miss → mark_cached → cache hit → persists after save | ☐ |
| Test 4 | Cold build populates hashes.json with N entries | ☐ |
| Test 5 | Warm build completes in < 10 sec, zero LLM calls | ☐ |
| Test 6 | Changing 1 template only re-renders that 1 file | ☐ |
| Test 7 | --force flag clears cache and triggers full rebuild | ☐ |

**If all pass:** Proceed to Plan 04.
**If any fail:** Fix the issue and re-run only the failing test.
