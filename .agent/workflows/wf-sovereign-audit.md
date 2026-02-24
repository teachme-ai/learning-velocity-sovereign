---
description: Quality Control — spins up a temporary Docker container, runs the Architect code, and generates a Pass/Fail report on local model performance.
---

# wf-sovereign-audit

Runs a local governance audit on the session's generated content and code. Requires:
- `session_folder` — the fully-named session directory to audit

## Steps

1. Verify that a `docker` daemon is running. If not, surface an error and stop.

2. Build a temporary audit container from the project's base `Dockerfile` (or a minimal Python-slim image if none exists):
   ```bash
   docker build -t sovereign-audit:tmp .
   ```

3. Mount the `{session_folder}/logic/` directory and run the `[ARCHITECT]` code inside the container:
   ```bash
   docker run --rm \
     -v "$(pwd)/{session_folder}/logic:/workspace" \
     sovereign-audit:tmp \
     python /workspace/run_audit.py
   ```

4. Collect stdout/stderr from the container run.

5. Generate a `audit_report.md` inside `{session_folder}/` with the following structure:

   ```markdown
   # Sovereign Audit Report — {session_folder}

   **Date:** {YYYY-MM-DD}
   **Verdict:** PASS | FAIL

   ## Checks
   | Check | Status | Notes |
   |---|---|---|
   | Docker build | ✅ / ❌ | |
   | Code execution | ✅ / ❌ | |
   | Output validation | ✅ / ❌ | |

   ## Raw Output
   \`\`\`
   {stdout}
   \`\`\`

   ## Errors (if any)
   \`\`\`
   {stderr}
   \`\`\`
   ```

6. Remove the temporary image:
   ```bash
   docker rmi sovereign-audit:tmp
   ```

7. Display the verdict and path to the report.
