import os
import json
import hashlib


class BuildCache:
    def __init__(self, cache_dir="_factory/cache"):
        self.cache_file = os.path.join(cache_dir, "hashes.json")
        os.makedirs(cache_dir, exist_ok=True)
        try:
            with open(self.cache_file, "r") as f:
                self.hashes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.hashes = {}

    def _compute_hash(self, template_path, context):
        with open(template_path, "r", encoding="utf-8", errors="ignore") as f:
            file_content = f.read()
        context_str = json.dumps(context, sort_keys=True)
        combined = file_content + context_str
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def is_cached(self, rel_path, template_path, context):
        try:
            computed = self._compute_hash(template_path, context)
            return self.hashes.get(rel_path) == computed
        except Exception:
            return False

    def mark_cached(self, rel_path, template_path, context):
        try:
            self.hashes[rel_path] = self._compute_hash(template_path, context)
        except Exception:
            pass

    def save(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.hashes, f, indent=2)

    def invalidate(self, rel_path=None):
        if rel_path:
            self.hashes.pop(rel_path, None)
        else:
            self.hashes = {}
        self.save()
