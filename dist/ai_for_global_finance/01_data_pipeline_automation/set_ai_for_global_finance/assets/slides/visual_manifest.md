# 🎨 Visual Manifest — AI Bootcamps Prompt Bible
**Theme:** Cyber-Sovereign | **Palette:** Deep Navy/Slate · Neon Cyan · Electric Purple/Teal · Amber
**Generator:** `assets/diagrams/generate_visuals.py` (nano-banana first → Imagen fallback)

> **To regenerate any visual**, edit the prompt in `generate_visuals.py → SESSIONS` dict and run:
> ```bash
> cd "/Users/khalidirfan/projects/Ai Bootcamps"
> source ~/.zshrc
> 01_data_pipeline_automation/.venv/bin/python \
>   01_data_pipeline_automation/assets/diagrams/generate_visuals.py --session 01
> ```
> Replace `01` with `02`, `03`, or `all`.

---

## Session 01 — Data Pipeline Automation

### Infographic: Hybrid Sovereign Audit

**Status:** ✅ Rendered → `assets/diagrams/session_01_hybrid_audit.png` (Imagen 4.0, 2026-02-24)

**Concept:** Five-stage horizontal pipeline showing the hybrid Pydantic + Ollama LLM audit flow.

#### Prompt A — Slide/Infographic Mode (nano-banana)
> Used first. Includes explicit slide layout instructions for nano-banana's infographic generation mode.

```
SLIDE INFOGRAPHIC — Cyber-Sovereign Enterprise Theme.
Title slide panel: "Hybrid Sovereign Audit: Deterministic Rules + Probabilistic Intelligence"
Background: Deep navy (#0d0f1a). Accent colors: Neon Cyan (#00f5ff), Electric Purple (#a855f7), Amber (#f59e0b).

Layout: Horizontal left-to-right pipeline diagram with 5 connected stage boxes, glowing neon arrows between each.

Stage 1 box — "RAW DATA": dark slate, CSV file icon, caption "corporate_expenses.csv"
Stage 2 box — "PHASE 1: PYDANTIC": amber glow border, shield icon, subtitle "Deterministic Rules · Schema · $10k threshold"
Stage 3 box — "CLEAN DATA": green glow, checkmark icon, "15 rows validated"
Stage 4 box — "PHASE 2: OLLAMA llama3.2": purple glow, neural-brain icon, "Probabilistic Intelligence"
Stage 5 box — "HYBRID REPORT": cyan glow, document+chart icon, "flagged_expenses.csv"

Bottom legend row: three pill-shaped badges: ✅ Policy-Compliant (green) | ⚠️ Needs Review (amber) | 🚨 Suspicious (red)
Top-right corner watermark: "Nano Banana" small elegant sans-serif white text.
Style: Premium enterprise slide deck infographic. High contrast. 1920×1080. Minimalist dark UI design.
```

#### Prompt B — Imagen Fallback
> Used when nano-banana is unavailable. Clean descriptive prompt optimised for Imagen 4.0.

```
A sleek enterprise data-pipeline infographic on a deep navy background (#0d0f1a).
Title: "Hybrid Sovereign Audit". Neon cyan and electric purple accents. Cyber-Sovereign theme.
Five labeled pipeline stages left to right connected by glowing neon arrows:
Stage 1: RAW DATA (CSV icon), Stage 2: PYDANTIC (amber shield, $10k threshold),
Stage 3: CLEAN DATA (green checkmark), Stage 4: OLLAMA llama3.2 (purple brain),
Stage 5: HYBRID REPORT (cyan document). Bottom: green/amber/red verdict pills.
Top-right watermark: Nano Banana. Premium slide-deck quality, 1920x1080.

```

**Output:** `assets/diagrams/session_01_hybrid_audit.png`