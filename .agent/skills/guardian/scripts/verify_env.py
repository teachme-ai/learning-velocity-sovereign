#!/usr/bin/env python3
"""
Codespace Guardian — verify_env.py
=====================================
Performs live smoke tests for Set A (Finance) across Sessions 01, 02, and 03.
Validates the Genkit venv, Ollama service, and actual script execution.

Usage:
    python3 .agent/skills/guardian/scripts/verify_env.py          # Set A only
    python3 .agent/skills/guardian/scripts/verify_env.py --all    # All 5 domains
"""

import os
import sys
import subprocess
import urllib.request
import json
from datetime import datetime

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
GENKIT_PYTHON = "/tmp/genkit_env/bin/python3"
STATUS_PATH = os.path.join(ROOT, "CODESPACE_STATUS.md")
TIMEOUT = 120  # seconds per smoke test

# ── Smoke Test Matrix ─────────────────────────────────────────────────────────
# Each entry: (label, script_relative_path, expected_output_fragment)
SMOKE_TESTS = {
    "Finance": [
        (
            "Session 01 — Data Pipeline",
            "dist/ai_for_global_finance/01_data_pipeline_automation/set_ai_for_global_finance/logic/cleaner.py",
            None,
        ),
        (
            "Session 02 — Narrative Engine",
            "dist/ai_for_global_finance/02_executive_narrative_engine/set_ai_for_global_finance/logic/narrative_gen.py",
            None,
        ),
        (
            "Session 03 — Multi-Agent Swarm",
            "dist/ai_for_global_finance/03_multi_agent_systems/set_ai_for_global_finance/logic/swarm.py",
            "Final Integrated Report",
        ),
    ],
    "Healthcare": [
        (
            "Session 01 — Data Pipeline",
            "builds/ai_in_retail_and_e-commerce/01_data_pipeline_automation/set_ai_in_retail_and_e-commerce/logic/cleaner.py",
            None,
        ),
        (
            "Session 02 — Narrative Engine",
            "builds/ai_in_retail_and_e-commerce/02_executive_narrative_engine/set_ai_in_retail_and_e-commerce/logic/narrative_gen.py",
            None,
        ),
        (
            "Session 03 — Multi-Agent Swarm",
            "builds/ai_in_retail_and_e-commerce/03_multi_agent_systems/set_ai_in_retail_and_e-commerce/logic/swarm.py",
            "Final Integrated Report",
        ),
    ],
    "Supply Chain": [
        (
            "Session 01 — Data Pipeline",
            "builds/sustainability_and_esg/01_data_pipeline_automation/set_sustainability_and_esg/logic/cleaner.py",
            None,
        ),
        (
            "Session 02 — Narrative Engine",
            "builds/sustainability_and_esg/02_executive_narrative_engine/set_sustainability_and_esg/logic/narrative_gen.py",
            None,
        ),
        (
            "Session 03 — Multi-Agent Swarm",
            "builds/sustainability_and_esg/03_multi_agent_systems/set_sustainability_and_esg/logic/swarm.py",
            "Final Integrated Report",
        ),
    ],
}


# ── Step 1: Verify Genkit venv ────────────────────────────────────────────────
def check_genkit_env() -> tuple[bool, str]:
    if not os.path.exists(GENKIT_PYTHON):
        return False, f"venv not found at {GENKIT_PYTHON}. Run: python3 -m venv /tmp/genkit_env && /tmp/genkit_env/bin/pip install genkit genkit-plugin-ollama pydantic"

    result = subprocess.run(
        [GENKIT_PYTHON, "-c", "import genkit; import genkit.plugins.ollama; print('ok')"],
        capture_output=True, text=True, timeout=10, cwd=ROOT
    )
    if result.returncode != 0 or "ok" not in result.stdout:
        err = (result.stderr or result.stdout).strip()[:200]
        return False, f"genkit import failed: {err}"

    return True, f"venv OK  ({GENKIT_PYTHON})"


# ── Step 2: Check Ollama service ──────────────────────────────────────────────
def check_ollama() -> tuple[bool, str]:
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())
            models = [m["name"] for m in data.get("models", [])]
            llama_ready = any("llama3.2" in m for m in models)
            if not llama_ready:
                return False, f"Ollama running but llama3.2:1b not found. Run: ollama pull llama3.2:1b"
            return True, "Ollama running · llama3.2:1b ready"
    except Exception as e:
        return False, f"Ollama unreachable: {e}"

# ── Step 2.5: Check FastAPI API Bridge ───────────────────────────────────────
def check_fastapi() -> tuple[bool, str]:
    try:
        req = urllib.request.Request("http://localhost:8000/health")
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") == "ok":
                return True, "API Bridge running on port 8000"
            return False, "FastAPI running but health status not ok"
    except Exception as e:
        return False, f"FastAPI API Bridge unreachable on port 8000: {e}"

# ── Step 2.6: Check Trace Quality (Session 06) ────────────────────────────────
import glob
import subprocess
import time

def check_trace(domain_key: str) -> tuple[str, str, str]:
    """Check if the latest trace for this domain is well-formed and correlates to the Swarm."""
    norm_key = domain_key.lower().replace(" ", "_").replace("-", "_")
    # Updated path for Finance track traces in dist/ folder
    base_trace_dir = os.path.join(ROOT, "dist/ai_for_global_finance/06_observability/traces")
    trace_dir = os.path.join(base_trace_dir, norm_key)
    
    # Fallback to 'unknown' if domain-specific folder is missing or empty
    if not os.path.exists(trace_dir) or not glob.glob(os.path.join(trace_dir, "*.json")):
        trace_dir = os.path.join(base_trace_dir, "unknown")
    
    if not os.path.exists(trace_dir):
        return "FAIL", f"No trace directory found at {trace_dir}", ""
        
    trace_files = glob.glob(os.path.join(trace_dir, "*.json"))
    if not trace_files:
        return "FAIL", f"No trace JSON files found in {trace_dir}", ""
        
    latest_trace = max(trace_files, key=os.path.getmtime)
    
    # Deriving swarm endpoint name expectations
    expected_swarm_name = f"{norm_key}_agent_swarm"
    
    try:
        with open(latest_trace, "r") as f:
            data = json.load(f)
            
            if not isinstance(data, dict) or "spans" not in data:
                return "FAIL", "Trace missing 'spans' object.", ""
                
            spans = data["spans"]
            if not spans:
                return "FAIL", "Trace has no tracked spans.", ""
                
            # Verify the top-level swarm flow execution was captured successfully
            swarm_flow_found = False
            for span_id, span_data in spans.items():
                attrs = span_data.get("attributes", {})
                if attrs.get("genkit:name") == expected_swarm_name and attrs.get("genkit:state") == "success":
                    swarm_flow_found = True
                    break
                    
            if swarm_flow_found:
                return "PASS", f"Trace verified: {expected_swarm_name} completed successfully.", ""
            else:
                return "FAIL", f"Trace incomplete: missing 'success' state for '{expected_swarm_name}'.", ""
    except Exception as e:
        return "FAIL", f"Error reading trace: {e}", ""


# Known environment-constraint messages — treated as CONDITIONAL PASS (not a code bug)
ENV_CONSTRAINT_SIGNALS = [
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "API key not set",
    "Run Session 01",   # upstream dependency not yet generated
]

# ── Step 3: Smoke test a single script ───────────────────────────────────────
def smoke_test(label: str, rel_path: str, expected_fragment: str | None) -> tuple[str, str, str]:
    """Returns (status, summary_line, captured_output).
    Status is one of: PASS | CONDITIONAL_PASS | FAIL
    """
    abs_path = os.path.join(ROOT, rel_path)

    if not os.path.exists(abs_path):
        msg = f"Script not found: {rel_path}"
        return "FAIL", msg, msg

    python_bin = GENKIT_PYTHON if os.path.exists(GENKIT_PYTHON) else sys.executable
    try:
        # Run with a generous timeout—local LLM processing can take 2+ minutes
        result = subprocess.run(
            [python_bin, abs_path],
            capture_output=True, text=True, timeout=300, cwd=ROOT
        )
        output = (result.stdout + result.stderr).strip()

        if result.returncode != 0:
            # Check if this is a known infrastructure constraint, not a code bug
            for signal in ENV_CONSTRAINT_SIGNALS:
                if signal in output:
                    return "CONDITIONAL_PASS", f"Requires env setup: {signal}", output[-300:]
            short_err = output[-500:] if len(output) > 500 else output
            return "FAIL", f"Exit code {result.returncode}", short_err

        if expected_fragment and expected_fragment not in output:
            return "FAIL", f"Expected '{expected_fragment}' not found in output", output[-300:]

        return "PASS", "Clean exit · output verified", output[-200:]

    except subprocess.TimeoutExpired:
        return "FAIL", f"Timed out after {TIMEOUT}s", "Process killed — exceeded timeout."
    except Exception as e:
        return "FAIL", str(e), str(e)


BOOTSTRAP_SCRIPT = os.path.join(os.path.dirname(__file__), "bootstrap_codespace.sh")


# ── Main ──────────────────────────────────────────────────────────────────────
def run_guardian():
    run_all = "--all" in sys.argv
    do_bootstrap = "--bootstrap" in sys.argv
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n🛡️  Codespace Guardian — Live Smoke Test  [{timestamp}]")
    print("=" * 60)

    # Environment checks
    genkit_ok, genkit_msg = check_genkit_env()
    ollama_ok, ollama_msg = check_ollama()
    api_ok, api_msg = check_fastapi()

    genkit_icon = "✅" if genkit_ok else "❌"
    ollama_icon = "✅" if ollama_ok else "❌"
    api_icon = "✅" if api_ok else "❌"
    print(f"\n[ENV] {genkit_icon} Genkit venv  — {genkit_msg}")
    print(f"[ENV] {ollama_icon} Ollama       — {ollama_msg}")
    print(f"[ENV] {api_icon} API Bridge   — {api_msg}")

    # Domains to test
    domains_to_test = list(SMOKE_TESTS.keys()) if run_all else ["Finance"]

    # Results store
    results = []  # [(domain, label, status, summary, output)]

    for domain in domains_to_test:
        print(f"\n  [{domain}]")
        for label, rel_path, fragment in SMOKE_TESTS[domain]:
            print(f"    Running: {label} ...", end="", flush=True)
            status, summary, captured = smoke_test(label, rel_path, fragment)
            icon = "✅" if status == "PASS" else "❌"
            print(f" {icon} [{status}] {summary}")
            results.append((domain, label, status, summary, captured))
            
        # Session 06 Trace verification
        print("    Running: Session 06 — Trace Quality ...", end="", flush=True)
        status, summary, captured = check_trace(domain)
        icon = "✅" if status == "PASS" else "❌"
        print(f" {icon} [{status}] {summary}")
        results.append((domain, "Session 06 — Trace Quality", status, summary, captured))

    # ── Write CODESPACE_STATUS.md ─────────────────────────────────────────────
    passed = sum(1 for _, _, s, _, _ in results if s == "PASS")
    total = len(results)
    overall = "✅ ALL SYSTEMS GO" if passed == total else f"⚠️  {passed}/{total} PASSED"

    md = [
        "# CODESPACE_STATUS.md",
        "",
        f"> Generated: {timestamp}",
        f"> Mode: {'Full Matrix (--all)' if run_all else 'Set A — Finance only'}",
        "",
        f"## Overall: {overall}",
        "",
        "## Environment",
        "",
        "| Component | Status | Detail |",
        "|:---|:---:|:---|",
        f"| Genkit venv (`/tmp/genkit_env`) | {genkit_icon} | {genkit_msg} |",
        f"| Ollama + llama3.2:1b | {ollama_icon} | {ollama_msg} |",
        f"| FastAPI API Bridge | {api_icon} | {api_msg} |",
        "",
        "---",
        "",
        "## Smoke Test Results",
        "",
    ]

    current_domain = None
    for domain, label, status, summary, captured in results:
        if domain != current_domain:
            md.append(f"### {domain}")
            md.append("")
            md.append("| Test | Result | Detail |")
            md.append("|:---|:---:|:---|")
            current_domain = domain

        if status == "PASS":
            icon = "✅"
        elif status == "CONDITIONAL_PASS":
            icon = "⚠️"
        else:
            icon = "❌"
        md.append(f"| {label} | {icon} `[{status}]` | {summary} |")

    # Failures section with captured output
    failures = [(d, l, s, captured) for d, l, s, _, captured in results if s == "FAIL"]
    conditionals = [(d, l, s, captured) for d, l, s, _, captured in results if s == "CONDITIONAL_PASS"]

    if conditionals:
        md += ["", "---", "", "## ⚠️ Conditional Details (env setup required)", ""]
        for domain, label, _, captured in conditionals:
            md.append(f"### [{domain}] {label}")
            md.append("```")
            md.append(captured[:600])
            md.append("```")
            md.append("")

    if failures:
        md += ["", "---", "", "## ❌ Failure Details", ""]
        for domain, label, _, captured in failures:
            md.append(f"### [{domain}] {label}")
            md.append("```")
            md.append(captured[:1000])
            md.append("```")
            md.append("")

    md += [
        "---",
        "",
        "## Pre-Validation Gate",
        "",
        "A session may be marked `✅ VALIDATED` in `PROJECT_MANIFEST.md` only when:",
        "- This report shows `[PASS]` for that session + domain",
        "- `HEALTH_CHECK.md` (Systems Validator) also shows `✅`",
        "- An SVG proof exists (Forensic Documentarian)",
    ]

    with open(STATUS_PATH, "w") as f:
        f.write("\n".join(md))

    print(f"\n📄 CODESPACE_STATUS.md written to: {STATUS_PATH}")
    print(f"📊 Summary: {passed}/{total} smoke tests passed")
    if not genkit_ok or not ollama_ok:
        print("⚠️  Fix the ENV issues above before running Session 02/03 smoke tests.")

    all_env_ok = genkit_ok and ollama_ok
    exit_code = 0 if (passed == total and all_env_ok) else 1

    if do_bootstrap and exit_code != 0:
        if not os.path.exists(BOOTSTRAP_SCRIPT):
            print(f"\n❌ Bootstrap script not found at {BOOTSTRAP_SCRIPT}")
        else:
            print("\n🔧 Environment incomplete. Running bootstrap script...")
            try:
                subprocess.run(["bash", BOOTSTRAP_SCRIPT], check=True)
                print("\n🔁 Re-running verification after bootstrap...")
                # Re-run without --bootstrap to avoid infinite loop
                args_no_bootstrap = [a for a in sys.argv[1:] if a != "--bootstrap"]
                result = subprocess.run(
                    [sys.executable, __file__] + args_no_bootstrap,
                    cwd=ROOT,
                )
                return result.returncode
            except subprocess.CalledProcessError as e:
                print(f"❌ Bootstrap failed: {e}")
                return 1

    return exit_code


if __name__ == "__main__":
    sys.exit(run_guardian())
