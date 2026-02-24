---
name: Forensic Documentarian
description: 'Automated validation and visual documentation of lab notes.'
triggers:
  - 'validate labs'
  - 'sync docs'
  - 'update proof'
---

# Forensic Documentarian Skill

## Instructions
1. Run code blocks marked with `# [VALIDATE]`.
2. Compare the output against existing lab notes documentation.
3. Update the Markdown documentation if it is stale.
4. Capture screenshots using Playwright (for UI) or Rich (for terminal) to provide visual proof of validation.

## bundled scripts
- Use `scripts/sync_docs.py` to automate this process.
