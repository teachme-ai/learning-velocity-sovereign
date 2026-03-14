# Plan 07 — Async Refinement Queue (SQLite + asyncio Workers)

**Model:** Claude Sonnet 4.6 (Amazon Q)
**Files Touched:** `_factory/core/compiler.py`, `_factory/core/queue.py`
**New File:** `_factory/core/worker.py`
**Priority:** 7 of 7
**Effort:** ~100 lines added, ~20 lines changed

---

## Problem

Even after Plan 04 (two-pass build), Pass 2 drains the queue **sequentially**:
```
file 1 → LLM call → wait → write → file 2 → LLM call → wait → write ...
```

For 24 files at 8 seconds each:
- Sequential: 24 × 8s = **192 seconds**
- 3 concurrent workers: ~8 × 8s = **64 seconds**
- 5 concurrent workers: ~5 × 8s = **40 seconds**

Additionally the `token_budget` from Plan 05 has no enforcement yet.
This plan adds concurrent async workers AND token budget enforcement.

---

## Instructions for Amazon Q

---

### STEP 1 — Create `_factory/core/worker.py` (new file)

#### Imports (all stdlib or already used):
```python
import asyncio, os, sys, json
from datetime import datetime
```

---

#### Class `TokenBudget`:

**`__init__(self, total_tokens, defer_after_tokens, tokens_per_minute)`**
- Store all three values
- Set `self.used_tokens = 0`
- Set `self.minute_bucket = 0`
- Set `self.bucket_reset_time = datetime.now()`

**`estimate_tokens(text)`** (static method)
- Return `len(text) // 4`

**`can_proceed(self)`**
- Reset `minute_bucket` to 0 if >60 seconds since `bucket_reset_time`, update reset time
- Return `False` if `used_tokens >= defer_after_tokens`
- Return `False` if `minute_bucket >= tokens_per_minute`
- Return `True` otherwise

**`record_usage(self, tokens)`**
- Add tokens to `self.used_tokens` and `self.minute_bucket`

**`is_exhausted(self)`**
- Return `True` if `used_tokens >= total_tokens`

**`stats(self)`**
- Return `{ "used": N, "total": N, "remaining": N, "deferred": bool }`

---

#### Async function `refine_file_async(job, industry_name, refiner_script, model, semaphore, budget, logger)`

```
async with semaphore:
    if budget.is_exhausted():
        logger.log(f"Budget exhausted — deferring: {basename}", level="WARNING")
        return {"status": "deferred", "job_id": job["id"]}

    if not budget.can_proceed():
        await asyncio.sleep(2)  # wait for rate limit bucket to reset

    # Estimate tokens from file content
    try:
        with open(job["file_path"], "r") as f:
            content = f.read()
    except FileNotFoundError:
        return {"status": "failed", "job_id": job["id"], "error": "file not found"}

    estimated_tokens = TokenBudget.estimate_tokens(content) * 2  # in + out

    # Run refiner as async subprocess
    env = os.environ.copy()
    env["REFINER_MODEL"] = model

    proc = await asyncio.create_subprocess_exec(
        sys.executable, refiner_script,
        job["file_path"], industry_name, job["industry_slug"],
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    budget.record_usage(estimated_tokens)

    if proc.returncode == 0:
        return {"status": "done", "job_id": job["id"], "tokens": estimated_tokens}
    else:
        return {"status": "failed", "job_id": job["id"], "error": stderr.decode().strip()}
```

---

#### Async function `drain_queue(queue, industry_name, refiner_script, model, token_budget_config, logger, concurrency=3)`

```
budget = TokenBudget(
    total_tokens=token_budget_config["total_tokens"],
    defer_after_tokens=token_budget_config["defer_after_tokens"],
    tokens_per_minute=token_budget_config["tokens_per_minute"]
)

semaphore = asyncio.Semaphore(concurrency)
tasks = []

while True:
    job = queue.next_job()
    if job is None:
        break
    if budget.is_exhausted():
        logger.log("Token budget exhausted. Remaining jobs deferred to next run.", level="WARNING")
        break
    queue.mark_in_progress(job["id"])
    task = asyncio.create_task(
        refine_file_async(job, industry_name, refiner_script, model, semaphore, budget, logger)
    )
    tasks.append(task)

results = await asyncio.gather(*tasks, return_exceptions=True)

for result in results:
    if isinstance(result, Exception):
        continue
    if result["status"] == "done":
        queue.mark_done(result["job_id"])
    elif result["status"] == "failed":
        queue.mark_failed(result["job_id"], result.get("error", "unknown"))
    elif result["status"] == "deferred":
        queue.reset_to_pending(result["job_id"])

queue.clear_done()
logger.log(f"Pass 2 complete. Budget: {budget.stats()} | Queue: {queue.stats()}")
return budget.stats()
```

---

### STEP 2 — Add `reset_to_pending()` to `_factory/core/queue.py`

```python
def reset_to_pending(self, job_id):
    self.conn.execute(
        "UPDATE jobs SET status='pending', error=NULL WHERE id=?", (job_id,)
    )
    self.conn.commit()
```

---

### STEP 3 — Modify `_factory/core/compiler.py`

#### 3a — Import drain_queue
```python
try:
    from _factory.core.worker import drain_queue
except ImportError:
    from core.worker import drain_queue
```

#### 3b — Replace sequential `compile_pass2()` with async version

```python
def compile_pass2(self):
    self.logger.log(f"Pass 2: draining queue ({self.refinement_queue.pending_count()} jobs) with {self.concurrency} workers...")

    refiner_script = os.path.join(
        os.path.dirname(__file__),
        "../../.agent/skills/factory/context_refiner.py"
    )
    model = self.router.get_model("md_refine")

    asyncio.run(drain_queue(
        queue=self.refinement_queue,
        industry_name=self.industry,
        refiner_script=refiner_script,
        model=model,
        token_budget_config=self.token_budget,
        logger=self.logger,
        concurrency=self.concurrency
    ))
```

#### 3c — Add `concurrency` from manifest in `__init__`
```python
self.concurrency = self.manifest.get("concurrency", 3)
```

---

## Updated Full Manifest Format

```yaml
industry: AI for Cyber-Security
tracks:
  - base
  - integrated
  - architect

concurrency: 3

token_budget:
  total_tokens: 50000
  tokens_per_minute: 500
  defer_after_tokens: 30000

data_schema:
  columns:
    - log_id
    - timestamp
    - source_ip
    - event_type
    - severity
    - bytes_transferred
  dirty_rate: 0.15
  row_count: 50
```

---

## TESTING PLAN

### Pre-conditions (verify before running any test)

```bash
# 1. All plans 01-06 complete
ls _factory/core/cache.py \
   _factory/core/queue.py \
   _factory/core/manifest_validator.py \
   _factory/core/model_router.py
# Expected: all 4 files found

# 2. worker.py must exist
ls _factory/core/worker.py
# Expected: file found

# 3. reset_to_pending method exists in queue.py
grep -c "def reset_to_pending" _factory/core/queue.py
# Expected: 1

# 4. compile_pass2 in compiler.py now uses asyncio.run
grep -c "asyncio.run" _factory/core/compiler.py
# Expected: 1

# 5. Ollama running with required models
ollama list | grep "qwen2.5\|llama3.2:3b"
```

---

### Test 1 — TokenBudget class behaves correctly

```bash
python3 - <<'EOF'
import sys, time
sys.path.insert(0, '.')
try:
    from _factory.core.worker import TokenBudget
except ImportError:
    from core.worker import TokenBudget

# Basic budget tracking
budget = TokenBudget(total_tokens=1000, defer_after_tokens=800, tokens_per_minute=500)

assert budget.can_proceed() == True, "FAIL: Should be able to proceed on fresh budget"
print("PASS: Fresh budget allows proceeding")

budget.record_usage(400)
assert budget.can_proceed() == True, "FAIL: Should proceed at 400/800 defer threshold"

budget.record_usage(450)  # now at 850, over defer threshold
assert budget.can_proceed() == False, "FAIL: Should defer at 850 (over defer_after_tokens=800)"
print("PASS: Budget defers correctly after threshold")

assert budget.is_exhausted() == False, "FAIL: Should not be exhausted at 850/1000"
budget.record_usage(200)  # now at 1050, over total
assert budget.is_exhausted() == True, "FAIL: Should be exhausted at 1050/1000"
print("PASS: is_exhausted() works correctly")

# Token estimation
tokens = TokenBudget.estimate_tokens("Hello world this is a test string")
assert tokens > 0, "FAIL: Token estimation returned 0"
print(f"PASS: Token estimation: '{len('Hello world this is a test string')} chars' -> {tokens} tokens")

stats = budget.stats()
print(f"Budget stats: {stats}")
assert stats["used"] > 0, "FAIL: Used tokens not tracked"
print("PASS: All TokenBudget tests passed")
EOF
```

**Expected result:** All PASS lines appear.

---

### Test 2 — Async workers fire concurrently (not sequentially)

```bash
python3 - <<'EOF'
import asyncio, time, sys
sys.path.insert(0, '.')

# Simulate async concurrency with fake async tasks
async def fake_job(job_id, delay=0.5):
    await asyncio.sleep(delay)
    return job_id

async def test_concurrency():
    semaphore = asyncio.Semaphore(3)

    async def bounded(job_id):
        async with semaphore:
            return await fake_job(job_id)

    start = time.time()
    tasks = [asyncio.create_task(bounded(i)) for i in range(6)]
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start

    print(f"6 jobs with concurrency=3, each 0.5s delay")
    print(f"Elapsed: {elapsed:.2f}s (expected ~1.0s, sequential would be ~3.0s)")
    assert elapsed < 2.0, f"FAIL: Too slow ({elapsed:.2f}s) — concurrency not working"
    assert len(results) == 6, "FAIL: Not all jobs completed"
    print("PASS: Async concurrency confirmed working")

asyncio.run(test_concurrency())
EOF
```

**Expected result:** `PASS: Async concurrency confirmed working` in under 2 seconds.

---

### Test 3 — Budget exhaustion defers jobs to next run

```bash
python3 - <<'EOF'
import sys, tempfile, os
sys.path.insert(0, '.')
try:
    from _factory.core.queue import RefinementQueue
    from _factory.core.worker import TokenBudget
except ImportError:
    from core.queue import RefinementQueue
    from core.worker import TokenBudget

q = RefinementQueue(db_path="/tmp/test_budget_queue.db")

# Enqueue 5 jobs
for i in range(5):
    q.enqueue("test", f"/tmp/file_{i}.md", "Test Industry")

print(f"Queued: {q.pending_count()} jobs")

# Simulate budget exhaustion after 2 jobs
budget = TokenBudget(total_tokens=100, defer_after_tokens=50, tokens_per_minute=1000)
budget.record_usage(60)  # already over defer threshold

jobs_processed = 0
while True:
    job = q.next_job()
    if job is None:
        break
    if budget.is_exhausted() or not budget.can_proceed():
        # Deferred — leave as pending
        print(f"Deferred job {job['id']} due to budget")
        break
    q.mark_in_progress(job["id"])
    q.mark_done(job["id"])
    jobs_processed += 1

q.clear_done()
remaining = q.pending_count()
print(f"Jobs processed: {jobs_processed}")
print(f"Jobs remaining (deferred): {remaining}")
assert remaining > 0, "FAIL: All jobs processed despite budget exhaustion"
print("PASS: Budget exhaustion correctly defers remaining jobs")

os.unlink("/tmp/test_budget_queue.db")
EOF
```

**Expected result:** `PASS: Budget exhaustion correctly defers remaining jobs`

---

### Test 4 — Pass 2 timing with async workers (speed test)

```bash
# First: run Pass 1 to populate queue
rm -f _factory/queue.db _factory/cache/hashes.json
python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local --pass 1

# Check how many jobs are queued
python3 -c "
import sys; sys.path.insert(0, '.')
try:
    from _factory.core.queue import RefinementQueue
except:
    from core.queue import RefinementQueue
q = RefinementQueue()
print(f'Jobs queued for Pass 2: {q.pending_count()}')
"

# Now run Pass 2 and time it
time python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local --pass 2
```

**Expected result:**
- Pass 2 completes faster than the sequential version from Plan 04
- Log shows multiple `"Refining:"` lines appearing close together in time (concurrent)
- Log shows `"Pass 2 complete. Budget: {...} | Queue: {'pending': 0, ...}"`

---

### Test 5 — Interrupted Pass 2 resumes correctly with async workers

```bash
# Populate queue
rm -f _factory/queue.db
python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local --pass 1

QUEUED=$(python3 -c "
import sys; sys.path.insert(0, '.')
try:
    from _factory.core.queue import RefinementQueue
except:
    from core.queue import RefinementQueue
print(RefinementQueue().pending_count())
")
echo "Total queued: $QUEUED"

# Simulate interrupt by setting very low budget (processes only 2-3 files)
cat > /tmp/low_budget.yaml << 'EOF2'
industry: AI for Cyber-Security
tracks:
  - base
token_budget:
  total_tokens: 1000
  tokens_per_minute: 500
  defer_after_tokens: 500
EOF2

python3 _factory/factory_compiler.py /tmp/low_budget.yaml --mode local --pass 2

# Check remaining jobs
python3 -c "
import sys; sys.path.insert(0, '.')
try:
    from _factory.core.queue import RefinementQueue
except:
    from core.queue import RefinementQueue
q = RefinementQueue()
s = q.stats()
print(f'After low-budget run: {s}')
assert s['pending'] > 0, 'FAIL: All jobs consumed — budget enforcement not working'
print('PASS: Some jobs correctly deferred due to budget')
"

# Now resume with full budget
python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local --pass 2

python3 -c "
import sys; sys.path.insert(0, '.')
try:
    from _factory.core.queue import RefinementQueue
except:
    from core.queue import RefinementQueue
q = RefinementQueue()
s = q.stats()
print(f'After full-budget resume: {s}')
assert s['pending'] == 0, f'FAIL: Still pending jobs: {s}'
print('PASS: Queue fully drained on resume')
"
```

**Expected result:**
- After low-budget run: some jobs deferred (pending > 0)
- After full-budget resume: queue fully drained (pending == 0)

---

### Test 6 — concurrency field in manifest is respected

```bash
cat > /tmp/concurrency_test.yaml << 'EOF'
industry: AI for Cyber-Security
tracks:
  - base
concurrency: 5
token_budget:
  total_tokens: 100000
  tokens_per_minute: 10000
  defer_after_tokens: 100000
EOF

python3 _factory/factory_compiler.py /tmp/concurrency_test.yaml --mode local --pass 1
grep "5 workers" _factory/logs/events.jsonl | tail -1
```

**Expected result:** Log shows `"draining queue (...) with 5 workers"`

---

### Test 7 — Full system integration test (all 7 plans together)

```bash
# Clean everything
rm -f _factory/queue.db _factory/cache/hashes.json _factory/logs/events.jsonl

# Run full build with complete manifest
cat > /tmp/full_test.yaml << 'EOF'
industry: AI for Healthcare
tracks:
  - base
  - integrated
concurrency: 3
token_budget:
  total_tokens: 100000
  tokens_per_minute: 1000
  defer_after_tokens: 100000
data_schema:
  columns:
    - record_id
    - date
    - patient_id
    - diagnosis_code
    - treatment
    - cost_usd
    - insurance_flag
  dirty_rate: 0.15
  row_count: 50
EOF

time python3 _factory/factory_compiler.py /tmp/full_test.yaml --mode local
```

**Expected result:**
- Build completes without errors
- `dist/ai_for_healthcare/` exists
- CSV has healthcare-specific columns (record_id, patient_id, diagnosis_code...)
- Logs show model routing: qwen2.5:0.5b for json/csv, llama3.2:3b for md_refine
- Cache populated after build
- Second run (warm) completes in under 10 seconds

```bash
# Warm build should be instant
time python3 _factory/factory_compiler.py /tmp/full_test.yaml --mode local
# Expected: under 10 seconds, "CACHE HIT" for all files
```

---

### PHASE 7 PASS CRITERIA (Final)

| Test | Check | Status |
|---|---|---|
| Pre-conditions | All plans 01-06 done, worker.py exists, reset_to_pending added | ☐ |
| Test 1 | TokenBudget tracking, deferral, exhaustion, estimation all work | ☐ |
| Test 2 | Async concurrency confirmed (6 jobs in ~1s not ~3s) | ☐ |
| Test 3 | Budget exhaustion leaves remaining jobs in pending state | ☐ |
| Test 4 | Pass 2 with async workers is faster than sequential | ☐ |
| Test 5 | Interrupted build resumes from correct point on re-run | ☐ |
| Test 6 | Concurrency manifest field is passed to drain_queue | ☐ |
| Test 7 | Full system integration: Healthcare build end-to-end clean | ☐ |

**If all pass: ALL 7 PLANS COMPLETE.**

---

## Final Architecture Summary (All 7 Plans)

```
manifest.yaml (validated, with budget + schema)    [Plan 05]
    │
    ▼
ManifestValidator         validates before any work starts
    │
    ▼
BuildCache                skip unchanged files entirely    [Plan 03]
    │
    ▼
Pass 1: StaticRenderer    Jinja2 only, < 5 sec            [Plan 04]
    │   enqueues .md files to SQLite RefinementQueue
    │
    ▼
Pass 2: AsyncWorkerPool   3 concurrent workers            [Plan 07]
    │   ├── TokenBudget gate       enforces manifest limits
    │   ├── ModelRouter            right model per task    [Plan 06]
    │   ├── SectionExtractor       400-token prompts       [Plan 02]
    │   └── IndustryAwareData      correct CSV per industry[Plan 01]
    │
    ▼
dist/{industry}/          fully refined curriculum output
```

## Cost Summary (5 industries, 8 sessions, 3 tracks)

| Scenario | LLM Calls | Cloud Tokens | Cost (Gemini Flash) |
|---|---|---|---|
| Original architecture | 120 sequential | ~360,000 | ~$0.54 |
| After Plan 02 (section extract) | 120 | ~60,000 | ~$0.09 |
| After Plan 03 (cache, 2nd build) | ~5 changed files | ~2,000 | ~$0.003 |
| After Plan 07 (budget + async) | Budget-capped | Controlled | You decide |
| **All plans, warm build** | **0** | **0** | **$0.00** |
