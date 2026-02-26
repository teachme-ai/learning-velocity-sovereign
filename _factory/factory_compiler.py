import os
import yaml
import json
import shutil
import ollama
import subprocess
import sys
from jinja2 import Environment, FileSystemLoader

class FactoryCompiler:
    def __init__(self, manifest_path):
        with open(manifest_path, 'r') as f:
            self.manifest = yaml.safe_load(f)
        
        self.industry = self.manifest.get('industry', 'Generic AI')
        self.slug = self.industry.lower().replace(' ', '_').replace('&', 'and')
        self.build_dir = os.path.join('builds', self.slug)
        self.template_dir = os.path.join('_factory', 'templates')
        
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.context = {
            'industry_name': self.industry,
            'industry_slug': self.slug,
            'tracks': self.manifest.get('tracks', ['base', 'integrated', 'architect'])
        }

    def generate_llm_context(self):
        """Use Ollama to generate industry-specific jargon and scenarios."""
        print(f"🚀 Generating LLM context for {self.industry}...")
        prompt = f"""
        You are an expert AI curriculum architect. Generate industry-specific context for an AI Bootcamp focused on {self.industry}.
        Return ONLY a JSON object with this exact structure:
        {{
            "terminology": ["term1", "term2", "term3", "term4", "term5"],
            "data_scenario": "A short 2-sentence description of an industry-specific data challenge.",
            "dataset_name": "filename_without_spaces.csv",
            "primary_color": "#HEXCODE"
        }}
        Do not include any other text before or after the JSON.
        """
        try:
            response = ollama.chat(model='llama3.2:1b', messages=[
                {'role': 'user', 'content': prompt}
            ], format='json')
            
            raw_content = response['message']['content']
            llm_data = json.loads(raw_content)
            self.context.update(llm_data)
            print("✅ Context generated.")
        except Exception as e:
            print(f"❌ Failed to parse LLM JSON: {e}")
            if 'raw_content' in locals():
                print(f"DEBUG: Raw content: {raw_content}")
            # Fallback data
            self.context.update({
                "terminology": ["AI Automation", "Data Pipeline", "Predictive Analytics", "Machine Learning", "Neural Networks"],
                "data_scenario": f"Optimizing operations in {self.industry} using automated AI pipelines.",
                "dataset_name": f"{self.slug}_data.csv",
                "primary_color": "#007bff"
            })
            print("⚠️ Using fallback context.")

    def run_data_synth(self):
        """Trigger the data synthesis skill."""
        print(f"🧬 Synthesizing data for {self.industry}...")
        synth_script = os.path.join(os.path.dirname(__file__), "../.agent/skills/factory/data_synth.py")
        try:
            subprocess.run([sys.executable, synth_script, self.slug, self.industry], check=True)
            print("✅ Data synthesis complete.")
        except Exception as e:
            print(f"⚠️ Data synthesis failed: {e}. Build might lack custom data.")

    def run_context_refiner(self, dest_path):
        """Trigger the linguistic refinement skill for markdown files."""
        refiner_script = os.path.join(os.path.dirname(__file__), "../.agent/skills/factory/context_refiner.py")
        try:
            subprocess.run([sys.executable, refiner_script, dest_path, self.industry, self.slug], check=True)
        except Exception as e:
            print(f"⚠️ Context refinement failed for {dest_path}: {e}")

    def generate_build_tests(self):
        """Generate a portable tests.py for the specific build."""
        print("🛡️ Generating Portable Guardian tests...")
        test_content = f"""import os
import pandas as pd

def test_data_schema():
    path = "01_data_pipeline_automation/set_{self.slug}/data/corporate_expenses.csv"
    if not os.path.exists(path):
        print("❌ Data file missing!")
        return False
    df = pd.read_csv(path)
    expected_cols = ['transaction_id', 'date', 'employee_id', 'department', 'category', 'description', 'amount_usd']
    # Check if a subset of columns exist (since synth might be slightly off)
    actual_cols = df.columns.tolist()
    missing = [c for c in expected_cols if c not in actual_cols]
    if missing:
        print(f"⚠️ Missing columns: {{missing}}")
        return False
    print("✅ Data schema validated.")
    return True

def test_sessions_exist():
    sessions = ['01_data_pipeline_automation', '07_sovereign_security', '08_grand_capstone']
    for s in sessions:
        if not os.path.exists(s):
            print(f"❌ Session {{s}} folder missing!")
            return False
    print("✅ Session structure validated.")
    return True

if __name__ == "__main__":
    print(f"🛡️ Running Build Validation for {{os.getcwd()}}")
    s1 = test_data_schema()
    s2 = test_sessions_exist()
    if s1 and s2:
        print("🌟 BUILD STATUS: PASS")
    else:
        print("🚨 BUILD STATUS: WARNING (Incomplete or schema mismatch)")
"""
        with open(os.path.join(self.build_dir, "tests.py"), 'w') as f:
            f.write(test_content)
        print("✅ Portable Guardian tests generated.")

    def compile(self):
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)

        print(f"📦 Compiling {self.industry} to {self.build_dir}...")
        
        for root, dirs, files in os.walk(self.template_dir):
            # Skip hidden folders and environments
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('.venv', '__pycache__')]
            
            for file in files:
                # Skip hidden files
                if file.startswith('.'):
                    continue
                
                # Get relative path from template dir
                rel_path = os.path.relpath(os.path.join(root, file), self.template_dir)
                
                # Render the PATH itself (allows set_{{ industry_slug }} to work)
                rendered_rel_path = self.env.from_string(rel_path).render(self.context)
                dest_path = os.path.join(self.build_dir, rendered_rel_path)
                
                # Ensure dest dir exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Render if it's a code/markdown file, else just copy
                if file.endswith(('.md', '.py', '.txt', '.json', '.yaml', '.sh')):
                    try:
                        template = self.env.get_template(rel_path)
                        rendered = template.render(self.context)
                        with open(dest_path, 'w') as f:
                            f.write(rendered)
                        
                        # Apply context refiner to manuals
                        if file.endswith('.md'):
                            self.run_context_refiner(dest_path)
                            
                    except Exception as e:
                        print(f"⚠️ Could not render {rel_path}, copying instead. Error: {e}")
                        shutil.copy2(os.path.join(root, file), dest_path)
                else:
                    shutil.copy2(os.path.join(root, file), dest_path)

        print(f"🎉 Build complete: {self.build_dir}")
        self.generate_readme()
        self.generate_build_tests()

    def generate_readme(self):
        """Generate a build-specific README.md reflecting the triple-track structure."""
        print("📝 Generating Build README...")
        readme_content = f"""# AI Bootcamp: {{ industry_name }}

This repository contains a localized, generative AI curriculum focused on **{{ industry_name }}**.

## 🛤️ Triple-Track Matrix

| Session | 🟢 Base (No-Code) | 🟡 Integrated (Low-Code) | 🔴 Architect (High-Code) |
| :--- | :--- | :--- | :--- |
| **01: Data Pipeline** | [Manual](00_base_track_creators/session_01/README.md) | [Notebook](01_data_pipeline_automation/README.md) | [Code](01_data_pipeline_automation/set_{{ industry_slug }}/logic/cleaner.py) |
| **02: Narrative** | [Manual](00_base_track_creators/session_02/README.md) | [Notebook](02_executive_narrative_engine/README.md) | [Code](02_executive_narrative_engine/set_{{ industry_slug }}/logic/narrative_gen.py) |
| **03: Swarms** | [Manual](00_base_track_creators/session_03/README.md) | [Notebook](03_multi_agent_systems/README.md) | [Code](03_multi_agent_systems/set_{{ industry_slug }}/logic/swarm.py) |
| **04: RAG** | [Manual](00_base_track_creators/session_04/README.md) | [Notebook](04_sovereign_knowledge_rag/README.md) | [Code](04_sovereign_knowledge_rag/set_{{ industry_slug }}/logic/ingest_and_query.py) |
| **05: UI/UX** | [Manual](00_base_track_creators/session_05/README.md) | [Notebook](05_advanced_ui_lobechat/05_advanced_ui_lobechat.md) | [Code](05_advanced_ui_lobechat/logic/multi_domain_api.py) |
| **06: Observability** | [Manual](00_base_track_creators/session_06_observability.md) | [Notebook](06_observability/06_sovereign_tracing.md) | [Code](06_observability/traces) |
| **07: Security** | [Manual](07_sovereign_security/README.md) | [Notebook](07_sovereign_security/07_sovereign_security.md) | [Code](07_sovereign_security/set_{{ industry_slug }}/logic/pii_scrubber.py) |
| **08: Capstone** | [Manual](08_grand_capstone/README.md) | [Notebook](08_grand_capstone/08_grand_capstone.md) | [Code](08_grand_capstone/set_{{ industry_slug }}/logic/dashboard.py) |

---
*Created by the Learning Velocity Curriculum Factory.*
"""
        template = self.env.from_string(readme_content)
        rendered = template.render(self.context)
        with open(os.path.join(self.build_dir, "README.md"), 'w') as f:
            f.write(rendered)
        print("✅ README.md generated.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 factory_compiler.py <manifest.yaml>")
        sys.exit(1)
    
    compiler = FactoryCompiler(sys.argv[1])
    compiler.generate_llm_context()
    compiler.run_data_synth()
    compiler.compile()
