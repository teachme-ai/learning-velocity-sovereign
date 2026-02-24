---
description: Material Build — triggers Nano Banana to generate slide visuals and five vertical-specific lab guides using the Golden Path logic.
---

# wf-content-factory

Generates all visual and written content for a given session. Requires:
- `session_folder` — the fully-named session directory (e.g. `01_sovereign_ai_foundations`)
- `topic_name`     — human-readable topic title for slide headings

## Steps

1. Open the session's `README.md` to extract the list of **Learning Outcomes** as the content scaffold.

2. Using **Nano Banana** with the `Cyber-Sovereign` theme, generate an architecture diagram for each major concept covered by the Learning Outcomes. Save outputs to:
   ```
   {session_folder}/assets/diagrams/
   ```

3. Generate five vertical-specific lab guide files inside `{session_folder}/prompts/`, one per enterprise vertical:
   - `lab_fintech.md`
   - `lab_healthtech.md`
   - `lab_govtech.md`
   - `lab_retailtech.md`
   - `lab_edtech.md`

   Each lab guide must use the Two-Track format:
   ```markdown
   ## [INTEGRATOR] Lab — {vertical}
   <!-- Integration tasks specific to this vertical -->

   ## [ARCHITECT] Lab — {vertical}
   <!-- Design tasks specific to this vertical -->
   ```

4. Validate that all generated files exist and report a checklist back to the user.
