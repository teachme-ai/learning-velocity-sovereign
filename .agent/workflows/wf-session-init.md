---
description: Structural Start — scaffold a new bootcamp session folder with standard subfolders and a boilerplate README.
---

# wf-session-init

Initialise a new bootcamp session. Requires two inputs:
- `session_number` — zero-padded integer, e.g. `01`
- `topic_name`     — snake_case topic label, e.g. `sovereign_ai_foundations`

## Steps

1. Derive the session folder name: `{session_number}_{topic_name}` (e.g. `01_sovereign_ai_foundations`).

2. Create the following directory structure inside the project root:
   ```
   {session_number}_{topic_name}/
   ├── README.md
   ├── prompts/
   └── logic/
   ```

3. Populate `README.md` with this boilerplate (substitute real values for placeholders):

   ```markdown
   # Session {session_number}: {topic_name}

   ## Overview
   <!-- One-paragraph summary of what this session covers. -->

   ## Learning Outcomes
   - [ ] Outcome 1
   - [ ] Outcome 2
   - [ ] Outcome 3

   ## [INTEGRATOR] Lab
   <!-- Step-by-step integration tasks for implementation-focused learners. -->

   ## [ARCHITECT] Lab
   <!-- Design & internals tasks for architecture-focused learners. -->

   ## Governance Notes
   <!-- Compliance, security, and enterprise governance considerations. -->
   ```

4. Confirm creation by listing the new directory tree back to the user.
