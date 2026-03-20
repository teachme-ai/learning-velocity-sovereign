"""
Prompt Compressor — LLMLingua-2 wrapper for input token reduction.
Gracefully degrades to no-op if llmlingua not installed.
Install: pip install llmlingua
"""

try:
    from llmlingua import PromptCompressor as _LLMLingua
    _HAS_LLMLINGUA = True
except ImportError:
    _HAS_LLMLINGUA = False


class FactoryCompressor:
    def __init__(self, target_ratio=0.5, min_length=500):
        self.target_ratio = target_ratio
        self.min_length = min_length
        self.compressor = None
        self.stats = {"calls": 0, "skipped": 0, "compressed": 0, "tokens_saved": 0}
        if _HAS_LLMLINGUA:
            try:
                self.compressor = _LLMLingua(model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank")
            except Exception:
                pass

    @property
    def available(self):
        return self.compressor is not None

    def compress(self, prompt, task_type="general"):
        self.stats["calls"] += 1
        est_tokens = len(prompt) // 4
        if not self.available or est_tokens < self.min_length:
            self.stats["skipped"] += 1
            return prompt
        if task_type in ("json_context", "data_synth"):
            self.stats["skipped"] += 1
            return prompt
        try:
            result = self.compressor.compress_prompt(prompt, rate=self.target_ratio)
            compressed = result.get("compressed_prompt", prompt)
            saved = est_tokens - (len(compressed) // 4)
            self.stats["compressed"] += 1
            self.stats["tokens_saved"] += max(0, saved)
            return compressed
        except Exception:
            self.stats["skipped"] += 1
            return prompt

    def get_stats(self):
        return self.stats
