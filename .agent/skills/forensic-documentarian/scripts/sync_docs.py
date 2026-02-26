import subprocess
import os
import re
import sys
import argparse
from pathlib import Path

try:
    from rich.console import Console
    from rich.terminal_theme import MONOKAI
except ImportError:
    print("Error: 'rich' package not found. Please run 'pip install rich playwright'")
    sys.exit(1)

# --- Configuration & Sessions ---
# Adding support for dynamic sessions via dictionary mapping
SESSIONS = {
    "01": {
        "name": "Session 01: Hybrid Sovereign Audit",
        "script": ["python3", "01_data_pipeline_automation/logic/cleaner.py"],
        "markdown": "01_data_pipeline_automation/01_data_pipeline_automation.md",
        "output_dir": "assets/proof/session_01",
        "regex": r'(## 📈 \[INTEGRATOR\] Proof of Work\n\*\*Focus\*\*: \*Operational implementation\.\*\n\nSuccessfully running `cleaner\.py` results in a hybrid summary\. Below is your target output:\n```text\n).*?(\n```)'
    },
    "01_healthcare": {
        "name": "Session 01: Healthcare Data Pipeline",
        "script": ["python3", "01_data_pipeline_automation/set_b_healthcare/logic/scrubber.py"],
        "markdown": "01_data_pipeline_automation/set_b_healthcare/01_healthcare_pipeline.md",
        "output_dir": "01_data_pipeline_automation/set_b_healthcare",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "01_supply_chain": {
        "name": "Session 01: Supply Chain Data Pipeline",
        "script": ["python3", "01_data_pipeline_automation/set_c_supply_chain/logic/inventory_validator.py"],
        "markdown": "01_data_pipeline_automation/set_c_supply_chain/01_supply_chain_pipeline.md",
        "output_dir": "01_data_pipeline_automation/set_c_supply_chain",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "02": {
        "name": "Session 02: Executive Narrative Engine",
        "script": ["python3", "02_executive_narrative_engine/logic/narrative_gen.py"],
        "markdown": "02_executive_narrative_engine/02_executive_narrative_engine.md",
        "output_dir": "assets/proof/session_02",
        "regex": None
    },
    "02_healthcare": {
        "name": "Session 02: Healthcare Narrative Engine",
        "script": ["python3", "02_executive_narrative_engine/set_b_healthcare/logic/compliance_gen.py"],
        "markdown": "02_executive_narrative_engine/set_b_healthcare/02_healthcare_narrative.md",
        "output_dir": "02_executive_narrative_engine/set_b_healthcare",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "02_supply_chain": {
        "name": "Session 02: Supply Chain Narrative Engine",
        "script": ["python3", "02_executive_narrative_engine/set_c_supply_chain/logic/risk_memo_gen.py"],
        "markdown": "02_executive_narrative_engine/set_c_supply_chain/02_supply_chain_narrative.md",
        "output_dir": "02_executive_narrative_engine/set_c_supply_chain",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "03": {
        "name": "Session 03: Multi-Agent Systems",
        "script": ["python3", "03_multi_agent_systems/logic/audit_flow_mock.py"],
        "markdown": "03_multi_agent_systems/03_multi_agent_systems.md",
        "output_dir": "assets/proof/session_03",
        "regex": r'(## 📈 \[INTEGRATOR\] Proof of Work\n\*\*Focus\*\*: \*Flow and Orchestration\.\*\n\nSuccessful committee orchestration results in a tiered deliberation\. Below is your target terminal proof:\n```text\n).*?(\n```)'
    },
    "03_finance": {
        "name": "Session 03: Multi-Agent Systems (Finance)",
        "script": ["python3", "03_multi_agent_systems/set_a_finance/logic/swarm.py"],
        "markdown": "03_multi_agent_systems/set_a_finance/03_finance_swarm.md",
        "output_dir": "03_multi_agent_systems/set_a_finance",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "03_healthcare": {
        "name": "Session 03: Multi-Agent Systems (Healthcare)",
        "script": ["python3", "03_multi_agent_systems/set_b_healthcare/logic/swarm.py"],
        "markdown": "03_multi_agent_systems/set_b_healthcare/03_healthcare_swarm.md",
        "output_dir": "03_multi_agent_systems/set_b_healthcare",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "03_supply_chain": {
        "name": "Session 03: Multi-Agent Systems (Supply Chain)",
        "script": ["python3", "03_multi_agent_systems/set_c_supply_chain/logic/swarm.py"],
        "markdown": "03_multi_agent_systems/set_c_supply_chain/03_supply_chain_swarm.md",
        "output_dir": "03_multi_agent_systems/set_c_supply_chain",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "01_edtech": {
        "name": "Session 01: EdTech Data Pipeline",
        "script": ["python3", "01_data_pipeline_automation/set_d_edtech/logic/velocity_cleaner.py"],
        "markdown": "01_data_pipeline_automation/set_d_edtech/01_edtech_pipeline.md",
        "output_dir": "01_data_pipeline_automation/set_d_edtech",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "02_edtech": {
        "name": "Session 02: EdTech Narrative Engine",
        "script": ["python3", "02_executive_narrative_engine/set_d_edtech/logic/velocity_memo_gen.py"],
        "markdown": "02_executive_narrative_engine/set_d_edtech/02_edtech_narrative.md",
        "output_dir": "02_executive_narrative_engine/set_d_edtech",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "01_legal": {
        "name": "Session 01: Legal Data Pipeline",
        "script": ["python3", "01_data_pipeline_automation/set_e_legal/logic/clause_scanner.py"],
        "markdown": "01_data_pipeline_automation/set_e_legal/01_legal_pipeline.md",
        "output_dir": "01_data_pipeline_automation/set_e_legal",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "02_legal": {
        "name": "Session 02: Legal Narrative Engine",
        "script": ["python3", "02_executive_narrative_engine/set_e_legal/logic/due_diligence_gen.py"],
        "markdown": "02_executive_narrative_engine/set_e_legal/02_legal_narrative.md",
        "output_dir": "02_executive_narrative_engine/set_e_legal",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "03_edtech": {
        "name": "Session 03: Multi-Agent Systems (EdTech)",
        "script": ["python3", "03_multi_agent_systems/set_d_edtech/logic/swarm.py"],
        "markdown": "03_multi_agent_systems/set_d_edtech/03_edtech_swarm.md",
        "output_dir": "03_multi_agent_systems/set_d_edtech",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "03_legal": {
        "name": "Session 03: Multi-Agent Systems (Legal)",
        "script": ["python3", "03_multi_agent_systems/set_e_legal/logic/swarm.py"],
        "markdown": "03_multi_agent_systems/set_e_legal/03_legal_swarm.md",
        "output_dir": "03_multi_agent_systems/set_e_legal",
        "regex": r'(### Validation Output\n).*?(---)'
    },
    "04": {
        "name": "Session 04: Sovereign Knowledge RAG",
        "script": ["python3", "04_sovereign_knowledge_rag/logic/rag_demo.py"],
        "markdown": "04_sovereign_knowledge_rag/04_sovereign_knowledge_rag.md",
        "output_dir": "assets/proof/session_04",
        "regex": None
    },
    "04_api": {
        "name": "Session 04: Sovereign RAG API (Integration)",
        "script": ["bash", "-c", "PYTHONPATH=/tmp/pylib_rag python3 -m uvicorn 04_sovereign_knowledge_rag.logic.api:app --host 0.0.0.0 --port 8000 & sleep 15 && curl -s -X POST http://localhost:8000/query -H 'Content-Type: application/json' -d '{\"query\":\"Why was international travel flagged?\"}' && kill %1"],
        "markdown": "04_sovereign_knowledge_rag/04_sovereign_knowledge_rag.md",
        "output_dir": "assets/proof/session_04",
        "regex": None
    }
}

def capture_output(cmd, cwd=None):
    """Run a shell command and capture the output."""
    try:
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            cwd=cwd
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print(f"Error output:\n{e.stderr}")
        return e.stdout.strip()

def update_markdown(md_path, new_output, regex_pattern):
    """Update the [INTEGRATOR] Proof of Work section with new execution output."""
    if not regex_pattern:
        print(f"Skip: No regex pattern defined for updating markdown in {md_path}")
        return True
        
    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found.")
        return False
        
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    pattern = re.compile(regex_pattern, re.DOTALL)
    
    if not pattern.search(md_content):
        print(f"Warning: Could not find the expected markdown structure to update in {md_path}.")
        return False

    new_content = pattern.sub(rf'\g<1>{new_output}\g<2>', md_content)
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {md_path} with new lab execution evidence.")
    return True

def save_proof(output_text, title, output_dir):
    """Export the terminal success message to a PNG or SVG using Rich."""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Render output using Rich
    console = Console(record=True, width=100)
    console.print(output_text)
    
    # Save as SVG (Native to Rich)
    svg_path = os.path.join(output_dir, "success.svg")
    console.save_svg(svg_path, title=title, theme=MONOKAI)
    print(f"Saved SVG validation to: {svg_path}")

def validate_session(session_id: str):
    root_dir = Path(__file__).parent.parent.parent.parent.parent
    
    if session_id not in SESSIONS:
        print(f"[Error] Unknown session: {session_id}. Available: {list(SESSIONS.keys())}")
        sys.exit(1)
        
    config = SESSIONS[session_id]
    print(f"\n=== Forensic Documentarian: Auditing {config['name']} ===")
    
    print("Executing Lab Logic...")
    output = capture_output(config['script'], cwd=str(root_dir))
    
    print("\nExecution Complete. Captured Output:")
    print("-" * 40)
    print(output)
    print("-" * 40)
    
    md_file_path = os.path.join(str(root_dir), config['markdown'])
    full_output_dir = os.path.join(str(root_dir), config['output_dir'])
    
    update_markdown(md_file_path, output, config['regex'])
    save_proof(output, config['name'], full_output_dir)
    print("=== Audit Process Completed ===\n")

def main():
    parser = argparse.ArgumentParser(description="Forensic Documentarian Lab Validator")
    parser.add_argument("--session", "-s", type=str, help="Session ID to run (e.g., '01', '02'). If omitted, runs all.", default=None)
    args = parser.parse_args()
    
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    if args.session:
        validate_session(args.session)
    else:
        print("Running all sessions...")
        for session_id in sorted(SESSIONS.keys()):
            validate_session(session_id)

if __name__ == "__main__":
    main()
