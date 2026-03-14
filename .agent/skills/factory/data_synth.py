import os
import sys
import ollama

def call_llm(prompt):
    """Use Gemini if API key available, otherwise fall back to Ollama."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            print("   → Using Gemini (cloud)")
            return response.text
        except Exception as e:
            print(f"   → Gemini failed ({e}), falling back to Ollama")

    print("   → Using Ollama (local)")
    model = os.environ.get("SYNTH_MODEL", "qwen2.5:0.5b")
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
