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

**Output:** `01_data_pipeline_automation/assets/diagrams/session_01_hybrid_audit.png`

---

## Session 02 — Executive Narrative Engine

### Infographic: The Boardroom Intelligence Bridge

**Status:** ✅ Rendered → `02_executive_narrative_engine/assets/diagrams/session_02_boardroom_bridge.png` (Imagen 4.0, 2026-02-24)

#### Prompt A — Slide/Infographic Mode (nano-banana)

```
SLIDE INFOGRAPHIC — Cyber-Sovereign Executive Theme.
Title panel: "Executive Narrative Engine: From Raw Data to Boardroom Intelligence"
Background: Deep Charcoal (#0f1117). Accent: Electric Teal (#00e5cc), sharp white typography.

Main visual: Top-down perspective of a dark polished slate boardroom table (fills 80% of frame).
Center element: A floating glowing digital memo document, title "AUDIT STRATEGY" in bold teal text,
  volumetric teal glow halo around it, subtle drop shadow onto the table surface.
Surrounding the memo: Animated-style teal data streams arc outward to CSV file icons at the table edges,
  representing the journey from raw transactional data to executive insight.

Bottom legend bar — three items with icons:
  📊 "Pattern Detection"   |   🤖 "AI Synthesis"   |   👤 "Human-in-the-Loop Review"

Top-right watermark: "Nano Banana" small elegant sans-serif.
Style: Premium 3D enterprise slide infographic. Dark polished materials. 1920×1080.
```

#### Prompt B — Imagen Fallback

```
A premium 3D enterprise infographic showing a top-down boardroom table in deep charcoal (#0f1117).
Electric teal (#00e5cc) accent color. Center: a glowing digital memo titled "AUDIT STRATEGY"
hovering above the table with volumetric teal glow. Teal data streams arc from CSV file icons
at the table edges to the central memo. Bottom legend: Pattern Detection, AI Synthesis,
Human-in-the-Loop Review. Top-right watermark: Nano Banana. Premium slide quality, 1920x1080.
```

**Output:** `02_executive_narrative_engine/assets/diagrams/session_02_boardroom_bridge.png`

---

## Session 03 — Multi-Agent Systems

### Infographic: Sovereign Orchestration: The Genkit Trace

**Status:** ✅ Rendered

**Concept:** A cinematic dual-view infographic. One side shows three stylized agent nodes (Lens, Shield, Pen) in electric teal. The other side shows a futuristic dashboard with a "Trace Map" showing data flow.

#### Prompt A — Slide/Infographic Mode (nano-banana)

```
SLIDE INFOGRAPHIC — Cyber-Sovereign Multi-Agent Theme.
Layout: Cinematic dual-view horizontal split.
Left Panel: "The Sovereign Committee". Three stylized 3D agent nodes floating in a dark void.
- Node 1: Lens icon (Forensic)
- Node 2: Shield icon (Strategist)
- Node 3: Pen icon (Critic)
Nodes are rendered in glowing Electric Teal (#00e5cc) with neon halos.

Right Panel: "Genkit Trace Dashboard". A futuristic high-tech dashboard interface.
Main feature: A "Trace Map" showing glowing data flow arcs and hierarchical spans connecting the agents.
Data packets labeled "JSON", "Markdown", and "Critique" move between spans.

Theme: Dark Mode, Cyber-Sovereign aesthetic.
Palette: Deep Charcoal (#0f1117), Electric Teal (#00e5cc), Neon Cyan (#00f5ff).
Quality: 4K enterprise quality, premium 3D materials, high contrast. 1920×1080.
```

#### Prompt B — Imagen Fallback

```
A cinematic 4K enterprise infographic in a dual-view layout. Cyber-Sovereign theme.
Left: Three stylized glowing agent nodes with Lens, Shield, and Pen icons in electric teal.
Right: A futuristic dashboard with a "Trace Map" showing glowing data flow arcs between agents.
Deep charcoal background. Electric teal and neon cyan accents. High-tech interface design.
```

**Output:** `03_multi_agent_systems/assets/diagrams/session_03_agent_network.png`

---

## Session 04 — Sovereign Knowledge RAG

### Infographic: Private Intelligence: The Local Vault

**Status:** ✅ Rendered

**Concept:** A high-tech library vault made of glowing hexagonal cells. Each cell contains a digital book icon. A central AI brain is pulling specific data from one cell using a teal tractor beam.

#### Prompt A — Slide/Infographic Mode (nano-banana)

```
SLIDE INFOGRAPHIC — Cyber-Sovereign RAG Theme.
Layout: Immersive 3D interior of a futuristic data vault.
Main visual: A vast "Library Vault" constructed from glowing hexagonal glass cells stacked vertically into infinity.
Each cell contains a minimalist holographic "Digital Book" icon. 
The cells pulse with soft blue light.

Central feature: A stylized "AI Brain" core (crystalline structure) at the bottom-center.
The brain is firing an "Electric Teal (#00e5cc) Tractor Beam" upwards, targeting a single specific hexagonal cell.
The targeted cell is highlighted in bright gold, and bits of glowing data (binary/cubes) are being pulled down the beam into the brain.

Title: "Private Intelligence: The Local Vault" (Elegant, futuristic sans-serif).
Theme: Dark Mode, Cyber-Sovereign.
Palette: Deep Midnight (#05070a), Electric Teal (#00e5cc), Soft Blue, Golden highlight.
Quality: Cinematic 4K, ray-traced materials, depth of field. 1920×1080.
```

#### Prompt B — Imagen Fallback

```
A cinematic 4K enterprise infographic of a futuristic high-tech library vault. 
The vault is made of glowing hexagonal glass cells, each containing a digital book icon. 
A central AI brain crystalline core in the foreground uses a teal tractor beam to pull data 
from one specific gold-highlighted cell. Cyber-Sovereign theme, dark mode, 1920x1080.
```

**Output:** `04_sovereign_knowledge_rag/assets/diagrams/session_04_local_vault.png`


---

## Iteration Guide

If you're not satisfied with an output:

1. Open [`generate_visuals.py`](file:///Users/khalidirfan/projects/Ai%20Bootcamps/01_data_pipeline_automation/assets/diagrams/generate_visuals.py)
2. Find the session in `SESSIONS = { ... }`
3. Edit `slide_prompt` or `imagen_prompt`
4. Run with `--session XX` flag
5. Update the **Status** line in this manifest when satisfied

> **Tip:** Adding phrases like `"ultra-detailed", "4K quality", "Behance award-winning infographic"` to Prompt B can push Imagen outputs to higher fidelity.
