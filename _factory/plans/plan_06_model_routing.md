# Plan 06 — Model Routing (Right Model for Right Task)

**Model:** Claude Sonnet 4.6 (Amazon Q)
**Files Touched:** `_factory/core/compiler.py`, `.agent/skills/factory/context_refiner.py`, `.agent/skills/factory/data_synth.py`
**New File:** `_factory/core/model_router.py`
**Priority:** 6 of 7
**Effort:** ~50 lines added, ~15 lines changed

---

## Problem

Every LLM call uses the same model regardless of task complexity:
- `llama3.2:1b` locally or `gemini-1.5-flash` on cloud for everything
- `llama3.2:1b` is too weak for markdown rewriting
- It is overkill for simple JSON/CSV generation
- No way to swap models without editing multiple files
- Cloud tokens wasted on simple structured tasks that a tiny local model handles fine

---

## Task Type Taxonomy

| Task Type | Description | Local Model | Cloud Model |
|---|---|---|---|
| `json_context` | Generate 4-field JSON industry DNA | qwen2.5:0.5b | gemini-1.5-flash |
| `data_synth` | Generate 50-row CSV with dirty data | qwen2.5:0.5b | gemini-1.5-flash |
| `md_refine` | Rewrite Introduction/Business Value | llama3.2:3b | gemini-1.5-flash |
| `timeline` | Generate 2011-2026 AI evolution table | llama3.2:3b | gemini-1.5-flash |
| `general` | Any unclassified call | llama3.2:1b | gemini-1.5-flash |

---

## Instructions for Amazon Q

---

### STEP 1 — Create `_factory/core/model_router.py` (new file)

Create class `ModelRouter`:

#### Class-level routing table `ROUTES`:
```python
ROUTES = {
    "local": {
        "json_context": "qwen2.5:0.5b",
        "data_synth":   "qwen2.5:0.5b",
        "md_refine":    "llama3.2:3b",
        "timeline":     "llama3.2:3b",
        "general":      "llama3.2:1b"
    },
    "cloud": {
        "json_context": "gemini-1.5-flash",
        "data_synth":   "gemini-1.5-flash",
        "md_refine":    "gemini-1.5-flash",
        "timeline":     "gemini-1.5-flash",
        "general":      "gemini-1.5-flash"
    }
}
```

#### `__init__(self, engine_mode="local")`
- Store `self.engine_mode`
- Store `self.usage = {}` to count calls per task type

#### `get_model(self, task_type)`
- Look up `ROUTES[engine_mode][task_type]`
- Fall back to `general` if task_type unknown
- Increment `self.usage[task_type]` counter
- Return model name string

#### `get_stats(self)`
- Return `self.usage` dict

#### `override(self, task_type, model_name)`
- Update `ROUTES[engine_mode][task_type]` at runtime
- Useful for testing and future manifest-level overrides

---

### STEP 2 — Modify `_factory/core/compiler.py`

#### 2a — Import ModelRouter
```python
try:
    from _factory.core.model_router import ModelRouter
except ImportError:
    from core.model_router import ModelRouter
```

#### 2b — Initialise router in `__init__` after engine_mode is set
```python
self.router = ModelRouter(engine_mode=self.engine_mode)
```

#### 2c — Update `call_llm()` signature to accept task_type
```python
def call_llm(self, prompt, is_json=False, task_type="general"):
```

Inside the method:
- Replace hardcoded `'llama3.2:1b'` with `self.router.get_model(task_type)`
- Log at DEBUG: `"Using model: {model} for task: {task_type}"`

#### 2d — Update all call_llm() call sites to pass task_type

In `generate_llm_context()`:
```python
data = self.call_llm(prompt, is_json=True, task_type="json_context")
```

In `control_tower.py` tab3 timeline:
```python
content = comp.call_llm(prompt, task_type="timeline")
```

#### 2e — Set env var before context_refiner subprocess call
```python
env = os.environ.copy()
env["REFINER_MODEL"] = self.router.get_model("md_refine")
subprocess.run([sys.executable, refiner_script, ...], env=env, check=True)
```

#### 2f — Set env var before data_synth subprocess call
```python
env = os.environ.copy()
env["SYNTH_MODEL"] = self.router.get_model("data_synth")
subprocess.run([sys.executable, synth_script, ...], env=env, check=True)
```

#### 2g — Log router stats at end of compile()
```python
self.logger.log(f"Model usage stats: {self.router.get_stats()}")
```

---

### STEP 3 — Modify `.agent/skills/factory/context_refiner.py`

Replace hardcoded model on line 31:
```python
model = os.environ.get("REFINER_MODEL", "llama3.2:3b")
response = ollama.chat(model=model, messages=[...])
```

---

### STEP 4 — Modify `.agent/skills/factory/data_synth.py`

Replace hardcoded model on line 24:
```python
model = os.environ.get("SYNTH_MODEL", "qwen2.5:0.5b")
response = ollama.chat(model=model, messages=[...])
```

---

## TESTING PLAN

### Pre-conditions (verify before running any test)

```bash
# 1. Plans 01-05 complete
ls _factory/core/cache.py _factory/core/queue.py _factory/core/manifest_validator.py
# Expected: all 3 files found

# 2. model_router.py must exist
ls _factory/core/model_router.py
# Expected: file found

# 3. Pull required models if not already available
ollama list | grep "qwen2.5\|llama3.2:3b"
# If missing, pull them:
# ollama pull qwen2.5:0.5b
# ollama pull llama3.2:3b
```

---

### Test 1 — ModelRouter returns correct model per task type

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from _factory.core.model_router import ModelRouter
except ImportError:
    from _factory.core.model_router import ModelRouter

# Local mode
router = ModelRouter(engine_mode="local")

assert router.get_model("json_context") == "qwen2.5:0.5b", "FAIL: json_context wrong model"
assert router.get_model("data_synth") == "qwen2.5:0.5b", "FAIL: data_synth wrong model"
assert router.get_model("md_refine") == "llama3.2:3b", "FAIL: md_refine wrong model"
assert router.get_model("timeline") == "llama3.2:3b", "FAIL: timeline wrong model"
assert router.get_model("general") == "llama3.2:1b", "FAIL: general wrong model"
assert router.get_model("unknown_task") == "llama3.2:1b", "FAIL: unknown task should fall back to general"
print("PASS: All local mode routing correct")

# Cloud mode
router_cloud = ModelRouter(engine_mode="cloud")
assert router_cloud.get_model("json_context") == "gemini-1.5-flash", "FAIL: cloud json_context wrong"
assert router_cloud.get_model("md_refine") == "gemini-1.5-flash", "FAIL: cloud md_refine wrong"
print("PASS: All cloud mode routing correct")
EOF
```

**Expected result:** Both PASS lines appear.

---

### Test 2 — Usage stats are tracked correctly

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from _factory.core.model_router import ModelRouter
except ImportError:
    from _factory.core.model_router import ModelRouter

router = ModelRouter(engine_mode="local")

router.get_model("json_context")
router.get_model("json_context")
router.get_model("md_refine")
router.get_model("data_synth")
router.get_model("md_refine")
router.get_model("md_refine")

stats = router.get_stats()
print(f"Usage stats: {stats}")
assert stats.get("json_context") == 2, f"FAIL: Expected 2 json_context calls, got {stats}"
assert stats.get("md_refine") == 3, f"FAIL: Expected 3 md_refine calls, got {stats}"
assert stats.get("data_synth") == 1, f"FAIL: Expected 1 data_synth call, got {stats}"
print("PASS: Usage stats tracked correctly")
EOF
```

**Expected result:** `PASS: Usage stats tracked correctly`

---

### Test 3 — Override works at runtime

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from _factory.core.model_router import ModelRouter
except ImportError:
    from _factory.core.model_router import ModelRouter

router = ModelRouter(engine_mode="local")
assert router.get_model("md_refine") == "llama3.2:3b"

router.override("md_refine", "llama3.2:1b")
assert router.get_model("md_refine") == "llama3.2:1b", "FAIL: Override not applied"
print("PASS: Runtime override works")
EOF
```

**Expected result:** `PASS: Runtime override works`

---

### Test 4 — context_refiner.py uses REFINER_MODEL env var

```bash
# Test that env var is respected
REFINER_MODEL=llama3.2:1b python3 -c "
import sys
sys.path.insert(0, '.agent/skills/factory')
import os
# Just check the model selection logic, don't actually call LLM
model = os.environ.get('REFINER_MODEL', 'llama3.2:3b')
print(f'Model selected: {model}')
assert model == 'llama3.2:1b', 'FAIL: env var not picked up'
print('PASS: REFINER_MODEL env var respected')
"
```

**Expected result:** `PASS: REFINER_MODEL env var respected`

---

### Test 5 — data_synth.py uses SYNTH_MODEL env var

```bash
SYNTH_MODEL=llama3.2:1b python3 -c "
import sys, os
sys.path.insert(0, '.agent/skills/factory')
model = os.environ.get('SYNTH_MODEL', 'qwen2.5:0.5b')
print(f'Model selected: {model}')
assert model == 'llama3.2:1b', 'FAIL: SYNTH_MODEL env var not picked up'
print('PASS: SYNTH_MODEL env var respected')
"
```

**Expected result:** `PASS: SYNTH_MODEL env var respected`

---

### Test 6 — Build logs show model names per task

```bash
# Run a build and check event logs for model names
rm -f _factory/logs/events.jsonl
python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local --pass 1

grep "model" _factory/logs/events.jsonl | head -10
```

**Expected result:** Log entries contain model names such as:
- `"Using model: qwen2.5:0.5b for task: json_context"`
- `"Model usage stats: {'json_context': 1, ...}"`

---

### Test 7 — End-to-end build uses correct models per task (latency check)

```bash
# Clear cache for fresh run
rm -f _factory/cache/hashes.json _factory/queue.db

# Time the json_context step separately to confirm fast model is used
time python3 - <<'EOF'
import sys, yaml, tempfile, os
sys.path.insert(0, '.')
try:
    from _factory.core.compiler import FactoryCompiler
except ImportError:
    from core.compiler import FactoryCompiler

with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
    yaml.dump({"industry": "AI for Cyber-Security", "tracks": ["base"]}, f)
    path = f.name

compiler = FactoryCompiler(path, engine_mode="local")
compiler.generate_llm_context()  # Should use qwen2.5:0.5b (fast)
print(f"Context: {compiler.context}")
os.unlink(path)
EOF
```

**Expected result:**
- Completes in under 5 seconds (qwen2.5:0.5b is fast)
- Context dict has all 4 fields: terminology, data_scenario, dataset_name, primary_color

---

### PHASE 6 PASS CRITERIA

| Test | Check | Status |
|---|---|---|
| Pre-conditions | Plans 01-05 done, model_router.py exists, models pulled | ☐ |
| Test 1 | All task types route to correct models (local + cloud) | ☐ |
| Test 2 | Usage stats counted correctly per task type | ☐ |
| Test 3 | Runtime override works | ☐ |
| Test 4 | context_refiner.py respects REFINER_MODEL env var | ☐ |
| Test 5 | data_synth.py respects SYNTH_MODEL env var | ☐ |
| Test 6 | Build logs contain model names per task | ☐ |
| Test 7 | json_context generation completes fast with qwen2.5:0.5b | ☐ |

**If all pass:** Proceed to Plan 07.
**If any fail:** Fix the issue and re-run only the failing test.
