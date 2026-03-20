"""
Cost Tracker — records per-call token usage and cost across the build pipeline.
Produces cost_report.json at end of build.
"""
import json
import os
from datetime import datetime


class CostTracker:
    USD_TO_INR = 85.0

    PRICING = {
        "gemini-2.0-flash-lite": {"input": 0.10, "output": 0.40},
        "gemini-2.0-flash":      {"input": 0.10, "output": 0.40},
        "gemini-2.5-flash-lite": {"input": 0.075, "output": 0.30},
        "gemini-2.5-flash":      {"input": 0.15, "output": 0.60},
        "gemini-2.5-pro":        {"input": 1.25, "output": 10.00},
    }

    def __init__(self):
        self.calls = []
        self.start_time = datetime.now()

    def _cost(self, model, input_tokens, output_tokens):
        pricing = self.PRICING.get(model)
        if not pricing:
            if "ollama" in model or "llama" in model or "qwen" in model or "gemma" in model:
                return 0.0
            pricing = self.PRICING["gemini-2.0-flash"]
        return (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000

    def record(self, task_type, model, input_tokens, output_tokens):
        cost = self._cost(model, input_tokens, output_tokens)
        self.calls.append({
            "task_type": task_type,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
        })

    def total_cost(self):
        return sum(c["cost"] for c in self.calls)

    def total_tokens(self):
        return sum(c["input_tokens"] + c["output_tokens"] for c in self.calls)

    def report(self):
        by_task = {}
        for c in self.calls:
            t = c["task_type"]
            if t not in by_task:
                by_task[t] = {"calls": 0, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}
            by_task[t]["calls"] += 1
            by_task[t]["input_tokens"] += c["input_tokens"]
            by_task[t]["output_tokens"] += c["output_tokens"]
            by_task[t]["cost_usd"] += c["cost"]
        for t in by_task:
            by_task[t]["cost_inr"] = round(by_task[t]["cost_usd"] * self.USD_TO_INR, 4)
        total_usd = self.total_cost()
        return {
            "build_time": str(datetime.now() - self.start_time),
            "total_calls": len(self.calls),
            "total_tokens": self.total_tokens(),
            "total_cost_usd": round(total_usd, 6),
            "total_cost_inr": round(total_usd * self.USD_TO_INR, 4),
            "by_task": by_task,
        }

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.report(), f, indent=2)
