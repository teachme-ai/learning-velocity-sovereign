# Plan 10 — Dynamic Session Planner & Tool Researcher

## Goal
Generate personalized curriculum plans based on learner persona data (from TeachMeAI intake). Parse persona profiles, research relevant low-code AI tools via web search, and produce a dynamic session plan with the correct number of sessions, tool assignments, and portfolio artifacts.

## Problem Statement
Previously, the factory used a static 8-session template for all learners regardless of their background, maturity, or priorities. This plan adds:
1. Persona-aware session count (8 base, 9-10 for high-maturity learners with score > 45)
2. Tool discovery via web search (SearXNG primary, Tavily fallback) + LLM curation
3. Dynamic session planning with priority mapping and portfolio artifact integration

## Files Created / Modified

| # | File | Action | Purpose |
|---|------|--------|---------|
| 1 | `_factory/core/persona_parser.py` | CREATE | Load TeachMeAI Intake_v2 CSV (6 JSON columns), YAML, or JSON persona files |
| 2 | `_factory/core/tool_researcher.py` | CREATE | Discover low-code AI tools via SearXNG/Tavily search + LLM curation |
| 3 | `_factory/core/session_planner.py` | CREATE | Generate dynamic curriculum plan with session count, justification, artifacts |
| 4 | `_factory/core/manifest_validator.py` | MODIFY | Added persona_source, planned_sessions, tools to DEFAULTS dict |
| 5 | `_factory/core/compiler.py` | MODIFY | Added persona→tools→planner pipeline in generate_llm_context() |

## Architecture

```
manifest.yaml (persona_source) 
        │
        ▼
┌──────────────────┐
│  persona_parser   │ ← CSV/YAML/JSON intake data
│  load_persona()   │
└────────┬─────────┘
         │ persona_dict
         ▼
┌──────────────────┐
│  tool_researcher  │ ← SearXNG (free) → Tavily (fallback) → LLM knowledge
│  research_tools() │
└────────┬─────────┘
         │ tools_list [{name, url, setup_requirements, reason}]
         ▼
┌──────────────────┐
│  session_planner  │ ← persona + tools → LLM reasoning
│  plan_sessions()  │
└────────┬─────────┘
         │ {total_sessions, justification, sessions[]}
         ▼
    compiler.py (generates session-specific content)
```

## Key Constraints
- 8-session floor for all learners
- 9-10 sessions only if marketMaturityScore > 45
- Each session maps to a learner priority where possible
- Portfolio artifacts from persona are assigned to relevant sessions
- No-code tools (Google AI Studio, n8n, Make.com) included for low-maturity learners
- Tools must be Codespace-executable or browser-accessible

## Implementation Details

### persona_parser.py
- `load_persona(source_path, row_index=None)` — main entry point
- Handles CSV with 6 embedded JSON columns (TeachMeAI Intake_v2 format)
- Handles YAML/JSON persona files
- Extracts: topPriorities, marketMaturityScore, decisionStyle, uncertaintyHandling, cognitiveLoadTolerance, socialEntanglement, portfolioArtifact
- `_safe_json()` for robust JSON parsing from CSV cells
- `_flatten_blocks()` to normalize nested persona structures

### tool_researcher.py
- `research_tools(industry, use_cases, llm_caller)` — main entry point
- Builds search query from industry + use cases
- Search chain: SearXNG (free, unlimited) → Tavily (1000/mo) → LLM knowledge
- LLM curates 2-3 tools from search results
- Returns `[{name, url, setup_requirements, reason}]`

### session_planner.py
- `plan_sessions(persona_dict, tools_list, llm_caller)` — main entry point
- Determines session count: 8 if maturity < 45, up to 10 if maturity >= 45
- Maps priorities to sessions
- Assigns portfolio artifacts to relevant sessions
- `_fallback_plan(count)` for graceful degradation if LLM fails
- Returns `{total_sessions, justification, sessions[]}`

## Test Results (Verified)

All tests passed with mock LLM:
- ✅ Persona loading from YAML (healthcare doctor, maturity 42)
- ✅ Tool research with SearXNG context (2 tools returned)
- ✅ Session planning: 8 sessions (maturity 38 < 45 threshold)
- ✅ No-code tool inclusion for low-maturity learners
- ✅ Priority mapping across sessions
- ✅ Portfolio artifact assignment
- ✅ Compiler integration (persona→tools→planner pipeline)

## Status

| # | File | Status |
|---|------|--------|
| 1 | `_factory/core/persona_parser.py` | ✅ DONE |
| 2 | `_factory/core/tool_researcher.py` | ✅ DONE |
| 3 | `_factory/core/session_planner.py` | ✅ DONE |
| 4 | `_factory/core/manifest_validator.py` | ✅ DONE |
| 5 | `_factory/core/compiler.py` | ✅ DONE |

## ✅ PLAN COMPLETE
