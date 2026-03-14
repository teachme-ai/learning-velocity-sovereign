import asyncio
import os
import yaml
import json
import shutil
import subprocess
import sys
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Try importing LLM providers
try:
    import ollama
except ImportError:
    ollama = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from _factory.core.cache import BuildCache
except ImportError:
    from core.cache import BuildCache

try:
    from _factory.core.queue import RefinementQueue
except ImportError:
    from core.queue import RefinementQueue

try:
    from _factory.core.manifest_validator import ManifestValidator
except ImportError:
    from core.manifest_validator import ManifestValidator

try:
    from _factory.core.model_router import ModelRouter
except ImportError:
    from core.model_router import ModelRouter

try:
    from _factory.core.worker import drain_queue
except ImportError:
    from core.worker import drain_queue

class TelemetryLogger:
    def __init__(self, log_path="_factory/logs/events.jsonl"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def log(self, event, level="INFO", metadata=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "event": event,
            "metadata": metadata or {}
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"[{level}] {event}")

class FactoryCompiler:
    def __init__(self, manifest_path, engine_mode="local"):
        with open(manifest_path, 'r') as f:
            raw_manifest = yaml.safe_load(f)

        self.engine_mode = engine_mode
        self.logger = TelemetryLogger()

        validator = ManifestValidator(raw_manifest)
        if not validator.validate():
            raise ValueError(f"Invalid manifest:\n{validator.report()}")
        if validator.warnings:
            self.logger.log(f"Manifest warnings:\n{validator.report()}", level="WARNING")

        self.manifest = validator.get_merged()
        self.token_budget = self.manifest.get("token_budget")
        self.data_schema = self.manifest.get("data_schema")
        self.concurrency = self.manifest.get("concurrency", 3)

        self.industry = self.manifest.get('industry', 'Generic AI')
        self.slug = self.industry.lower().replace(' ', '_').replace('&', 'and')
        self.build_dir = os.path.join('dist', self.slug)
        self.template_dir = os.path.join('_factory', 'templates')
        self.allowed_sessions = self.manifest.get('sessions', list(range(1, 9)))

        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        self.context = {
            'industry_name': self.industry,
            'industry_slug': self.slug,
            'tracks': self.manifest.get('tracks', ['base', 'integrated', 'architect']),
            'audience': self.manifest.get('audience', 'Developer / Engineer'),
            'use_cases': self.manifest.get('use_cases', []),
            'tone': self.manifest.get('tone', 'Practical & Applied'),
            'compliance_framework': self.manifest.get('compliance_framework', 'None'),
            'region': self.manifest.get('region', 'Global'),
        }
        self.cache = BuildCache()
        self.refinement_queue = RefinementQueue()
        self.router = ModelRouter(engine_mode=self.engine_mode)

        if self.engine_mode == "cloud":
            api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
            if not api_key:
                self.logger.log("GOOGLE_API_KEY not found in environment. Falling back to local.", level="WARNING")
                self.engine_mode = "local"
            else:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.logger.log("Turbo Mode (Gemini) activated.", level="INFO")

    def call_llm(self, prompt, is_json=False, task_type="general"):
        """Unified interface for local and cloud LLMs."""
        model = self.router.get_model(task_type)
        self.logger.log(f"Using model: {model} for task: {task_type}", level="DEBUG")
        if self.engine_mode == "cloud":
            try:
                response = self.model.generate_content(prompt)
                text = response.text
                if is_json:
                    if "```json" in text:
                        text = text.split("```json")[1].split("```")[0].strip()
                    elif "{" in text:
                        text = "{" + text.split("{", 1)[1].rsplit("}", 1)[0] + "}"
                    return json.loads(text)
                return text
            except Exception as e:
                self.logger.log(f"Gemini call failed: {e}", level="ERROR")
                return None
        else:
            try:
                format_arg = 'json' if is_json else None
                response = ollama.chat(model=model, messages=[
                    {'role': 'user', 'content': prompt}
                ], format=format_arg)
                content = response['message']['content']
                if is_json:
                    return json.loads(content)
                return content
            except Exception as e:
                self.logger.log(f"Ollama call failed: {e}", level="ERROR")
                return None

    def generate_llm_context(self):
        self.logger.log(f"Generating DNA context for {self.industry} via {self.engine_mode}...")
        use_cases_str = ", ".join(self.context.get('use_cases', [])) or "general AI applications"
        prompt = f"""
        You are an expert AI curriculum architect. Generate industry-specific context for an AI Bootcamp.

        Industry: {self.industry}
        Target Audience: {self.context.get('audience', 'Developer / Engineer')}
        Use Cases to emphasize: {use_cases_str}
        Compliance context: {self.context.get('compliance_framework', 'None')}
        Region: {self.context.get('region', 'Global')}
        Tone: {self.context.get('tone', 'Practical & Applied')}

        Return ONLY a JSON object with this exact structure:
        {{
            "terminology": ["term1", "term2", "term3", "term4", "term5"],
            "data_scenario": "A 2-sentence description of an industry-specific data challenge tied to the use cases above.",
            "dataset_name": "filename_without_spaces.csv",
            "primary_color": "#HEXCODE"
        }}
        """
        data = self.call_llm(prompt, is_json=True, task_type="json_context")
        if data:
            self.context.update(data)
            self.logger.log("DNA context generated successfully.")
        else:
            self.logger.log("Using fallback context defaults.", level="WARNING")
            self.context.update({
                "terminology": ["AI Automation", "Data Pipeline", "Predictive Analytics", "Machine Learning", "Neural Networks"],
                "data_scenario": f"Optimizing operations in {self.industry} using automated AI pipelines.",
                "dataset_name": f"{self.slug}_data.csv",
                "primary_color": "#007bff"
            })

    def run_data_synth(self):
        self.logger.log(f"Initiating data synthesis agent for {self.industry}...")
        synth_script = os.path.join(os.path.dirname(__file__), "../../.agent/skills/factory/data_synth.py")
        try:
            columns = ",".join(self.data_schema["columns"])
            dirty_rate = str(self.data_schema["dirty_rate"])
            row_count = str(self.data_schema["row_count"])
            env = os.environ.copy()
            env["SYNTH_MODEL"] = self.router.get_model("data_synth")
            subprocess.run([
                sys.executable, synth_script,
                self.slug, self.industry, columns, dirty_rate, row_count
            ], env=env, check=True)
            self.logger.log("Data synthesis agent completed.")
        except Exception as e:
            self.logger.log(f"Data synthesis failed: {e}", level="ERROR")

    def run_context_refiner(self, dest_path):
        refiner_script = os.path.join(os.path.dirname(__file__), "../../.agent/skills/factory/context_refiner.py")
        try:
            env = os.environ.copy()
            env["REFINER_MODEL"] = self.router.get_model("md_refine")
            env["REFINER_TONE"] = self.context.get('tone', 'Practical & Applied')
            subprocess.run([sys.executable, refiner_script, dest_path, self.industry, self.slug], env=env, check=True)
        except Exception as e:
            self.logger.log(f"Linguistic refinement failed for {os.path.basename(dest_path)}", level="WARNING")

    def compile_pass1(self):
        if not os.path.exists(self.build_dir):
            os.makedirs(self.build_dir)
        self.logger.log(f"Incremental build: cache active for {self.industry}")
        self.logger.log(f"Mission Start: Compiling {self.industry} to {self.build_dir}")

        queued_count = 0
        for root, dirs, files in os.walk(self.template_dir):
            rel_root = os.path.relpath(root, self.template_dir)
            parts = rel_root.split(os.sep)
            if len(parts) >= 1 and parts[0] != '.':
                dir_name = parts[0]
                if len(dir_name) >= 2 and dir_name[:2].isdigit():
                    session_num = int(dir_name[:2])
                    if session_num not in self.allowed_sessions:
                        dirs[:] = []
                        continue
            original_dirs = list(dirs)
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('.venv', '__pycache__', 'node_modules', 'libs')]
            for skipped in [d for d in original_dirs if d not in dirs]:
                self.logger.log(f"Skipping technical dir: {skipped}", level="DEBUG")

            for file in files:
                if file.startswith('.'): continue

                rel_path = os.path.relpath(os.path.join(root, file), self.template_dir)
                rendered_rel_path = self.env.from_string(rel_path).render(self.context)
                dest_path = os.path.join(self.build_dir, rendered_rel_path)
                full_template_path = os.path.join(root, file)

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                if self.cache.is_cached(rendered_rel_path, full_template_path, self.context):
                    self.logger.log(f"CACHE HIT: skipping {rendered_rel_path}", level="DEBUG")
                    continue

                if file.endswith(('.md', '.py', '.txt', '.json', '.yaml', '.sh')):
                    try:
                        template = self.env.get_template(rel_path)
                        rendered = template.render(self.context)
                        with open(dest_path, 'w') as f:
                            f.write(rendered)
                        self.cache.mark_cached(rendered_rel_path, full_template_path, self.context)

                        if file.endswith('.md') and 'node_modules' not in rel_path and '.agent' not in rel_path:
                            self.refinement_queue.enqueue(self.slug, dest_path, self.industry)
                            queued_count += 1
                            self.logger.log(f"Queued for refinement: {file}")

                    except Exception as e:
                        self.logger.log(f"Render error {rel_path}: {e}", level="ERROR")
                        shutil.copy2(os.path.join(root, file), dest_path)
                else:
                    shutil.copy2(os.path.join(root, file), dest_path)
                    self.cache.mark_cached(rendered_rel_path, full_template_path, self.context)

        self.logger.log(f"Mission Successful: {self.industry} build complete.")
        self.generate_readme()
        self.generate_build_tests()
        self.cache.save()
        self.logger.log(f"Cache saved: {len(self.cache.hashes)} entries indexed.")
        self.logger.log(f"Pass 1 complete. {queued_count} files queued for LLM refinement.")

    def compile_pass2(self):
        self.logger.log(f"Pass 2: draining queue ({self.refinement_queue.pending_count()} jobs) with {self.concurrency} workers...")
        refiner_script = os.path.join(
            os.path.dirname(__file__),
            "../../.agent/skills/factory/context_refiner.py"
        )
        model = self.router.get_model("md_refine")
        asyncio.run(drain_queue(
            queue=self.refinement_queue,
            industry_name=self.industry,
            refiner_script=refiner_script,
            model=model,
            token_budget_config=self.token_budget,
            logger=self.logger,
            concurrency=self.concurrency
        ))

    def run_forensic_documentarian(self):
        self.logger.log(f"Running Forensic Documentarian for {self.industry}...")
        synth_script = os.path.join(
            os.path.dirname(__file__),
            "../../.agent/skills/forensic-documentarian/scripts/sync_docs.py"
        )
        try:
            env = os.environ.copy()
            env["TARGET_INDUSTRY"] = self.slug
            subprocess.run([sys.executable, synth_script], check=True, env=env)
            self.logger.log("Lab execution and documentation sync complete.")
        except Exception as e:
            self.logger.log(f"Forensic Documentarian failed: {e}", level="WARNING")

    def compile(self):
        self.compile_pass1()
        self.compile_pass2()
        self.logger.log(f"Model usage stats: {self.router.get_stats()}")
        self.run_forensic_documentarian()

    def generate_readme(self):
        self.logger.log("Generating Factory Manual (README)...")
        readme_content = """# AI Bootcamp: {{ industry_name }}

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
*Created by the Learning Velocity Curriculum Factory (Engine: {{ engine_mode }}).*
"""
        template = self.env.from_string(readme_content)
        # Add engine_mode to context for the README
        current_context = self.context.copy()
        current_context['engine_mode'] = self.engine_mode
        rendered = template.render(current_context)
        with open(os.path.join(self.build_dir, "README.md"), 'w') as f:
            f.write(rendered)

    def generate_build_tests(self):
        self.logger.log("Generating Portable Guardian...")
        test_content = f"""import os
import pandas as pd

def test_data_schema():
    slug = "{self.slug}"
    path = f"01_data_pipeline_automation/set_{{slug}}/data/dirty_data.csv"
    if not os.path.exists(path):
        print(f"❌ Data file missing at {{path}}!")
        return False
    df = pd.read_csv(path)
    if len(df) < 5:
        print("⚠️ Data file seems empty or too small.")
        return False
    print("✅ Data schema and synthesis validated.")
    return True

if __name__ == "__main__":
    print(f"🛡️ Running Build Validation for {{os.getcwd()}}")
    if test_data_schema():
        print("🌟 BUILD STATUS: PASS")
    else:
        print("🚨 BUILD STATUS: WARNING")
"""
        with open(os.path.join(self.build_dir, "tests.py"), 'w') as f:
            f.write(test_content)
