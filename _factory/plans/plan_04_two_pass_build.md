# Plan 04 — Two-Pass Build (Static First, LLM Deferred)

**Model:** Claude Sonnet 4.6 (Amazon Q)
**Files Touched:** `_factory/core/compiler.py`, `_factory/factory_compiler.py`
**New File:** `_factory/core/queue.py`
**Priority:** 4 of 7
**Effort:** ~80 lines added, ~20 lines changed

---

## Problem

The current `compile()` method is a single blocking loop. For every `.md` file it:
1. Renders the Jinja2 template (fast, < 1ms)
2. Immediately calls `context_refiner.py` via subprocess (slow, 5-30 sec per file)

This means:
- User waits 3-5 minutes before seeing ANY output
- If the process is interrupted mid-way, partial builds are unusable
- LLM refinement and static rendering are tightly coupled
- No visibility into what is happening until it is all done

---

## Solution: Two-Pass Architecture

**Pass 1 — Static Render (< 5 seconds)**
- Jinja2 renders ALL templates to dist/
- No LLM calls at all
- Build is immediately usable with variable substitution complete
- Refinement jobs are queued in a SQLite database

**Pass 2 — LLM Refinement Queue (background, resumable)**
- Drains the SQLite queue file by file
- Each job: read file → extract sections → call LLM → patch file → mark done
- If interrupted: resumes from last incomplete job on next run

---

## Instructions for Amazon Q

---

### STEP 1 — Create `_factory/core/queue.py` (new file)

Create class `RefinementQueue` backed by SQLite using Python's built-in `sqlite3`.

#### Database schema:
```sql
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    industry_slug TEXT NOT NULL,
    file_path TEXT NOT NULL,
    industry_name TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TEXT,
    completed_at TEXT,
    error TEXT
)
```

Status values: `pending`, `in_progress`, `done`, `failed`

#### Methods:

**`__init__(self, db_path="_factory/queue.db")`**
- Connect to SQLite at db_path
- Create jobs table if not exists
- Set `self.conn` and `self.db_path`

**`enqueue(self, industry_slug, file_path, industry_name)`**
- Insert new `pending` job with `created_at` timestamp
- Skip if identical `(industry_slug, file_path)` already exists with status `pending` or `in_progress`

**`next_job(self)`**
- Return oldest `pending` job as dict
- Return None if queue is empty

**`mark_in_progress(self, job_id)`** — update status to `in_progress`

**`mark_done(self, job_id)`** — update status to `done`, set `completed_at`

**`mark_failed(self, job_id, error_message)`** — update status to `failed`, store error

**`reset_to_pending(self, job_id)`** — reset status back to `pending`, clear error

**`pending_count(self)`** — return count of pending rows

**`stats(self)`** — return `{ "pending": N, "done": N, "failed": N, "total": N }`

**`clear_done(self)`** — delete all rows where status = `done`

---

### STEP 2 — Modify `_factory/core/compiler.py`

#### 2a — Import RefinementQueue at top of file
```python
try:
    from _factory.core.queue import RefinementQueue
except ImportError:
    from core.queue import RefinementQueue
```

#### 2b — Initialise queue in `__init__`
```python
self.refinement_queue = RefinementQueue()
```

#### 2c — Rename current `compile()` to `compile_pass1()`

In `compile_pass1()`:
- Keep all Jinja2 rendering logic exactly as-is
- REMOVE the `self.run_context_refiner(dest_path)` call
- REPLACE it with queue enqueue for .md files:
  ```python
  if file.endswith('.md'):
      self.refinement_queue.enqueue(self.slug, dest_path, self.industry)
      self.logger.log(f"Queued for refinement: {file}")
  ```
- Keep `generate_readme()` and `generate_build_tests()` at the end
- Add final log: `"Pass 1 complete. {N} files queued for LLM refinement."`

#### 2d — Add `compile_pass2(self)` method

Drain queue sequentially (async upgrade comes in Plan 07):
```
while True:
    job = self.refinement_queue.next_job()
    if job is None:
        break
    self.refinement_queue.mark_in_progress(job['id'])
    try:
        self.run_context_refiner(job['file_path'])
        self.refinement_queue.mark_done(job['id'])
        self.logger.log(f"Refined: {os.path.basename(job['file_path'])}")
    except Exception as e:
        self.refinement_queue.mark_failed(job['id'], str(e))
        self.logger.log(f"Refinement failed: {e}", level="WARNING")

self.refinement_queue.clear_done()
self.logger.log(f"Pass 2 complete. Stats: {self.refinement_queue.stats()}")
```

#### 2e — Add new `compile(self)` that calls both passes
```python
def compile(self):
    self.compile_pass1()
    self.compile_pass2()
```

---

### STEP 3 — Modify `_factory/factory_compiler.py`

Add `--pass` CLI argument:
- `--pass 1` → call `compiler.compile_pass1()` only
- `--pass 2` → call `compiler.compile_pass2()` only
- No flag → call `compiler.compile()` (both passes, backward compatible)

---

## Queue File Location

```
_factory/queue.db    ← gitignore this file
```

---

## TESTING PLAN

### Pre-conditions (verify before running any test)

```bash
# 1. Plans 01, 02, 03 must be complete
grep -c "Retail" .agent/skills/factory/data_synth.py  # Expected: 0
grep -c "def extract_target_sections" .agent/skills/factory/context_refiner.py  # Expected: 1
ls _factory/core/cache.py  # Expected: file found

# 2. queue.py must exist
ls _factory/core/queue.py
# Expected: file found

# 3. compiler.py must have compile_pass1 and compile_pass2
grep -c "def compile_pass1\|def compile_pass2" _factory/core/compiler.py
# Expected: 2
```

---

### Test 1 — RefinementQueue CRUD operations

```bash
python3 - <<'EOF'
import sys, os
sys.path.insert(0, '.')
try:
    from _factory.core.queue import RefinementQueue
except ImportError:
    from _factory.core.queue import RefinementQueue

q = RefinementQueue(db_path="/tmp/test_queue.db")

# Enqueue a job
q.enqueue("cyber_security", "/tmp/test_file.md", "AI for Cyber-Security")
assert q.pending_count() == 1, "FAIL: Expected 1 pending job"
print("PASS: enqueue works")

# Get next job
job = q.next_job()
assert job is not None, "FAIL: next_job returned None"
assert job["file_path"] == "/tmp/test_file.md", "FAIL: Wrong file path"
print(f"PASS: next_job returns correct job (id={job['id']})")

# Mark in progress
q.mark_in_progress(job["id"])
assert q.pending_count() == 0, "FAIL: Job still pending after mark_in_progress"
print("PASS: mark_in_progress works")

# Mark done
q.mark_done(job["id"])
stats = q.stats()
assert stats["done"] == 1, f"FAIL: Expected 1 done, got {stats}"
print(f"PASS: mark_done works. Stats: {stats}")

# Clear done
q.clear_done()
stats = q.stats()
assert stats["total"] == 0, f"FAIL: Expected 0 total after clear_done, got {stats}"
print("PASS: clear_done works")

# Deduplication check
q.enqueue("cyber_security", "/tmp/file_a.md", "AI for Cyber-Security")
q.enqueue("cyber_security", "/tmp/file_a.md", "AI for Cyber-Security")
assert q.pending_count() == 1, "FAIL: Duplicate job was allowed"
print("PASS: Duplicate enqueue prevented")

import os; os.unlink("/tmp/test_queue.db")
print("PASS: All RefinementQueue tests passed")
EOF
```

**Expected result:** All PASS lines appear.

---

### Test 2 — Pass 1 completes in under 10 seconds with no LLM calls

```bash
# Clear the queue
rm -f _factory/queue.db

# Run Pass 1 only and time it
time python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local --pass 1
```

**Expected result:**
- Completes in **under 10 seconds**
- Log shows `"Queued for refinement:"` lines for .md files
- Log shows `"Pass 1 complete. N files queued for LLM refinement."`
- Log does NOT show any `"Refining manual"` or `"Refined:"` lines
- `dist/ai_for_cyber-security/` exists with files rendered

**Verify files exist and Jinja2 substitution worked:**
```bash
grep -r "ai_for_cyber" dist/ai_for_cyber-security/ --include="*.md" -l | head -5
# Expected: several .md files listed (industry slug substituted correctly)

grep "{{ industry" dist/ai_for_cyber-security/README.md
# Expected: no output (no unrendered Jinja2 variables remain)
```

---

### Test 3 — Queue database has pending jobs after Pass 1

```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from _factory.core.queue import RefinementQueue
except ImportError:
    from _factory.core.queue import RefinementQueue

q = RefinementQueue()
stats = q.stats()
print(f"Queue stats: {stats}")
assert stats["pending"] > 0, f"FAIL: Expected pending jobs after Pass 1, got {stats}"
print(f"PASS: {stats['pending']} jobs queued and waiting for Pass 2")
EOF
```

**Expected result:** `PASS: N jobs queued and waiting for Pass 2`

---

### Test 4 — Pass 2 drains the queue

```bash
# Run Pass 2 only (drains the queue from Pass 1)
python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local --pass 2
```

**Expected result:**
- Log shows `"Refined:"` lines for each .md file
- Log shows `"Pass 2 complete. Stats: {'pending': 0, 'done': 0, ...}"`
- No Python errors

**Verify queue is empty after Pass 2:**
```bash
python3 - <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from _factory.core.queue import RefinementQueue
except ImportError:
    from _factory.core.queue import RefinementQueue

q = RefinementQueue()
stats = q.stats()
print(f"Queue stats after Pass 2: {stats}")
assert stats["pending"] == 0, f"FAIL: Still pending jobs after Pass 2: {stats}"
print("PASS: Queue fully drained after Pass 2")
EOF
```

---

### Test 5 — Interrupted Pass 2 resumes correctly

```bash
# Enqueue some test jobs manually
python3 - <<'EOF'
import sys
sys.path.insert(0, '.')
try:
    from _factory.core.queue import RefinementQueue
except ImportError:
    from _factory.core.queue import RefinementQueue

q = RefinementQueue()
# Simulate a job that was interrupted mid-progress
q.enqueue("cyber_security", "/tmp/fake_interrupted.md", "AI for Cyber-Security")
job = q.next_job()
q.mark_in_progress(job["id"])
# Don't mark done — simulating a crash mid-job

# Now reset to pending (this is what resume logic should handle)
q.reset_to_pending(job["id"])
print(f"Pending count after reset: {q.pending_count()}")
assert q.pending_count() == 1, "FAIL: Job not reset to pending"
print("PASS: Interrupted job correctly reset to pending for retry")
EOF
```

**Expected result:** `PASS: Interrupted job correctly reset to pending for retry`

---

### Test 6 — Full compile() (both passes) is backward compatible

```bash
# Clean state
rm -f _factory/queue.db
rm -f _factory/cache/hashes.json

# Run full compile with no --pass flag (original interface)
python3 _factory/factory_compiler.py _factory/manifests/cyber_security.yaml --mode local
```

**Expected result:**
- Pass 1 runs then Pass 2 runs automatically
- Final log shows both `"Pass 1 complete"` and `"Pass 2 complete"`
- `dist/ai_for_cyber-security/` fully built and refined
- No breaking change to existing workflow

---

### PHASE 4 PASS CRITERIA

| Test | Check | Status |
|---|---|---|
| Pre-conditions | Plans 01-03 done, queue.py exists, both pass methods in compiler | ☐ |
| Test 1 | All RefinementQueue CRUD operations work correctly | ☐ |
| Test 2 | Pass 1 only completes < 10 sec, no LLM calls, files rendered | ☐ |
| Test 3 | Queue DB has pending jobs after Pass 1 | ☐ |
| Test 4 | Pass 2 drains queue, zero pending jobs after completion | ☐ |
| Test 5 | Interrupted job resets to pending for retry | ☐ |
| Test 6 | Full compile() (no flag) is backward compatible | ☐ |

**If all pass:** Proceed to Plan 05.
**If any fail:** Fix the issue and re-run only the failing test.
