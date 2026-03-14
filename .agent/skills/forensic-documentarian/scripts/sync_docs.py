import subprocess
import os
import re
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("Error: 'pyyaml' package not found. Please run 'pip install pyyaml'")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.terminal_theme import MONOKAI
except ImportError:
    print("Error: 'rich' package not found. Please run 'pip install rich'")
    sys.exit(1)

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../"))
SESSIONS_YAML = os.path.join(SKILL_DIR, "sessions.yaml")
EXEC_LOG = os.path.join(SKILL_DIR, "execution_log.jsonl")


def load_sessions(slug: str | None = None) -> dict:
    """Load session configs from sessions.yaml, resolving {slug} placeholders."""
    with open(SESSIONS_YAML, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    sessions = data.get("sessions", {})

    if slug:
        # Resolve {slug} placeholders in all string fields and list elements
        resolved = {}
        for sid, cfg in sessions.items():
            resolved[sid] = {}
            for key, val in cfg.items():
                if isinstance(val, str):
                    resolved[sid][key] = val.replace("{slug}", slug)
                elif isinstance(val, list):
                    resolved[sid][key] = [
                        v.replace("{slug}", slug) if isinstance(v, str) else v
                        for v in val
                    ]
                else:
                    resolved[sid][key] = val
        return resolved

    return sessions


def build_heading_regex(heading: str) -> str:
    """Build a regex that matches the proof block under a given markdown heading."""
    escaped = re.escape(heading)
    # Match: heading ... ```text\n <content> \n```
    return rf"({escaped}.*?```text\n).*?(\n```)"


def capture_output(cmd: list, cwd: str = None) -> str:
    """Run a command and capture stdout; returns combined output on failure."""
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300,
            cwd=cwd,
        )
        if result.returncode != 0:
            print(f"Command exited with code {result.returncode}")
            print(result.stderr[:500] if result.stderr else "")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print("Command timed out after 300s")
        return "[TIMEOUT: script exceeded 300s]"
    except Exception as e:
        print(f"Command error: {e}")
        return f"[ERROR: {e}]"


def update_markdown(md_path: str, new_output: str, regex_pattern: str | None, proof_heading: str | None) -> bool:
    """Update the Proof of Work section in a markdown file."""
    if not os.path.exists(md_path):
        print(f"Warning: markdown not found at {md_path}")
        return False

    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Determine which regex to use
    pattern_str = regex_pattern
    if not pattern_str and proof_heading:
        pattern_str = build_heading_regex(proof_heading)

    if not pattern_str:
        print(f"Skip: No regex or proof_heading defined for {md_path}")
        return True

    pattern = re.compile(pattern_str, re.DOTALL)
    if not pattern.search(content):
        print(f"Warning: Proof of Work section not found in {md_path}")
        return False

    new_content = pattern.sub(rf"\g<1>{new_output}\g<2>", content)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated: {md_path}")
    return True


def save_proof(output_text: str, title: str, output_dir: str) -> str:
    """Save timestamped SVG proof and maintain a latest.svg copy."""
    os.makedirs(output_dir, exist_ok=True)

    console = Console(record=True, width=100)
    console.print(output_text)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    svg_path = os.path.join(output_dir, f"success_{timestamp}.svg")
    latest_path = os.path.join(output_dir, "latest.svg")

    console.save_svg(svg_path, title=title, theme=MONOKAI)
    shutil.copy2(svg_path, latest_path)
    print(f"Proof saved: {svg_path}")
    print(f"Latest:      {latest_path}")
    return svg_path


def append_execution_log(session_id: str, industry: str, status: str, proof_path: str):
    """Append a JSON record to execution_log.jsonl."""
    record = {
        "timestamp": datetime.now().isoformat(),
        "session": session_id,
        "industry": industry,
        "status": status,
        "proof": proof_path,
    }
    with open(EXEC_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def validate_session(session_id: str, sessions: dict, industry_slug: str):
    if session_id not in sessions:
        print(f"[Error] Unknown session: {session_id}. Available: {list(sessions.keys())}")
        return

    config = sessions[session_id]
    print(f"\n=== Forensic Documentarian: Auditing {config['name']} ===")

    output = capture_output(config["script"], cwd=ROOT)

    print("\nCapture complete:")
    print("-" * 40)
    print(output[:1000] if len(output) > 1000 else output)
    print("-" * 40)

    md_path = os.path.join(ROOT, config["markdown"])
    output_dir = os.path.join(ROOT, config["output_dir"])

    md_ok = update_markdown(
        md_path,
        output,
        config.get("regex"),
        config.get("proof_heading"),
    )

    proof_path = save_proof(output, config["name"], output_dir)
    status = "pass" if md_ok and not output.startswith("[ERROR") and not output.startswith("[TIMEOUT") else "fail"
    append_execution_log(session_id, industry_slug, status, proof_path)
    print("=== Audit Complete ===\n")


def main():
    parser = argparse.ArgumentParser(description="Forensic Documentarian Lab Validator")
    parser.add_argument(
        "--session", "-s",
        type=str,
        help="Session ID to run (e.g. '01', '03'). Omit to run all.",
        default=None,
    )
    args = parser.parse_args()

    # TARGET_INDUSTRY lets the factory pipeline scope execution to one industry
    industry_slug = os.environ.get("TARGET_INDUSTRY")

    sessions = load_sessions(slug=industry_slug)

    if not sessions:
        print("No sessions loaded. Check sessions.yaml.")
        sys.exit(1)

    if args.session:
        validate_session(args.session, sessions, industry_slug or "unknown")
    else:
        print(f"Running all sessions{f' for {industry_slug}' if industry_slug else ''}...")
        for sid in sorted(sessions.keys()):
            validate_session(sid, sessions, industry_slug or "unknown")


if __name__ == "__main__":
    main()
