"""
Tool Memory — persistent cross-build cache for tool research results.
TTL-based expiry with revision notification lifecycle:
  Day 25: revision_recommended
  Day 28: revision_urgent
  Day 30: expired (auto-refresh on next build)
"""
import json
import os
from datetime import datetime, timedelta


MEMORY_PATH = os.path.join(os.path.dirname(__file__), "..", ".tool_memory.json")


class ToolMemory:
    def __init__(self, memory_path=None):
        self.path = memory_path or MEMORY_PATH
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                return json.load(f)
        return {}

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def _key(self, industry, use_cases):
        uc = "|".join(sorted(use_cases)) if use_cases else ""
        return f"{industry.lower().strip()}::{uc}"

    def _age_days(self, entry):
        created = datetime.fromisoformat(entry["created"])
        return (datetime.now() - created).days

    def status(self, industry, use_cases):
        key = self._key(industry, use_cases)
        entry = self.data.get(key)
        if not entry:
            return "missing"
        age = self._age_days(entry)
        if age >= 30:
            return "expired"
        if age >= 28:
            return "revision_urgent"
        if age >= 25:
            return "revision_recommended"
        return "fresh"

    def recall(self, industry, use_cases):
        key = self._key(industry, use_cases)
        entry = self.data.get(key)
        if not entry:
            return None
        if self._age_days(entry) >= 30:
            return None
        return entry["tools"]

    def remember(self, industry, use_cases, tools):
        key = self._key(industry, use_cases)
        self.data[key] = {
            "industry": industry,
            "use_cases": use_cases,
            "tools": tools,
            "created": datetime.now().isoformat(),
        }
        self._save()

    def forget(self, industry=None):
        if industry is None:
            self.data = {}
        else:
            keys = [k for k in self.data if k.startswith(industry.lower().strip())]
            for k in keys:
                del self.data[k]
        self._save()

    def all_entries(self):
        result = []
        for key, entry in self.data.items():
            result.append({
                "industry": entry["industry"],
                "use_cases": entry.get("use_cases", []),
                "tool_count": len(entry.get("tools", [])),
                "age_days": self._age_days(entry),
                "status": self.status(entry["industry"], entry.get("use_cases", [])),
            })
        return result
