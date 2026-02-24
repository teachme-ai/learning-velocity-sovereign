"""
generate_visuals.py — Sovereign Visual Generator
Generates all session infographics for the AI Bootcamps project.

Strategy:
  1. Try nano-banana-pro-preview first (slide/infographic generation mode)
  2. Fall back through Imagen models: fast → standard → ultra

All prompts are stored in SESSIONS below — edit there to iterate on visuals.
Output paths are relative to the 01_data_pipeline_automation/ project root.

Run:
  cd "/Users/khalidirfan/projects/Ai Bootcamps"
  source ~/.zshrc
  01_data_pipeline_automation/.venv/bin/python \
    01_data_pipeline_automation/assets/diagrams/generate_visuals.py

  # Or a specific session:
  ... generate_visuals.py --session 02
"""

import os
import sys
import argparse
import base64
from pathlib import Path
from google import genai
from google.genai import types

API_KEY = os.environ.get('GEMINI_API_KEY')
ROOT    = Path(__file__).resolve().parent.parent.parent.parent  # Ai Bootcamps/

# ── Model Order ────────────────────────────────────────────────────────────────
NANO_BANANA = 'nano-banana-pro-preview'
IMAGEN_MODELS = [
    'imagen-4.0-fast-generate-001',
    'imagen-4.0-generate-001',
    'imagen-4.0-ultra-generate-001',
]

# ── All Session Visual Definitions ────────────────────────────────────────────
# Each entry defines two prompt variants:
#   "slide_prompt"  — used with nano-banana (slide/infographic mode language)
#   "imagen_prompt" — used with Imagen (clean descriptive prompt)
# Edit either prompt and rerun to iterate on the output.

SESSIONS = {
    '01': {
        'title':       'Hybrid Sovereign Audit',
        'description': 'Five-stage data pipeline: RAW DATA → Pydantic → Clean → Ollama LLM → Report',
        'output':      '01_data_pipeline_automation/assets/diagrams/session_01_hybrid_audit.png',

        # ── Prompt used with nano-banana (slide/infographic mode) ──────────────
        'slide_prompt': """
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
""".strip(),

        # ── Prompt used with Imagen fallback ───────────────────────────────────
        'imagen_prompt': """
A sleek enterprise data-pipeline infographic on a deep navy background (#0d0f1a).
Title: "Hybrid Sovereign Audit". Neon cyan and electric purple accents. Cyber-Sovereign theme.
Five labeled pipeline stages left to right connected by glowing neon arrows:
Stage 1: RAW DATA (CSV icon), Stage 2: PYDANTIC (amber shield, $10k threshold),
Stage 3: CLEAN DATA (green checkmark), Stage 4: OLLAMA llama3.2 (purple brain),
Stage 5: HYBRID REPORT (cyan document). Bottom: green/amber/red verdict pills.
Top-right watermark: Nano Banana. Premium slide-deck quality, 1920x1080.
""".strip(),
    },

    '02': {
        'title':       'The Boardroom Intelligence Bridge',
        'description': 'Boardroom table with AI memo hovering above, data streams from CSV files',
        'output':      '02_executive_narrative_engine/assets/diagrams/session_02_boardroom_bridge.png',

        'slide_prompt': """
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
""".strip(),

        'imagen_prompt': """
A premium 3D enterprise infographic showing a top-down boardroom table in deep charcoal (#0f1117).
Electric teal (#00e5cc) accent color. Center: a glowing digital memo titled "AUDIT STRATEGY"
hovering above the table with volumetric teal glow. Teal data streams arc from CSV file icons
at the table edges to the central memo. Bottom legend: Pattern Detection, AI Synthesis,
Human-in-the-Loop Review. Top-right watermark: Nano Banana. Premium slide quality, 1920x1080.
""".strip(),
    },

    '03': {
        'title':       'Sovereign Orchestration: The Genkit Trace',
        'description': 'Cinematic dual-view: agent nodes (Lens, Shield, Pen) and a futuristic Trace Map dashboard',
        'output':      '03_multi_agent_systems/assets/diagrams/session_03_agent_network.png',

        'slide_prompt': """
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
""".strip(),

        'imagen_prompt': """
A cinematic 4K enterprise infographic in a dual-view layout. Cyber-Sovereign theme.
Left: Three stylized glowing agent nodes with Lens, Shield, and Pen icons in electric teal.
Right: A futuristic dashboard with a "Trace Map" showing glowing data flow arcs between agents.
Deep charcoal background. Electric teal and neon cyan accents. High-tech interface design.
""".strip(),
    },

    '04': {
        'title':       'Private Intelligence: The Local Vault',
        'description': 'High-tech library vault with hexagonal cells and a central AI brain pulling data with a tractor beam',
        'output':      '04_sovereign_knowledge_rag/assets/diagrams/session_04_local_vault.png',

        'slide_prompt': """
A high-tech digital vault with glowing hexagonal honeycombs. A central AI brain is pulling a specific "policy" document from a cell using a teal tractor beam. Title: "Private Intelligence: The Local Vault". Cyber-Sovereign theme.
""".strip(),

        'imagen_prompt': """
A cinematic 4K enterprise infographic of a futuristic high-tech library vault. 
The vault is made of glowing hexagonal glass cells, each containing a digital book icon. 
A central AI brain crystalline core in the foreground uses a teal tractor beam to pull data 
from one specific gold-highlighted cell. Cyber-Sovereign theme, dark mode, 1920x1080.
""".strip(),
    },
}


# ── Generator Logic ────────────────────────────────────────────────────────────

def try_nano_banana(client: genai.Client, prompt: str) -> bytes | None:
    """Attempt generation with nano-banana-pro-preview (slide/infographic mode)."""
    print(f'  [nano-banana] Attempting generation...')
    try:
        response = client.models.generate_images(
            model=NANO_BANANA,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio='16:9',
                safety_filter_level='BLOCK_LOW_AND_ABOVE',
                person_generation='DONT_ALLOW',
            ),
        )
        if response.generated_images:
            img = response.generated_images[0]
            raw = img.image.image_bytes
            return base64.b64decode(raw) if isinstance(raw, str) else raw
        print('  [nano-banana] No images returned.')
    except Exception as exc:
        print(f'  [nano-banana] Failed: {exc}')
    return None


def try_imagen(client: genai.Client, prompt: str) -> bytes | None:
    """Fallback: try Imagen models in order fast → standard → ultra."""
    for model in IMAGEN_MODELS:
        print(f'  [Imagen] Trying {model}...')
        try:
            response = client.models.generate_images(
                model=model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio='16:9',
                    safety_filter_level='BLOCK_LOW_AND_ABOVE',
                    person_generation='DONT_ALLOW',
                ),
            )
            if response.generated_images:
                img = response.generated_images[0]
                raw = img.image.image_bytes
                return base64.b64decode(raw) if isinstance(raw, str) else raw
            print(f'  [Imagen] {model} returned no images.')
        except Exception as exc:
            print(f'  [Imagen] {model} failed: {exc}')
    return None


def generate_session(client: genai.Client, session_id: str) -> bool:
    """Generate the infographic for a single session. Returns True on success."""
    if session_id not in SESSIONS:
        print(f'[ERROR] Unknown session: {session_id}')
        return False

    cfg         = SESSIONS[session_id]
    output_path = ROOT / cfg['output']
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f'\n{"═" * 60}')
    print(f'  Session {session_id}: {cfg["title"]}')
    print(f'{"═" * 60}')

    # 1. Try nano-banana with slide-mode prompt
    image_bytes = try_nano_banana(client, cfg['slide_prompt'])
    engine = NANO_BANANA

    # 2. Fall back to Imagen with imagen-optimised prompt
    if image_bytes is None:
        print(f'  → Falling back to Imagen...')
        image_bytes = try_imagen(client, cfg['imagen_prompt'])
        engine = 'Imagen 4.0'

    if image_bytes is None:
        print(f'  [FAIL] All models failed for Session {session_id}.')
        return False

    output_path.write_bytes(image_bytes)
    print(f'  [OK] Saved ({engine}) → {output_path.relative_to(ROOT)}')
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate session infographics')
    parser.add_argument('--session', choices=['01', '02', '03', '04', 'all'], default='all',
                        help='Which session to generate (default: all)')
    args = parser.parse_args()

    if not API_KEY:
        print('[ERROR] GEMINI_API_KEY not set. Run: export GEMINI_API_KEY="your-key"')
        sys.exit(1)

    client   = genai.Client(api_key=API_KEY)
    sessions = list(SESSIONS.keys()) if args.session == 'all' else [args.session]
    results  = {}

    for sid in sessions:
        results[sid] = generate_session(client, sid)

    print(f'\n{"═" * 60}')
    print('  GENERATION SUMMARY')
    print(f'{"═" * 60}')
    for sid, ok in results.items():
        status = '✅' if ok else '❌'
        print(f'  Session {sid}: {status} {SESSIONS[sid]["title"]}')
    print()


if __name__ == '__main__':
    main()
