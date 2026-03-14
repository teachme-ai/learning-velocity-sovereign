import sys
import os
import json
import yaml
from datetime import datetime

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

try:
    from _factory.core.compiler import FactoryCompiler
except (ImportError, ModuleNotFoundError):
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from core.compiler import FactoryCompiler

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 factory_compiler.py <manifest.yaml> [--mode local|cloud] [--force]")
        sys.exit(1)

    engine_mode = "local"
    if "--mode" in sys.argv:
        mode_idx = sys.argv.index("--mode") + 1
        if mode_idx < len(sys.argv):
            engine_mode = sys.argv[mode_idx]

    force = "--force" in sys.argv

    compiler = FactoryCompiler(sys.argv[1], engine_mode=engine_mode)

    # Context cache path — stable across warm builds
    context_cache_path = os.path.join("_factory", "cache", f"{compiler.slug}_context.json")
    os.makedirs(os.path.dirname(context_cache_path), exist_ok=True)

    if force:
        compiler.logger.log("Force rebuild: cache cleared")
        compiler.cache.invalidate()
        compiler.generate_llm_context()
        with open(context_cache_path, "w") as f:
            json.dump(compiler.context, f)
        compiler.run_data_synth()
    elif os.path.exists(context_cache_path) and len(compiler.cache.hashes) > 0:
        compiler.logger.log("Warm build: loading cached context, skipping data synthesis")
        with open(context_cache_path) as f:
            compiler.context.update(json.load(f))
    else:
        compiler.logger.log("Cold build: generating LLM context and data")
        compiler.generate_llm_context()
        with open(context_cache_path, "w") as f:
            json.dump(compiler.context, f)
        compiler.run_data_synth()

    pass_arg = None
    if "--pass" in sys.argv:
        pass_idx = sys.argv.index("--pass") + 1
        if pass_idx < len(sys.argv):
            pass_arg = sys.argv[pass_idx]

    if pass_arg == "1":
        compiler.compile_pass1()
    elif pass_arg == "2":
        compiler.compile_pass2()
    else:
        compiler.compile()
