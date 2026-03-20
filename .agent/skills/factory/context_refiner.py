import os
import sys
import json
import requests

try:
    import ollama
except ImportError:
    ollama = None

TARGET_KEYWORDS = {
    "introduction", "business value", "overview", "why this matters",
    "objective", "goal", "the objective", "what you will learn",
    "what you will build", "learning outcomes", "prerequisites",
    "background", "context", "motivation", "the challenge",
    "step-by-step", "lab overview", "session overview",
}

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

def call_llm(prompt):
    """Use Gemini REST if API key available, otherwise fall back to Ollama."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    model = os.environ.get("REFINER_MODEL", "gemini-2.5-flash")
    if api_key and not model.startswith("llama") and not model.startswith("qwen"):
        try:
            url = GEMINI_API_URL.format(model=model) + f"?key={api_key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}}
            resp = requests.post(url, json=payload, timeout=90)
            resp.raise_for_status()
            return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"   → Gemini REST failed ({e}), falling back to Ollama")
    print("   → Using Ollama (local)")
    if ollama is None:
        print("   → Ollama not available, skipping refinement")
        return ""
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]


def extract_target_sections(content):
    """Return list of {heading, body} dicts for headings matching TARGET_KEYWORDS."""
    sections = []
    lines = content.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            heading_text = line.lstrip("#").strip().lower()
            if any(kw in heading_text for kw in TARGET_KEYWORDS):
                heading = line
                body_lines = []
                i += 1
                while i < len(lines) and not lines[i].startswith("#"):
                    body_lines.append(lines[i])
                    i += 1
                sections.append({"heading": heading, "body": "\n".join(body_lines)})
                continue
        i += 1
    return sections


def patch_sections(original_content, refined_sections):
    """Replace only the matched section bodies in the original content."""
    result = original_content
    try:
        for section in refined_sections:
            heading = section["heading"]
            new_body = section["body"]
            # Find heading in content
            idx = result.find(heading)
            if idx == -1:
                continue
            after_heading = idx + len(heading)
            # Find where the next heading starts
            rest = result[after_heading:]
            next_heading_idx = len(rest)
            for i, line in enumerate(rest.splitlines(keepends=True)):
                if i > 0 and line.startswith("#"):
                    next_heading_idx = rest.find(line)
                    break
            result = result[:after_heading] + "\n" + new_body + "\n" + result[after_heading + next_heading_idx:]
    except Exception:
        return original_content
    return result


def parse_refined_sections(llm_response):
    """Parse LLM response into list of {heading, body} dicts."""
    sections = []
    try:
        parts = llm_response.split("## SECTION:")
        for part in parts[1:]:
            end_marker = "## END_SECTION"
            end_idx = part.find(end_marker)
            block = part[:end_idx].strip() if end_idx != -1 else part.strip()
            newline_idx = block.find("\n")
            if newline_idx == -1:
                continue
            heading = block[:newline_idx].strip()
            body = block[newline_idx:].strip()
            sections.append({"heading": heading, "body": body})
    except Exception:
        return []
    return sections


def refine_intro_paragraph(content, industry_name, tone):
    """Fallback: rewrite the first prose paragraph for industry specificity."""
    lines = content.splitlines()
    # Find first non-heading, non-empty paragraph after the title
    para_start = None
    para_end = None
    for i, line in enumerate(lines):
        if line.startswith("#"):
            continue
        if line.strip() == "":
            continue
        if line.startswith("```") or line.startswith("|") or line.startswith("---"):
            continue
        # Found a prose line
        if para_start is None:
            para_start = i
        para_end = i
        # Take up to 5 consecutive prose lines
        if para_end - para_start >= 4:
            break
        # Stop at next heading or blank
        if i + 1 < len(lines) and (lines[i+1].startswith("#") or lines[i+1].strip() == ""):
            break

    if para_start is None:
        return None

    original_para = "\n".join(lines[para_start:para_end+1])
    if len(original_para) < 30:
        return None

    prompt = f"""Rewrite this paragraph for the {industry_name} industry. Keep it concise (2-3 sentences max). Use {industry_name}-specific terminology and examples. Tone: {tone}. Return ONLY the rewritten paragraph, nothing else.

Original:
{original_para}"""

    try:
        rewritten = call_llm(prompt).strip()
        if not rewritten or len(rewritten) < 20 or rewritten.startswith("#"):
            return None
        # Remove any markdown fencing the LLM might add
        if rewritten.startswith("```"):
            rewritten = rewritten.split("```")[1].strip()
        new_lines = list(lines)
        new_lines[para_start:para_end+1] = [rewritten]
        return "\n".join(new_lines)
    except Exception:
        return None


def refine_markdown(file_path, industry_name, industry_slug):
    """Surgically rewrite only Introduction/Business Value sections for the target industry."""
    print(f"✨ Refining {os.path.basename(file_path)} for {industry_name}...")
    tone = os.environ.get("REFINER_TONE", "Practical & Applied")

    with open(file_path, "r") as f:
        content = f.read()

    target_sections = extract_target_sections(content)
    if not target_sections:
        # Fallback: refine the first prose paragraph after the title
        refined = refine_intro_paragraph(content, industry_name, tone)
        if refined and refined != content:
            with open(file_path, "w") as f:
                f.write(refined)
            print(f"✅ Refined intro paragraph in {os.path.basename(file_path)}")
        else:
            print(f"⚠️  No refinable sections in {os.path.basename(file_path)}, skipping.")
        return

    extracted_text = "\n\n".join(
        f"## SECTION: {s['heading']}\n{s['body']}\n## END_SECTION"
        for s in target_sections
    )

    TONE_INSTRUCTIONS = {
        "Strategic & Analytical": "Use executive language: ROI, stakeholder outcomes, governance, risk-adjusted returns, strategic imperatives.",
        "Technical & Precise":    "Use engineering register: system architecture, implementation details, performance characteristics, failure modes.",
        "Practical & Applied":    "Use practitioner language: step-by-step workflows, real-world constraints, operational trade-offs.",
        "Conversational & Accessible": "Use plain, approachable language: relatable analogies, jargon-free explanations, encourage curiosity.",
    }
    tone_instruction = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["Practical & Applied"])

    prompt = f"""You are a technical curriculum expert rewriting sections for the {industry_name} industry.

Tone: {tone}
Tone guidance: {tone_instruction}

Rewrite each section below. Rules:
1. Replace generic analogies with {industry_name}-specific ones
2. Keep all technical terms, commands, and code references identical
3. Match the tone and vocabulary described above
4. Return ONLY the rewritten sections in this exact format:
   ## SECTION: <original heading>
   <rewritten body>
   ## END_SECTION

Sections to rewrite:
{extracted_text}"""

    estimated_tokens = len(prompt) // 4
    print(f"   → Sending ~{estimated_tokens} tokens to LLM (was ~750)")

    try:
        llm_output = call_llm(prompt).strip()

        refined_sections = parse_refined_sections(llm_output)
        if not refined_sections:
            print(f"⚠️  Could not parse LLM response for {file_path}, skipping write.")
            return

        patched = patch_sections(content, refined_sections)

        if "# " in patched or "## " in patched:
            with open(file_path, "w") as f:
                f.write(patched)
            print(f"✅ Patched {len(refined_sections)} section(s) in {os.path.basename(file_path)}")
        else:
            print(f"⚠️  Patched output didn't look like markdown, skipping write.")

    except Exception as e:
        print(f"❌ Failed to refine {file_path}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 context_refiner.py <file_path> <industry_name> <industry_slug>")
        sys.exit(1)
    refine_markdown(sys.argv[1], sys.argv[2], sys.argv[3])
