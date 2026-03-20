"""
Semantic Cache — vector-similarity response caching over BuildCache.
Falls back to exact-match hashing if sentence_transformers not installed.
Install: pip install sentence-transformers
"""
import hashlib
import json
import os

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    _HAS_EMBEDDINGS = True
except ImportError:
    _HAS_EMBEDDINGS = False


class SemanticCache:
    def __init__(self, cache_dir="_factory/.semantic_cache", similarity_threshold=0.85):
        self.cache_dir = cache_dir
        self.threshold = similarity_threshold
        self.model = None
        self.stats = {"hits": 0, "misses": 0, "stores": 0}
        os.makedirs(cache_dir, exist_ok=True)
        if _HAS_EMBEDDINGS:
            try:
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
            except Exception:
                pass

    @property
    def available(self):
        return self.model is not None

    def _hash(self, text):
        return hashlib.sha256(text.encode()).hexdigest()[:16]

    def _embed(self, text):
        if not self.available:
            return None
        return self.model.encode(text, normalize_embeddings=True)

    def _index_path(self):
        return os.path.join(self.cache_dir, "index.json")

    def _load_index(self):
        path = self._index_path()
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return {}

    def _save_index(self, index):
        with open(self._index_path(), "w") as f:
            json.dump(index, f)

    def get(self, prompt, task_type="general"):
        h = self._hash(prompt + task_type)
        index = self._load_index()
        # Exact match first
        if h in index:
            entry_path = os.path.join(self.cache_dir, index[h]["file"])
            if os.path.exists(entry_path):
                self.stats["hits"] += 1
                with open(entry_path) as f:
                    return json.load(f).get("response")
        # Semantic match (if embeddings available)
        if self.available and len(index) > 0:
            query_emb = self._embed(prompt)
            for key, meta in index.items():
                if meta.get("task_type") != task_type:
                    continue
                emb_path = os.path.join(self.cache_dir, f"{key}.emb.npy")
                if os.path.exists(emb_path):
                    stored_emb = np.load(emb_path)
                    sim = float(np.dot(query_emb, stored_emb))
                    if sim >= self.threshold:
                        entry_path = os.path.join(self.cache_dir, meta["file"])
                        if os.path.exists(entry_path):
                            self.stats["hits"] += 1
                            with open(entry_path) as f:
                                return json.load(f).get("response")
        self.stats["misses"] += 1
        return None

    def put(self, prompt, task_type, response):
        h = self._hash(prompt + task_type)
        index = self._load_index()
        entry_file = f"{h}.json"
        with open(os.path.join(self.cache_dir, entry_file), "w") as f:
            json.dump({"prompt_hash": h, "task_type": task_type, "response": response}, f)
        if self.available:
            emb = self._embed(prompt)
            np.save(os.path.join(self.cache_dir, f"{h}.emb.npy"), emb)
        index[h] = {"file": entry_file, "task_type": task_type}
        self._save_index(index)
        self.stats["stores"] += 1

    def get_stats(self):
        return self.stats
