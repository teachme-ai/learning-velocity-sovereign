#!/usr/bin/env python3
"""
tools/inject_footers.py
=======================
Automates injecting a standard Navigation Footer into all 30 lab manuals.

Footer format:
---
**[Back to Curriculum Hub] | [Previous Lab] | [Next Lab]**
"""

import os
import glob
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Shared lab manuals for Sessions 05 and 06
SHARED_LABS = {
    5: ROOT / "05_advanced_ui_lobechat" / "05_advanced_ui_lobechat.md",
    6: ROOT / "06_observability" / "06_sovereign_tracing.md"
}

# The domains and their folder abbreviations
DOMAINS = {
    "finance": "set_a_finance",
    "healthcare": "set_b_healthcare",
    "supply_chain": "set_c_supply_chain",
    "edtech": "set_d_edtech",
    "legal": "set_e_legal"
}

def get_lab_path(session: int, domain: str) -> Path:
    """Calculates the absolute path to a lab manual for a given domain and session."""
    if session == 5:
        return SHARED_LABS[5]
    if session == 6:
        return SHARED_LABS[6]
        
    # Special cases for Finance (Set A) early sessions which sit at the root
    if domain == "finance":
        if session == 1:
            return ROOT / "01_data_pipeline_automation" / "01_data_pipeline_automation.md"
        if session == 2:
            return ROOT / "02_executive_narrative_engine" / "02_executive_narrative_engine.md"
            
    session_folders = {
        1: "01_data_pipeline_automation",
        2: "02_executive_narrative_engine",
        3: "03_multi_agent_systems",
        4: "04_sovereign_knowledge_rag"
    }
    
    set_folder = DOMAINS[domain]
    filename = f"{session:02d}_{domain}_"
    if session == 1: filename += "pipeline.md"
    elif session == 2: filename += "narrative.md"
    elif session == 3: filename += "swarm.md"
    elif session == 4: filename += "rag.md"
        
    return ROOT / session_folders[session] / set_folder / filename

def get_relative_link(source_path: Path, target_path: Path) -> str:
    """Calculates relative link from source_path's DIRECTORY to target_path."""
    try:
        # relative_to calculates from the source file, but we need from the source directory
        # so os.path.relpath is safer
        rel = os.path.relpath(target_path, source_path.parent)
        return rel
    except ValueError:
        return str(target_path)

def generate_footer(session: int, domain: str, current_path: Path) -> str:
    """Generates the Markdown footer string with dynamically calculated relative links."""
    hub_link = get_relative_link(current_path, ROOT / "README.md")
    
    parts = [f"[Back to Curriculum Hub]({hub_link})"]
    
    # Previous Lab link
    if session > 1:
        prev_path = get_lab_path(session - 1, domain)
        prev_link = get_relative_link(current_path, prev_path)
        parts.append(f"[Previous Lab: Session {session-1:02d}]({prev_link})")
    else:
        parts.append("~~Previous Lab~~")
        
    # Next Lab link
    if session < 6:
        next_path = get_lab_path(session + 1, domain)
        next_link = get_relative_link(current_path, next_path)
        parts.append(f"[Next Lab: Session {session+1:02d}]({next_link})")
    else:
        parts.append("~~Next Lab~~")
        
    links_str = " | ".join(parts)
    
    return f"\n\n---\n**{links_str}**\n"

def inject_footer(path: Path, footer: str):
    """Appends the footer to the file if it's not already there."""
    if not path.exists():
        print(f"⚠️  File not found: {path}")
        return
        
    content = path.read_text(encoding="utf-8")
    
    # Simple check to avoid double-injecting
    if "[Back to Curriculum Hub]" in content:
        print(f"⏭️  Skipped (footer already exists): {path.name}")
        return
        
    content = content.rstrip() + footer
    path.write_text(content, encoding="utf-8")
    print(f"✅ Injected footer into: {path.name}")

def main():
    print(f"🚀 Injecting Navigation Footers...\n{'='*40}")
    count = 0
    # Process domains
    for domain in DOMAINS.keys():
        print(f"\n[{domain.upper()}]")
        for session in range(1, 5):
            path = get_lab_path(session, domain)
            footer = generate_footer(session, domain, path)
            inject_footer(path, footer)
            count += 1
            
    # Process Shared Sessions (05 and 06) just once with generic non-domain links
    # For shared sessions, "Previous" and "Next" don't strictly follow a single domain path.
    # To keep it simple, we link back to the HUB as the primary action from shared labs.
    print(f"\n[SHARED SESSIONS]")
    shared_footer = "\n\n---\n**[Back to Curriculum Hub](../README.md)**\n"
    for session in [5, 6]:
        path = get_lab_path(session, "finance") # path logic ignores domain for 5/6
        if not path.exists(): continue
        content = path.read_text(encoding="utf-8")
        if "[Back to Curriculum Hub]" not in content:
            path.write_text(content.rstrip() + shared_footer, encoding="utf-8")
            print(f"✅ Injected shared footer into: {path.name}")
            count += 1
        else:
            print(f"⏭️  Skipped shared (footer exists): {path.name}")
            
    print(f"\n🎉 Done! Processed {count} files.")

if __name__ == "__main__":
    main()
