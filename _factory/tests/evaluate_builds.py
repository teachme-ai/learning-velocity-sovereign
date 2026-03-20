"""
Bootcamp Quality Evaluator
Compares Local (Ollama) vs Cloud (Gemini) builds against learning effectiveness rubric.

Rubric:
  1. Industry Fidelity (20%) — healthcare-specific terms vs generic
  2. Hands-on Ratio (30%) — lab steps, code blocks, CLI commands vs prose
  3. Executable Practicality (25%) — can steps run in Codespace/browser? deps listed?
  4. Track Differentiation (15%) — navigator/builder/architect get different content
  5. Structural Completeness (10%) — all 8 sessions, sections intact
"""
import os
import re
import glob
import json

# ── Healthcare domain terms ──────────────────────────────────────────
HEALTHCARE_TERMS = [
    "patient", "clinical", "diagnosis", "treatment", "medical", "healthcare",
    "hospital", "EHR", "HIPAA", "radiology", "imaging", "readmission",
    "pharma", "prescription", "discharge", "triage", "prognosis",
    "pathology", "oncology", "cardiology", "vital signs", "lab results",
    "ICD", "CPT", "HL7", "FHIR", "PACS", "prior authorization",
    "claims", "insurance", "genomics", "biomarker", "dosage",
]

GENERIC_TERMS = [
    "corporate_expenses", "financial integrity", "expense report",
    "retail", "cyber", "trading", "stock", "portfolio management",
    "supply chain", "logistics", "warehouse",
]

# ── Hands-on indicators ─────────────────────────────────────────────
CODE_BLOCK_PATTERN = re.compile(r"```[\s\S]*?```")
CLI_PATTERN = re.compile(r"^\s*(pip install|npm|python3?|ollama|docker|curl|wget|git |cd |mkdir|streamlit|bash|sh )", re.MULTILINE)
STEP_PATTERN = re.compile(r"^\s*(step\s+\d|##\s+\d|###\s+\d|\d+\.\s+)", re.MULTILINE | re.IGNORECASE)

# ── Executable practicality indicators ───────────────────────────────
DEP_PATTERNS = [
    re.compile(r"pip install", re.IGNORECASE),
    re.compile(r"requirements\.txt", re.IGNORECASE),
    re.compile(r"npm install", re.IGNORECASE),
    re.compile(r"package\.json", re.IGNORECASE),
    re.compile(r"docker", re.IGNORECASE),
    re.compile(r"\.venv|venv|virtualenv", re.IGNORECASE),
]
CODESPACE_PATTERNS = [
    re.compile(r"codespace|github\.dev|\.devcontainer", re.IGNORECASE),
    re.compile(r"localhost:\d+", re.IGNORECASE),
    re.compile(r"streamlit run|flask run|uvicorn|gradio", re.IGNORECASE),
    re.compile(r"http://|https://", re.IGNORECASE),
]
PLATFORM_CONFIG_PATTERNS = [
    re.compile(r"n8n|make\.com|lovable|zapier", re.IGNORECASE),
    re.compile(r"\.json\b.*config|workflow.*json|import.*json", re.IGNORECASE),
]

# ── Track patterns ───────────────────────────────────────────────────
NAVIGATOR_INDICATORS = ["no-code", "browser", "drag", "visual", "click", "interface", "GUI", "dashboard"]
BUILDER_INDICATORS = ["low-code", "guided", "template", "modify", "customize", "configure"]
ARCHITECT_INDICATORS = ["python", "def ", "class ", "import ", "async", "API", "endpoint", "deploy", "docker"]


def collect_md_files(build_dir):
    """Collect all .md files from a build directory."""
    files = {}
    for path in glob.glob(os.path.join(build_dir, "**", "*.md"), recursive=True):
        rel = os.path.relpath(path, build_dir)
        with open(path, encoding="utf-8", errors="replace") as f:
            files[rel] = f.read()
    return files


def score_industry_fidelity(files):
    """20% — Count healthcare terms vs generic terms across all files."""
    all_text = " ".join(files.values()).lower()
    healthcare_hits = sum(all_text.count(t.lower()) for t in HEALTHCARE_TERMS)
    generic_hits = sum(all_text.count(t.lower()) for t in GENERIC_TERMS)
    total_words = len(all_text.split())

    # Score: healthcare density minus generic contamination
    density = (healthcare_hits / max(total_words, 1)) * 10000
    contamination = (generic_hits / max(total_words, 1)) * 10000
    raw_score = min(100, max(0, density * 5 - contamination * 20))

    return {
        "score": round(raw_score, 1),
        "healthcare_terms": healthcare_hits,
        "generic_terms": generic_hits,
        "total_words": total_words,
        "density_per_1k": round(healthcare_hits / max(total_words, 1) * 1000, 2),
    }


def score_handson_ratio(files):
    """30% — Ratio of hands-on content (code blocks, CLI, steps) vs total."""
    total_lines = 0
    handson_lines = 0
    code_blocks = 0
    cli_commands = 0
    step_markers = 0

    for content in files.values():
        lines = content.split("\n")
        total_lines += len(lines)

        # Count code block lines
        blocks = CODE_BLOCK_PATTERN.findall(content)
        code_blocks += len(blocks)
        for b in blocks:
            handson_lines += b.count("\n") + 1

        # Count CLI commands outside code blocks
        cli_commands += len(CLI_PATTERN.findall(content))

        # Count step markers
        step_markers += len(STEP_PATTERN.findall(content))

    ratio = handson_lines / max(total_lines, 1)
    # Target: 80% hands-on. Score relative to that.
    raw_score = min(100, (ratio / 0.8) * 100)

    return {
        "score": round(raw_score, 1),
        "handson_lines": handson_lines,
        "total_lines": total_lines,
        "ratio": round(ratio * 100, 1),
        "code_blocks": code_blocks,
        "cli_commands": cli_commands,
        "step_markers": step_markers,
    }


def score_executable_practicality(files):
    """25% — Can these steps actually run in Codespace/browser?"""
    all_text = " ".join(files.values())
    dep_hits = sum(len(p.findall(all_text)) for p in DEP_PATTERNS)
    codespace_hits = sum(len(p.findall(all_text)) for p in CODESPACE_PATTERNS)
    platform_hits = sum(len(p.findall(all_text)) for p in PLATFORM_CONFIG_PATTERNS)

    # Check for complete setup blocks (venv + pip + run)
    has_venv_setup = bool(re.search(r"python3?\s+-m\s+venv", all_text))
    has_pip_install = bool(re.search(r"pip install", all_text))
    has_run_command = bool(re.search(r"(streamlit run|python3?\s+\w+\.py|flask run|uvicorn)", all_text))
    complete_setup = has_venv_setup and has_pip_install and has_run_command

    total_signals = dep_hits + codespace_hits + platform_hits + (20 if complete_setup else 0)
    raw_score = min(100, total_signals * 2)

    return {
        "score": round(raw_score, 1),
        "dependency_refs": dep_hits,
        "codespace_refs": codespace_hits,
        "platform_config_refs": platform_hits,
        "complete_setup_flow": complete_setup,
    }


def score_track_differentiation(files):
    """15% — Do navigator/builder/architect get different content levels?"""
    track_scores = {"navigator": 0, "builder": 0, "architect": 0}

    for path, content in files.items():
        lower_path = path.lower()
        lower_content = content.lower()

        if "navigator" in lower_path or "track_1" in lower_path:
            track_scores["navigator"] += sum(1 for t in NAVIGATOR_INDICATORS if t.lower() in lower_content)
        if "builder" in lower_path or any(s in lower_path for s in ["01_data", "02_exec", "03_multi", "04_sov", "05_adv"]):
            track_scores["builder"] += sum(1 for t in BUILDER_INDICATORS if t.lower() in lower_content)
        if "architect" in lower_path or "logic" in lower_path or lower_path.endswith(".py"):
            track_scores["architect"] += sum(1 for t in ARCHITECT_INDICATORS if t.lower() in lower_content)

    # Score: all 3 tracks should have signals
    tracks_with_content = sum(1 for v in track_scores.values() if v > 0)
    raw_score = (tracks_with_content / 3) * 100

    return {
        "score": round(raw_score, 1),
        "navigator_signals": track_scores["navigator"],
        "builder_signals": track_scores["builder"],
        "architect_signals": track_scores["architect"],
    }


def score_structural_completeness(files):
    """10% — All 8 sessions present, no truncation."""
    session_dirs = set()
    for path in files:
        parts = path.split(os.sep)
        for p in parts:
            if len(p) >= 2 and p[:2].isdigit():
                session_dirs.add(int(p[:2]))

    sessions_found = len(session_dirs)
    total_files = len(files)

    # Check for truncation (files under 100 chars likely broken)
    truncated = sum(1 for c in files.values() if len(c) < 100)

    raw_score = (sessions_found / 8) * 80 + (20 if truncated == 0 else max(0, 20 - truncated * 5))

    return {
        "score": round(min(100, raw_score), 1),
        "sessions_found": sorted(session_dirs),
        "session_count": sessions_found,
        "total_md_files": total_files,
        "truncated_files": truncated,
    }


def evaluate_build(build_dir, label):
    """Run full evaluation on a build directory."""
    print(f"\n{'='*70}")
    print(f"  EVALUATING: {label}")
    print(f"  Directory: {build_dir}")
    print(f"{'='*70}")

    if not os.path.exists(build_dir):
        print(f"  BUILD DIRECTORY NOT FOUND: {build_dir}")
        return None

    files = collect_md_files(build_dir)
    if not files:
        print(f"  NO .md FILES FOUND")
        return None

    print(f"  Files analyzed: {len(files)}")
    print()

    results = {}

    # 1. Industry Fidelity (20%)
    r = score_industry_fidelity(files)
    results["industry_fidelity"] = r
    print(f"  1. INDUSTRY FIDELITY (20%):        {r['score']}/100")
    print(f"     Healthcare terms: {r['healthcare_terms']} | Generic contamination: {r['generic_terms']}")
    print(f"     Density: {r['density_per_1k']} healthcare terms per 1K words")
    print()

    # 2. Hands-on Ratio (30%)
    r = score_handson_ratio(files)
    results["handson_ratio"] = r
    print(f"  2. HANDS-ON RATIO (30%):           {r['score']}/100")
    print(f"     Hands-on lines: {r['handson_lines']}/{r['total_lines']} ({r['ratio']}%)")
    print(f"     Code blocks: {r['code_blocks']} | CLI commands: {r['cli_commands']} | Step markers: {r['step_markers']}")
    print()

    # 3. Executable Practicality (25%)
    r = score_executable_practicality(files)
    results["executable_practicality"] = r
    print(f"  3. EXECUTABLE PRACTICALITY (25%):   {r['score']}/100")
    print(f"     Dependency refs: {r['dependency_refs']} | Codespace refs: {r['codespace_refs']}")
    print(f"     Platform configs: {r['platform_config_refs']} | Complete setup flow: {r['complete_setup_flow']}")
    print()

    # 4. Track Differentiation (15%)
    r = score_track_differentiation(files)
    results["track_differentiation"] = r
    print(f"  4. TRACK DIFFERENTIATION (15%):     {r['score']}/100")
    print(f"     Navigator: {r['navigator_signals']} | Builder: {r['builder_signals']} | Architect: {r['architect_signals']}")
    print()

    # 5. Structural Completeness (10%)
    r = score_structural_completeness(files)
    results["structural_completeness"] = r
    print(f"  5. STRUCTURAL COMPLETENESS (10%):   {r['score']}/100")
    print(f"     Sessions: {r['session_count']}/8 {r['sessions_found']}")
    print(f"     Total .md files: {r['total_md_files']} | Truncated: {r['truncated_files']}")
    print()

    # Weighted total
    weights = {
        "industry_fidelity": 0.20,
        "handson_ratio": 0.30,
        "executable_practicality": 0.25,
        "track_differentiation": 0.15,
        "structural_completeness": 0.10,
    }
    weighted = sum(results[k]["score"] * weights[k] for k in weights)
    results["weighted_total"] = round(weighted, 1)

    print(f"  WEIGHTED TOTAL:                     {results['weighted_total']}/100")
    print(f"{'='*70}")

    return results


def compare(local_results, cloud_results):
    """Side-by-side comparison."""
    print(f"\n{'='*70}")
    print(f"  SIDE-BY-SIDE COMPARISON")
    print(f"{'='*70}")
    print()

    dims = [
        ("Industry Fidelity", "industry_fidelity", "20%"),
        ("Hands-on Ratio", "handson_ratio", "30%"),
        ("Executable Practicality", "executable_practicality", "25%"),
        ("Track Differentiation", "track_differentiation", "15%"),
        ("Structural Completeness", "structural_completeness", "10%"),
    ]

    print(f"  {'Dimension':<30} {'Weight':<8} {'Local':<10} {'Cloud':<10} {'Delta':<10} {'Winner':<10}")
    print(f"  {'-'*78}")

    for label, key, weight in dims:
        l = local_results[key]["score"] if local_results else 0
        c = cloud_results[key]["score"] if cloud_results else 0
        delta = c - l
        winner = "Cloud" if delta > 2 else ("Local" if delta < -2 else "Tie")
        print(f"  {label:<30} {weight:<8} {l:<10} {c:<10} {delta:+.1f}{'':5} {winner:<10}")

    lt = local_results["weighted_total"] if local_results else 0
    ct = cloud_results["weighted_total"] if cloud_results else 0
    delta = ct - lt
    winner = "CLOUD" if delta > 2 else ("LOCAL" if delta < -2 else "TIE")
    print(f"  {'-'*78}")
    print(f"  {'WEIGHTED TOTAL':<30} {'100%':<8} {lt:<10} {ct:<10} {delta:+.1f}{'':5} {winner:<10}")
    print()


if __name__ == "__main__":
    import sys
    local_dir = sys.argv[1] if len(sys.argv) > 1 else "dist/ai_for_healthcare_local"
    cloud_dir = sys.argv[2] if len(sys.argv) > 2 else "dist/ai_for_healthcare_cloud"

    local_results = evaluate_build(local_dir, "LOCAL (Ollama)")
    cloud_results = evaluate_build(cloud_dir, "CLOUD (Gemini)")

    if local_results and cloud_results:
        compare(local_results, cloud_results)

    # Save raw results
    output = {"local": local_results, "cloud": cloud_results}
    with open("_factory/logs/evaluation_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"  Raw results saved to _factory/logs/evaluation_results.json")
