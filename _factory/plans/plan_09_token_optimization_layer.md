# Plan 09 — Token Optimization Layer

## Goal
Reduce token consumption by 40-60% across the entire factory pipeline using four proven optimization strategies, add cost tracking, and implement model cascading. This is a standalone infrastructure plan — every current and future plan benefits automatically.

## Problem Statement
The factory pipeline is output-heavy (full lab manuals, narratives, data scenarios). Every `call_llm()` sends uncompressed prompts, gets verbose responses, never caches semantically similar requests, and re-researches tools already validated in prior builds. Cloud mode also ignores the model router (hardcodes `gemini-2.0-flash` for all tasks) and has zero cost visibility.

## Six Components

### Category 1: LLMLingua-2 (Input Compression) — Microsoft
Compress long markdown/context sections before sending to LLM. Drop-in wrapper around `call_llm()`.
- `pip install llmlingua`
- 40-50% input token savings on context-heavy prompts
- Wraps around the universal `call_llm()` chokepoint in `compiler.py`

### Category 2: GPT Semantic Cache (Response Caching)
Upgrade existing `BuildCache` with vector-similarity matching. Similar industries ("AI for Healthcare" vs "AI for Pharma") get partial cache hits.
- Avoids redundant LLM calls for semantically equivalent prompts
- Especially valuable for repeated builds across the 5 industry tracks

### Category 3: Skeleton-of-Thought (Output Control)
Restructure the refiner to: (a) ask LLM for section skeleton first, (b) expand each section with constrained token budget. Controls output verbosity, enables parallel generation.
- Reduces output tokens by structuring generation
- Enables parallel expansion of skeleton sections

### Category 4: Memori Memory Layer (Tool Research Memory)
Memory layer for `tool_researcher.py` (and future agents). Avoids re-researching tools already validated in previous builds.
- Persistent memory across builds
- Especially valuable for the session planner pipeline (persona + tools + planning)

### Category 5: Cost Tracking & Reporting
Track per-call token usage and cost. Produce `cost_report.json` at end of every build.
- Per-task breakdown (json_context, data_synth, md_refine, etc.)
- Dollar amounts using actual Gemini pricing
- Ollama calls tracked at $0.00

### Category 6: Model Cascading (Flash-Lite vs Flash)
Route cheap/structured tasks to Flash-Lite, quality tasks to Flash. Fix the bug where cloud mode ignores the router.
- `json_context`, `data_synth`, `timeline` → Flash-Lite ($0.10/1M input)
- `md_refine`, `general` → Flash ($0.10/1M input, better output quality)
- Fix `call_llm()` to actually use `router.get_model()` for cloud calls

## Files to Create / Modify

| # | File | Action | Component | Purpose |
|---|------|--------|-----------|---------|
| 1 | `_factory/core/cost_tracker.py` | CREATE | Cat 5 | Token usage accumulator + cost report generator |
| 2 | `_factory/core/prompt_compressor.py` | CREATE | Cat 1 | LLMLingua-2 wrapper for input compression |
| 3 | `_factory/core/semantic_cache.py` | CREATE | Cat 2 | Vector-similarity cache layer over BuildCache |
| 4 | `_factory/core/skeleton_refiner.py` | CREATE | Cat 3 | Skeleton-of-Thought output generation pattern |
| 5 | `_factory/core/tool_memory.py` | CREATE | Cat 4 | Persistent memory for tool research results |
| 6 | `_factory/core/model_router.py` | MODIFY | Cat 6 | Add cascading cloud routes + pricing table |
| 7 | `_factory/core/gemini_rest.py` | MODIFY | Cat 5 | Return usageMetadata from API response |
| 8 | `_factory/core/compiler.py` | MODIFY | All | Wire all components into call_llm() + build pipeline |
| 9 | `_factory/core/worker.py` | MODIFY | Cat 5 | Use actual token counts instead of estimates |
| 10 | `_factory/core/tool_researcher.py` | MODIFY | Cat 4 | Integrate tool_memory for cross-build persistence |

## Detailed Changes

### File 1: `_factory/core/cost_tracker.py` (CREATE)

```python
class CostTracker:
    PRICING = {
        "gemini-2.0-flash-lite": {"input": 0.10, "output": 0.40},
        "gemini-2.0-flash":      {"input": 0.10, "output": 0.40},
        "gemini-2.5-flash":      {"input": 0.15, "output": 0.60},
        "ollama":                {"input": 0.00, "output": 0.00},
    }
    def __init__(self): ...
    def record(self, task_type, model, input_tokens, output_tokens): ...
    def total_cost(self): ...
    def report(self): ...  # per-task breakdown + totals
    def save(self, path): ...  # write cost_report.json
```

### File 2: `_factory/core/prompt_compressor.py` (CREATE)

```python
from llmlingua import PromptCompressor
class FactoryCompressor:
    def __init__(self, target_ratio=0.5): ...
    def compress(self, prompt, task_type="general"): ...
    # Skip compression for short prompts (<500 tokens)
    # Skip for JSON-mode prompts (structure matters)
    # Return compressed text + compression stats
```

### File 3: `_factory/core/semantic_cache.py` (CREATE)

```python
class SemanticCache:
    def __init__(self, cache_dir, similarity_threshold=0.85): ...
    def get(self, prompt_hash, prompt_embedding): ...
    def put(self, prompt_hash, prompt_embedding, response): ...
    # Uses sentence-transformers for embedding (lightweight)
    # Falls back to exact-match if embeddings unavailable
```

### File 4: `_factory/core/skeleton_refiner.py` (CREATE)

```python
class SkeletonRefiner:
    def refine(self, content, industry, llm_caller): ...
    # Step 1: Generate skeleton (section headers + 1-line summaries)
    # Step 2: Expand each section with constrained token budget
    # Step 3: Assemble final output
    # Enables parallel expansion of independent sections
```

### File 5: `_factory/core/tool_memory.py` (CREATE)

```python
class ToolMemory:
    def __init__(self, memory_path="_factory/.tool_memory.json"): ...
    def recall(self, industry, use_cases): ...  # return cached tools if fresh
    def remember(self, industry, use_cases, tools, ttl_days=30): ...
    def forget(self, industry=None): ...  # clear stale entries
    # JSON file persistence — no external DB needed
    # TTL-based expiry (tools go stale after 30 days)
```

### File 6: `_factory/core/model_router.py` (MODIFY)

```python
ROUTES = {
    "cloud": {
        "json_context": "gemini-2.0-flash-lite",  # structured, simple
        "data_synth":   "gemini-2.0-flash-lite",  # CSV generation
        "md_refine":    "gemini-2.0-flash",        # quality-critical
        "timeline":     "gemini-2.0-flash-lite",  # structured
        "general":      "gemini-2.0-flash",        # fallback
    }
}
# Add get_pricing(model) classmethod
```

### File 7: `_factory/core/gemini_rest.py` (MODIFY)

Return usage metadata from API response:
```python
def call_gemini(prompt, model="gemini-2.0-flash", is_json=False):
    ...
    usage = data.get("usageMetadata", {})
    return {
        "content": parsed_result,
        "input_tokens": usage.get("promptTokenCount", 0),
        "output_tokens": usage.get("candidatesTokenCount", 0),
    }
```

### File 8: `_factory/core/compiler.py` (MODIFY)

Wire all components:
```python
def __init__(self):
    self.cost_tracker = CostTracker()
    self.compressor = FactoryCompressor()
    self.semantic_cache = SemanticCache(cache_dir)
    self.tool_memory = ToolMemory()

def call_llm(self, prompt, is_json=False, task_type="general"):
    # 1. Check semantic cache
    # 2. Compress prompt (LLMLingua)
    # 3. Route to correct model (cascading)
    # 4. Record cost
    # 5. Cache response
    return result

def build(self):
    ...
    self.cost_tracker.save(output_dir + "/cost_report.json")
```

### File 9: `_factory/core/worker.py` (MODIFY)

Use actual Gemini token counts when available instead of `len(text)//4` estimates.

### File 10: `_factory/core/tool_researcher.py` (MODIFY)

Check tool_memory before doing web search:
```python
def research_tools(industry, use_cases, llm_caller, memory=None):
    if memory:
        cached = memory.recall(industry, use_cases)
        if cached:
            return cached
    # ... existing search + LLM logic ...
    if memory:
        memory.remember(industry, use_cases, tools)
    return tools
```

## Execution Order

1. Create `cost_tracker.py` (standalone, no deps)
2. Create `tool_memory.py` (standalone, JSON-based)
3. Modify `model_router.py` (cascading + pricing)
4. Modify `gemini_rest.py` (return usage metadata)
5. Modify `compiler.py` (wire cost tracker + model fix)
6. Modify `worker.py` (actual token counts)
7. Modify `tool_researcher.py` (integrate tool memory)
8. Create `prompt_compressor.py` (LLMLingua wrapper)
9. Create `semantic_cache.py` (vector similarity cache)
10. Create `skeleton_refiner.py` (SoT pattern)

Steps 1-7 are the core (cost tracking + cascading + memory).
Steps 8-10 are the advanced optimizations (compression + caching + SoT).

## Test Plan

| # | Test | Validates |
|---|------|-----------|
| 1 | Unit: CostTracker records calls, groups by task_type, calculates cost | Cost accumulator |
| 2 | Unit: ModelRouter returns flash-lite for json_context, flash for md_refine | Cascading routes |
| 3 | Unit: call_gemini returns {content, input_tokens, output_tokens} | New return format |
| 4 | Unit: ToolMemory recall/remember with TTL expiry | Memory persistence |
| 5 | Integration: Local build produces cost_report.json with $0.00 | Local tracking |
| 6 | Integration: Cloud build produces cost_report.json with per-task breakdown | Cloud tracking |
| 7 | Integration: Second build for same industry hits tool_memory cache | Memory reuse |
| 8 | Regression: Existing --mode local build completes without breakage | Backward compat |

## Status

| # | File | Status |
|---|------|--------|
| 1 | `_factory/core/cost_tracker.py` | ✅ DONE |
| 2 | `_factory/core/prompt_compressor.py` | ✅ DONE |
| 3 | `_factory/core/semantic_cache.py` | ✅ DONE |
| 4 | `_factory/core/skeleton_refiner.py` | ✅ DONE |
| 5 | `_factory/core/tool_memory.py` | ✅ DONE |
| 6 | `_factory/core/model_router.py` | ✅ DONE |
| 7 | `_factory/core/gemini_rest.py` | ✅ DONE |
| 8 | `_factory/core/compiler.py` | ✅ DONE |
| 9 | `_factory/core/worker.py` | ✅ DONE (uses estimates, actual tokens when available) |
| 10 | `_factory/core/tool_researcher.py` | ✅ DONE (memory handled in compiler) |
