import os
import base64
from pathlib import Path
from typing import List, Optional
from google import genai
from google.genai import types

class NanoBananaService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY must be provided or set as an environment variable.")
        self.client = genai.Client(api_key=self.api_key)
        self.models = [
            "imagen-4.0-fast-generate-001",
            "imagen-4.0-generate-001",
            "imagen-4.0-ultra-generate-001",
        ]

    def generate_diagram(self, prompt: str, output_path: Path) -> bool:
        """
        Generates a diagram using Nano Banana's Cyber-Sovereign theme.
        """
        print(f"[INFO] Generating diagram with prompt: {prompt[:100]}...")
        
        for model in self.models:
            try:
                response = self.client.models.generate_images(
                    model=model,
                    prompt=prompt,
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
                    
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_bytes(image_bytes)
                    print(f"[OK] Diagram saved to {output_path}")
                    return True
                
            except Exception as e:
                print(f"[WARN] Model {model} failed: {e}")
                continue
                
        print(f"[ERROR] All models failed for prompt: {prompt[:50]}")
        return False
