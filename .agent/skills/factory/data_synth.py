import os
import sys
import json
import requests

try:
    import ollama
except ImportError:
    ollama = None

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

def call_llm(prompt):
    """Use Gemini REST if API key available, otherwise fall back to Ollama."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    model = os.environ.get("SYNTH_MODEL", "gemini-2.5-flash-lite")
    if api_key and not model.startswith("llama") and not model.startswith("qwen"):
        try:
            url = GEMINI_API_URL.format(model=model) + f"?key={api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}}
            resp = requests.post(url, json=payload, timeout=90)
            resp.raise_for_status()
            print("   → Using Gemini (cloud)")
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"   → Gemini REST failed ({e}), falling back to Ollama")
    print("   → Using Ollama (local)")
    if ollama is None:
        print("   → Ollama not available")
        return ""
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

def generate_dirty_data(slug, industry, columns=None, dirty_rate=0.15, row_count=50):
    """Generate dirty CSV data for a specific industry."""
    print(f"🧬 Generating {row_count} rows of synthetic data for {industry}...")

    if columns:
        col_list = columns if isinstance(columns, list) else columns.split(",")
        col_instruction = f"Use EXACTLY these columns in this order: {', '.join(col_list)}"
    else:
        col_instruction = f"Choose column names that are specific and meaningful for {industry} professionals. Always include: an id column, a date column, and an amount/value column."

    dirty_pct = int(dirty_rate * 100)
    prompt = f"""Generate {row_count} rows of CSV data for the {industry} industry.
{col_instruction}
Inject intentional dirty data in ~{dirty_pct}% of rows: nulls, duplicates, format errors, misspellings.
Return ONLY the CSV starting with the header row. No preamble, no explanation.
START CSV NOW."""

    try:
        csv_content = call_llm(prompt).strip()

        # Find the header row: first line containing a comma
        lines = csv_content.splitlines()
        for i, line in enumerate(lines):
            if ',' in line:
                csv_content = '\n'.join(lines[i:])
                break

        target_dir = os.path.join(os.path.dirname(__file__), "../../../_factory/templates/01_data_pipeline_automation/set_{{ industry_slug }}/data")
        os.makedirs(target_dir, exist_ok=True)

        target_file = os.path.join(target_dir, "dirty_data.csv")
        with open(target_file, 'w') as f:
            f.write(csv_content)

        with open(os.path.join(target_dir, "corporate_expenses.csv"), 'w') as f:
            f.write(csv_content)

        print(f"✅ Data written to {target_file}")
    except Exception as e:
        print(f"❌ Failed to generate synthetic data: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 data_synth.py <slug> <industry> [columns] [dirty_rate] [row_count]")
        sys.exit(1)
    _columns = sys.argv[3] if len(sys.argv) > 3 else None
    _dirty_rate = float(sys.argv[4]) if len(sys.argv) > 4 else 0.15
    _row_count = int(sys.argv[5]) if len(sys.argv) > 5 else 50
    generate_dirty_data(sys.argv[1], sys.argv[2], _columns, _dirty_rate, _row_count)
