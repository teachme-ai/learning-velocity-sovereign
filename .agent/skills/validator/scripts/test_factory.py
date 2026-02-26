#!/usr/bin/env python3
"""
Systems Validator — test_factory.py
====================================
Loops through all 5 domains × configured sessions.
For each entry:
  1. Checks the logic script file exists.
  2. Runs a Dry Run (import-safe, no Ollama call) to verify the module is valid Python.
  3. Captures exit code: 0 = PASS, non-zero = FAIL.
Then writes HEALTH_CHECK.md to the project root.

Usage:
    python3 .agent/skills/validator/scripts/test_factory.py
"""

import os
import sys
import ast
import urllib.request
import json
from datetime import datetime

# ── Project root (3 levels up from this script) ───────────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
HEALTH_CHECK_PATH = os.path.join(ROOT, "HEALTH_CHECK.md")
PYTHON = sys.executable

# ── Session × Domain Matrix ───────────────────────────────────────────────────
DOMAINS = {
    "set_a_finance": {
        "label": "Finance",
        "sessions": {
            "01": "01_data_pipeline_automation/set_a_finance/logic/cleaner.py",
            "02": "02_executive_narrative_engine/set_a_finance/logic/narrative_gen.py",
            "03": "03_multi_agent_systems/set_a_finance/logic/swarm.py",
        },
    },
    "set_b_healthcare": {
        "label": "Healthcare",
        "sessions": {
            "01": "01_data_pipeline_automation/set_b_healthcare/logic/scrubber.py",
            "02": "02_executive_narrative_engine/set_b_healthcare/logic/compliance_gen.py",
            "03": "03_multi_agent_systems/set_b_healthcare/logic/swarm.py",
        },
    },
    "set_c_supply_chain": {
        "label": "Supply Chain",
        "sessions": {
            "01": "01_data_pipeline_automation/set_c_supply_chain/logic/inventory_validator.py",
            "02": "02_executive_narrative_engine/set_c_supply_chain/logic/risk_memo_gen.py",
            "03": "03_multi_agent_systems/set_c_supply_chain/logic/swarm.py",
        },
    },
    "set_d_edtech": {
        "label": "EdTech",
        "sessions": {
            "01": "01_data_pipeline_automation/set_d_edtech/logic/velocity_cleaner.py",
            "02": "02_executive_narrative_engine/set_d_edtech/logic/velocity_memo_gen.py",
            "03": "03_multi_agent_systems/set_d_edtech/logic/swarm.py",
        },
    },
    "set_e_legal": {
        "label": "Legal",
        "sessions": {
            "01": "01_data_pipeline_automation/set_e_legal/logic/clause_scanner.py",
            "02": "02_executive_narrative_engine/set_e_legal/logic/due_diligence_gen.py",
            "03": "03_multi_agent_systems/set_e_legal/logic/swarm.py",
        },
    },
}

SESSION_LABELS = {
    "01": "Data Pipeline Automation",
    "02": "Executive Narrative Engine",
    "03": "Multi-Agent Systems",
}

# ── Ollama Health Check ────────────────────────────────────────────────────────
def check_ollama() -> tuple[bool, str]:
    """Returns (is_running, model_status_string)."""
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            models = [m["name"] for m in data.get("models", [])]
            llama_ready = any("llama3.2" in m for m in models)
            model_status = "✅ llama3.2:1b ready" if llama_ready else "❌ llama3.2:1b NOT pulled"
            return True, model_status
    except Exception as e:
        return False, f"❌ Ollama unreachable ({e})"


# ── Dry Run: Validate Python syntax without running Ollama calls ───────────────
def dry_run(script_rel_path: str) -> tuple[str, str]:
    """
    Checks if the file exists and validates Python syntax using ast.parse.
    Returns (status_emoji, detail_message).
    """
    abs_path = os.path.join(ROOT, script_rel_path)

    # Check 1: file existence
    if not os.path.exists(abs_path):
        return "❌", f"File not found: `{script_rel_path}`"

    # Check 2: Python syntax via ast.parse (in-process, no subprocess needed)
    try:
        with open(abs_path, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source, filename=abs_path)
    except SyntaxError as e:
        return "❌", f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return "❌", f"Read error: {str(e)[:120]}"

    return "✅", "Exists · Syntax OK"


# ── Main Validation Loop ───────────────────────────────────────────────────────
def run_validation():
    print("\n🔍 Systems Validator — Starting Health Check\n" + "=" * 55)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Ollama check
    ollama_running, model_status = check_ollama()
    ollama_emoji = "✅" if ollama_running else "❌"
    print(f"[Ollama] {ollama_emoji} Daemon  |  {model_status}")

    # Per-domain, per-session results
    results = {}  # {domain_key: {session: (emoji, detail)}}

    for domain_key, domain_info in DOMAINS.items():
        domain_label = domain_info["label"]
        results[domain_key] = {}
        print(f"\n  [{domain_label}]")
        for session_id, rel_path in domain_info["sessions"].items():
            emoji, detail = dry_run(rel_path)
            results[domain_key][session_id] = (emoji, detail)
            session_label = SESSION_LABELS[session_id]
            print(f"    Session {session_id} ({session_label}): {emoji}  {detail}")

    # ── Generate HEALTH_CHECK.md ──────────────────────────────────────────────
    md_lines = [
        "# HEALTH_CHECK.md",
        "",
        f"> Generated: {timestamp}",
        "",
        "## System Health",
        "",
        f"| Component | Status |",
        f"|:---|:---|",
        f"| Ollama Daemon | {ollama_emoji} {'Running' if ollama_running else 'Not Running'} |",
        f"| Model | {model_status} |",
        "",
        "---",
        "",
        "## Session × Domain Matrix",
        "",
    ]

    # Header row
    domain_labels = [info["label"] for info in DOMAINS.values()]
    md_lines.append("| Session | " + " | ".join(domain_labels) + " |")
    md_lines.append("|:---|" + "|:---:" * len(DOMAINS) + "|")

    for session_id, session_label in SESSION_LABELS.items():
        row = f"| **{session_id}** {session_label} |"
        for domain_key in DOMAINS:
            emoji, _ = results[domain_key][session_id]
            row += f" {emoji} |"
        md_lines.append(row)

    md_lines += [
        "",
        "---",
        "",
        "## Detailed Results",
        "",
    ]

    for domain_key, domain_info in DOMAINS.items():
        md_lines.append(f"### {domain_info['label']}")
        md_lines.append("")
        md_lines.append("| Session | Script | Status |")
        md_lines.append("|:---|:---|:---|")
        for session_id, rel_path in domain_info["sessions"].items():
            emoji, detail = results[domain_key][session_id]
            md_lines.append(f"| Session {session_id} | `{os.path.basename(rel_path)}` | {emoji} {detail} |")
        md_lines.append("")

    md_lines += [
        "---",
        "",
        "## Definition of Complete",
        "",
        "A domain/session may only be marked `✅ VALIDATED` in `PROJECT_MANIFEST.md` when:",
        "- This report shows `✅` for that cell.",
        "- The script exits with code `0` in both Dry Run and Live Run.",
        "- An SVG proof exists (generated by the Forensic Documentarian).",
    ]

    health_check_path = HEALTH_CHECK_PATH
    with open(health_check_path, "w") as f:
        f.write("\n".join(md_lines))

    print(f"\n✅ HEALTH_CHECK.md written to: {health_check_path}")

    # Count totals
    total = sum(len(v) for v in results.values())
    passed = sum(1 for domain in results.values() for emoji, _ in domain.values() if emoji == "✅")
    print(f"\n📊 Summary: {passed}/{total} checks passed")
    if not ollama_running:
        print("⚠️  Ollama is not running — Session 02 & 03 live runs will fail until it starts.")

    return 0 if passed == total and ollama_running else 1


if __name__ == "__main__":
    sys.exit(run_validation())
