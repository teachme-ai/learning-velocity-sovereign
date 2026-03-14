class ModelRouter:
    ROUTES = {
        "local": {
            "json_context": "llama3.2:1b",
            "data_synth":   "qwen2.5:0.5b",
            "md_refine":    "llama3.2:latest",
            "timeline":     "llama3.2:latest",
            "general":      "llama3.2:1b"
        },
        "cloud": {
            "json_context": "gemini-1.5-flash",
            "data_synth":   "gemini-1.5-flash",
            "md_refine":    "gemini-1.5-flash",
            "timeline":     "gemini-1.5-flash",
            "general":      "gemini-1.5-flash"
        }
    }

    def __init__(self, engine_mode="local"):
        self.engine_mode = engine_mode
        self.usage = {}

    def get_model(self, task_type):
        routes = self.ROUTES.get(self.engine_mode, self.ROUTES["local"])
        model = routes.get(task_type) or routes.get("general")
        self.usage[task_type] = self.usage.get(task_type, 0) + 1
        return model

    def get_stats(self):
        return self.usage

    def override(self, task_type, model_name):
        self.ROUTES[self.engine_mode][task_type] = model_name
