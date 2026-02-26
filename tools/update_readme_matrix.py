import re

with open("README.md", "r") as f:
    content = f.read()

def rewrite_cell(session_num, domain_idx, domain_key, existing_link_path):
    if session_num > 5 and session_num != 6:
        return "*Architecting*"
    
    # Base track paths
    base_tracks = {
        1: f"00_base_track_creators/session_01/set_{chr(97+domain_idx)}_{domain_key}/01_{domain_key}_nocode.md",
        2: f"00_base_track_creators/session_02/set_{chr(97+domain_idx)}_{domain_key}/02_{domain_key}_nocode.md",
        3: f"00_base_track_creators/session_03/set_{chr(97+domain_idx)}_{domain_key}/03_{domain_key}_nocode.md",
        4: f"00_base_track_creators/session_04/set_{chr(97+domain_idx)}_{domain_key}/04_{domain_key}_nocode.md",
        5: f"00_base_track_creators/session_05/set_{chr(97+domain_idx)}_{domain_key}/05_{domain_key}_nocode.md"
    }
    
    if session_num <= 5:
        base_link = f"[Base]({base_tracks[session_num]})"
        # Integrated & Architect share the same file
        int_link = f"[Int]({existing_link_path})"
        arch_link = f"[Arch]({existing_link_path})"
        return f"{base_link}<br>{int_link}<br>{arch_link}"
    elif session_num == 6:
        return f"*Architecting*<br>[Int]({existing_link_path})<br>[Arch]({existing_link_path})"

domains = ["finance", "healthcare", "supply_chain", "edtech", "legal"]

new_table = """| Session | 🏦 Finance (Set A) | 🏥 Healthcare (Set B) | 📦 Supply Chain (Set C) | 🎓 EdTech (Set D) | ⚖️ Legal (Set E) |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""

rows = [
    ("01 Pipeline", ["01_data_pipeline_automation/01_data_pipeline_automation.md", "01_data_pipeline_automation/set_b_healthcare/01_healthcare_pipeline.md", "01_data_pipeline_automation/set_c_supply_chain/01_supply_chain_pipeline.md", "01_data_pipeline_automation/set_d_edtech/01_edtech_pipeline.md", "01_data_pipeline_automation/set_e_legal/01_legal_pipeline.md"]),
    ("02 Narrative", ["02_executive_narrative_engine/02_executive_narrative_engine.md", "02_executive_narrative_engine/set_b_healthcare/02_healthcare_narrative.md", "02_executive_narrative_engine/set_c_supply_chain/02_supply_chain_narrative.md", "02_executive_narrative_engine/set_d_edtech/02_edtech_narrative.md", "02_executive_narrative_engine/set_e_legal/02_legal_narrative.md"]),
    ("03 Swarm", ["03_multi_agent_systems/set_a_finance/03_finance_swarm.md", "03_multi_agent_systems/set_b_healthcare/03_healthcare_swarm.md", "03_multi_agent_systems/set_c_supply_chain/03_supply_chain_swarm.md", "03_multi_agent_systems/set_d_edtech/03_edtech_swarm.md", "03_multi_agent_systems/set_e_legal/03_legal_swarm.md"]),
    ("04 RAG", ["04_sovereign_knowledge_rag/set_a_finance/04_finance_rag.md", "04_sovereign_knowledge_rag/set_b_healthcare/04_healthcare_rag.md", "04_sovereign_knowledge_rag/set_c_supply_chain/04_supply_chain_rag.md", "04_sovereign_knowledge_rag/set_d_edtech/04_edtech_rag.md", "04_sovereign_knowledge_rag/set_e_legal/04_legal_rag.md"]),
    ("05 Cockpit UI", ["05_advanced_ui_lobechat/05_advanced_ui_lobechat.md"] * 5),
    ("06 Observability", ["06_observability/06_sovereign_tracing.md"] * 5),
    ("07 Identity", [""] * 5),
    ("08 Capstone", [""] * 5)
]

for s_idx, (s_name, existing_paths) in enumerate(rows, start=1):
    cells = []
    for d_idx, d_key in enumerate(domains):
        cells.append(rewrite_cell(s_idx, d_idx, d_key, existing_paths[d_idx]))
    new_table += f"| **{s_name}** | {' | '.join(cells)} |\n"

# Replace the table in the README using regex
pattern = re.compile(r'\| Session \| 🏦 Finance \(Set A\) \|.*\| \*\*08 Capstone\*\* \| \*Architecting\* \| \*Architecting\* \| \*Architecting\* \| \*Architecting\* \| \*Architecting\* \|', re.DOTALL)
new_content = pattern.sub(new_table.strip(), content)

with open("README.md", "w") as f:
    f.write(new_content)

print("✅ Successfully updated the Curriculum Matrix in README.md")
