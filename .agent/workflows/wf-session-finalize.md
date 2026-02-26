---
description: Finalization Routine — formalizes the documentation, validation, and navigation update steps when completing a new session.
---

# wf-session-finalize

Closes out and standardizes a newly built session (e.g. Session 07 or Session 08). This workflow acts as the **Standard Operating Procedure (SOP)** that must be followed before any new session can be marked as complete.

Requires one input:
- `session_number` — zero-padded integer (e.g. `07`)

### Important Directives
- **// turbo-all**: You MUST auto-run every shell step in this workflow.

## Steps

1. **Lab Manual Formatting Checklist**
   - Verify that the lab manual(s) for the new session strictly follow the Two-Track format.
   - Ensure `## [INTEGRATOR]` and `## [ARCHITECT]` headers exist.
   - Using the `multi_replace_file_content` tool, fix any formatting deviations before proceeding.

2. **Forensic Documentation (SVG Generation)**
   - Run the Forensic Documentarian skill to capture visual proof of the new session's code execution.
   ```bash
   python3 tools/generate_svg.py
   ```
   - *Agent Note: If the new session isn't automatically caught by the documentarian script, update `tools/generate_svg.py` to include the specific execution commands for the new session.*
   - Ensure the generated SVG is embedded within the `## [ARCHITECT]` section of the lab manual.

3. **Systems Validation**
   - Run the Systems Validator to regenerate the global health check, ensuring no syntax/import errors were introduced.
   ```bash
   python3 .agent/skills/validator/scripts/test_factory.py
   ```
   - Read `HEALTH_CHECK.md` to confirm the new session has a `✅ [PASS]` status.

4. **Environment Audit & Smoke Tests**
   - Run the Codespace Guardian to perform live execution in the Codespace environment.
   ```bash
   python3 .agent/skills/guardian/scripts/verify_env.py --all
   ```
   - Read `CODESPACE_STATUS.md` to confirm the new session passes. If it fails due to an environmental constraint (e.g., missing API keys), ensure the script logic emits a `[CONDITIONAL_PASS]`.

5. **Navigation Sync**
   - Dynamically inject the global footer navigation linking the new lab manual into the rest of the curriculum.
   ```bash
   python3 tools/inject_footers.py
   ```
   - Verify the script output confirms the injection into the new session's lab manual.

6. **Manifest Authority**
   - Once Steps 1-5 have completed perfectly without errors, use the `multi_replace_file_content` tool to edit `PROJECT_MANIFEST.md`.
   - Mark the new session across Sets A-E from `Architecting` to `✅ VALIDATED`.

7. **Report Status**
   - Format a concise summary for the User indicating that the session has cleared the Finalization Routine and is now officially live in the Master Manifest.
