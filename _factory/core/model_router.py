"""
Model Router — cascading model selection with cost awareness.
Cloud: Flash-Lite for structured/cheap tasks, Flash for quality-critical.
Local: task-specific Ollama models by capability.
"""


class ModelRouter:
    ROUTES = {
        "local": {
            "json_context": "llama3.2:1b",
            "data_synth":   "qwen2.5:0.5b",
            "md_refine":    "llama3.2:latest",
            "timeline":     "llama3.2:latest",
            "general":      "llama3.2:1b",
        },
        "cloud": {
            "json_context": "gemini-2.5-flash-lite",
            "data_synth":   "gemini-2.5-flash-lite",
            "md_refine":    "gemini-2.5-flash",
            "timeline":     "gemini-2.5-flash-lite",
            "general":      "gemini-2.5-flash",
        },
    }

    PRICING = {
        "gemini-2.5-flash-lite": {"input": 0.075, "output": 0.30},
        "gemini-2.5-flash":      {"input": 0.15,  "output": 0.60},
        "gemini-2.5-pro":        {"input": 1.25,  "output": 10.00},
    }

    def __init__(self, engine_mode="local"):
        self.engine_mode = engine_mode
        self.usage = {}

    def get_model(self, task_type):
        routes = self.ROUTES.get(self.engine_mode, self.ROUTES["local"])
        model = routes.get(task_type) or routes.get("general")
        self.usage[task_type] = self.usage.get(task_type, 0) + 1
        return model

    def get_pricing(self, model):
        return self.PRICING.get(model, {"input": 0.0, "output": 0.0})

    def get_stats(self):
        return self.usage

    def override(self, task_type, model_name):
        self.ROUTES[self.engine_mode][task_type] = model_name
