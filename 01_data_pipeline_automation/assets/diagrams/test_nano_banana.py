"""
assets/diagrams/test_nano_banana.py
Generates the Session 01 Hybrid Sovereign Audit infographic using Imagen 4.0.
Falls back through model options: imagen-4.0-fast → imagen-4.0-generate → imagen-4.0-ultra.
"""

import os
import base64
from pathlib import Path
from google import genai
from google.genai import types

API_KEY    = os.environ.get("GEMINI_API_KEY")
OUTPUT_DIR = Path(__file__).parent
OUTPUT_PATH = OUTPUT_DIR / "session_01_hybrid_audit.png"

MODELS = [
    "imagen-4.0-fast-generate-001",
    "imagen-4.0-generate-001",
    "imagen-4.0-ultra-generate-001",
]

PROMPT = (
    "A sleek enterprise infographic titled 'Hybrid Sovereign Audit: "
    "Deterministic Rules + Probabilistic Intelligence'. "
    "Dark navy background with neon cyan and electric purple accents. Cyber-Sovereign theme. "
    "Left-to-right horizontal pipeline with 5 labeled stages connected by glowing neon arrows: "
    "Stage 1: RAW DATA (CSV file icon, dark slate). "
    "Stage 2: PHASE 1 PYDANTIC (amber shield, 'Schema validation + $10k threshold'). "
    "Stage 3: CLEAN DATA (green checkmark, '15 rows validated'). "
    "Stage 4: PHASE 2 OLLAMA llama3.2 (purple neural brain, 'Probabilistic categorisation'). "
    "Stage 5: HYBRID REPORT (cyan document and chart, 'flagged_expenses.csv'). "
    "Bottom legend: green Policy-Compliant pill, amber Needs Review pill, red Suspicious pill. "
    "Top-right watermark text: Nano Banana. Premium slide-deck quality, 1920x1080."
)


def main():
    if not API_KEY:
        print("[ERROR] GEMINI_API_KEY not set. Run: export GEMINI_API_KEY='your-key'")
        return

    client = genai.Client(api_key=API_KEY)

    for model in MODELS:
        print(f"[INFO]  Trying {model}...")
        try:
            response = client.models.generate_images(
                model=model,
                prompt=PROMPT,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="16:9",
                    safety_filter_level="BLOCK_LOW_AND_ABOVE",
                    person_generation="DONT_ALLOW",
                ),
            )

            if response.generated_images:
                img = response.generated_images[0]
                image_bytes = base64.b64decode(img.image.image_bytes) \
                    if isinstance(img.image.image_bytes, str) \
                    else img.image.image_bytes
                OUTPUT_PATH.write_bytes(image_bytes)
                print(f"[OK]    Image saved → {OUTPUT_PATH}")
                return
            else:
                print(f"[WARN]  {model} returned no images, trying next...")

        except Exception as exc:
            print(f"[ERROR] {model} failed: {exc}")
            continue

    print("[FAIL]  All Imagen models failed. Try again later.")


if __name__ == "__main__":
    main()
