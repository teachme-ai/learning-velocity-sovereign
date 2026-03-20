# Plan 11 — Generative Curriculum Engine (Karpathy Loop)

## Context

Plans 01–10 built a **template refinement engine**: 8 fixed session templates rendered with Jinja2 variables and refined by LLM for industry-specific language. This works for industry customization but fails for **role-level customization** — a Business Analyst in Finance gets the same "Build a Pydantic data cleaner" learning outcome as a Developer in Healthcare.

User testing of the Streamlit UI surfaced 4 critical gaps:
1. Audience picker hardcoded to 5 roles
2. No separation of role vs industry in the manifest
3. Session topics fixed to 8 modules regardless of role/industry
4. Tone/Voice misplaced in the UI

Additionally: TeachMeAI persona pipeline (Plan 10) is built but disconnected — persona_parser → session_planner works, but output never drives content generation. Learning outcomes are static text in template files, never customized.

This plan evolves the factory from a **refinement engine** to a **generative engine** using the Karpathy Loop pattern: generate → evaluate → keep/regenerate.

### Research Sources (Deep Dive — March 2026)

Four external projects were analyzed to inform this architecture:

1. **EduPlanner** — Generate-evaluate-optimize loop for lesson plans. Uses CIDDP rubric (Clarity, Integrity, Depth, Practicality, Pertinence). Code is research-grade/incomplete, but the iterative evaluation pattern and rubric dimensions are directly adoptable.

2. **Stanford Instructional Agents** — Implements 3 of 5 ADDIE phases (Analysis, Design, Development) with 5 coarse-grained agents. Four modes: Autonomous, Catalog-Guided, Feedback-Guided, Co-Pilot. Key insight: coarse-grained tool design (5 phase-level tools) outperforms fine-grained (14 tools). Our Plan 11 aligns with their architecture.

3. **GPT Researcher** — Planner/execution agent pattern for deep web research. Supports Gemini + SearXNG. ~18-28 LLM calls per task, ~$0.02 with Flash. We adopt the planner→sub-questions→executor→synthesizer pattern (built in-house, not as a dependency).

4. **Intelligent Textbooks (McCreary)** — CSV→JSON concept dependency graphs with Bloom's taxonomy mapping. Nodes have group 1-12 (foundation→goal), edges are prerequisites. DAG validated by topological sort. This gives us **principled session ordering** via prerequisite graphs rather than arbitrary sequencing. Visualizable in Streamlit via `streamlit-agraph`.

---

## Architecture: The Karpathy Loop for Curriculum

```
manifest.yaml (role + industry + rubric)
        │
        ▼
┌──────────────────────┐
│  RESEARCH PHASE       │  ← planner/executor pattern (GPT Researcher)
│  "What does this role  │     web search + LLM
│   need to learn?"     │     competency extraction
│                       │     learning objective generation
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  CONCEPT GRAPH PHASE  │  ← concept dependency DAG (Intelligent Textbooks)
│  Build prerequisite   │     nodes = competencies, edges = dependencies
│  DAG + Bloom's levels │     topological sort → session ordering
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  GENERATE PHASE       │  ← LLM generates session titles,
│  session_planner →    │     learning outcomes, and content
│  content_generator    │     from scratch (no fixed templates)
│                       │     ADDIE: Analysis→Design→Development
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  EVALUATE PHASE       │  ← LLM-as-judge scores each session
│  quality_evaluator    │     CIDDP-inspired rubric (EduPlanner)
│                       │     + Bloom's alignment check
└──────────┬───────────┘
           ▼
     score >= threshold?
    /              \
  YES               NO
   │                 │
 KEEP            REGENERATE
 (save)          (feed critique, loop)
   │              max 3 iterations
   ▼                 │
 cost_report    ◄───┘
```

---

## Files to Create / Modify

| # | File | Action | Purpose |
|---|------|--------|---------|
| 1 | `_factory/core/curriculum_researcher.py` | CREATE | Planner/executor research pattern — web search + LLM → competencies + concept graph |
| 2 | `_factory/core/concept_graph.py` | CREATE | Concept dependency DAG — nodes=competencies, edges=prerequisites, topological sort for session ordering, Bloom's group mapping |
| 3 | `_factory/core/content_generator.py` | CREATE | Generate full session markdown from learning objectives (no templates needed) |
| 4 | `_factory/core/quality_evaluator.py` | CREATE | CIDDP-inspired LLM-as-judge rubric scoring + critique generation |
| 5 | `_factory/core/quality_loop.py` | CREATE | Karpathy Loop orchestrator: generate → evaluate → keep/regenerate |
| 6 | `_factory/quality_rubric.md` | CREATE | Rubric definition (CIDDP-inspired: role relevance, Bloom's, completeness, practical applicability) |
| 7 | `_factory/core/session_planner.py` | MODIFY | Accept research output + concept graph; topological sort for session ordering; remove hardcoded fallback |
| 8 | `_factory/core/compiler.py` | MODIFY | Wire quality loop into build pipeline; use planner output to drive content generation instead of template walk |
| 9 | `_factory/core/manifest_validator.py` | MODIFY | Add `role` as separate field; relax `audience` validation; add `quality_threshold` |
| 10 | `_factory/ui/control_tower.py` | MODIFY | Split role + industry inputs; move tone to audience step; make audience free-text; wire persona_source; concept graph visualization |
| 11 | `_factory/core/compiler.py` → `generate_readme()` | MODIFY | Dynamic README from actual generated sessions instead of hardcoded 8-row table |

---

## Detailed Changes

### File 1: `_factory/core/curriculum_researcher.py` (CREATE)

Researches what a specific role in a specific industry needs to learn about AI. Uses the **planner/executor pattern** (inspired by GPT Researcher): a planner LLM generates sub-questions, executor searches each, synthesizer combines into structured output.

```python
class CurriculumResearcher:
    def research(self, role, industry, use_cases, llm_caller, search_fn=None):
        """
        Planner/Executor pattern:
          1. Planner generates 3-5 sub-questions about role+industry AI needs
          2. Executor searches each sub-question (SearXNG → Tavily → LLM fallback)
          3. Synthesizer combines search results into structured competencies
          4. Graph builder creates concept dependency DAG

        Returns:
            {
                "competencies": [
                    {"id": "fin_data_analysis", "name": "Financial Data Analysis with AI",
                     "bloom_level": "Apply", "bloom_group": 5,
                     "description": "...", "priority": "high"}
                ],
                "learning_objectives": [
                    {"objective": "...", "bloom_verb": "Analyze",
                     "competency_id": "fin_data_analysis"}
                ],
                "concept_graph": {
                    "nodes": [
                        {"id": "fin_data_analysis", "label": "Financial Data Analysis",
                         "group": 5, "bloom_level": "Apply"}
                    ],
                    "edges": [
                        {"from": "data_literacy", "to": "fin_data_analysis"}
                    ]
                },
                "recommended_session_count": 6,
                "rationale": "..."
            }
        """
        # Step 1: PLAN — LLM generates sub-questions
        #   "What AI tools does a {role} in {industry} use daily?"
        #   "What competencies do {industry} job postings require for AI-augmented {role}s?"
        #   "What are the prerequisite skills for AI adoption in {industry}?"
        # Step 2: EXECUTE — search each sub-question
        #   Uses existing tool_researcher.py search_fn pattern (SearXNG → Tavily → LLM fallback)
        # Step 3: SYNTHESIZE — LLM combines search results into competencies
        #   Map each competency to Bloom's Taxonomy level + group (1-12)
        # Step 4: GRAPH — LLM generates concept dependency edges
        #   "Which competencies are prerequisites for which?"
        #   Output as DAG nodes + edges (Intelligent Textbooks pattern)
```

**Reuses:**
- `tool_researcher.py` search infrastructure (SearXNG/Tavily)
- `tool_memory.py` for caching research results across builds
- `model_router.py` for task routing (this is a `general` task → gemini-2.5-flash)

### File 2: `_factory/core/concept_graph.py` (CREATE)

Concept dependency DAG inspired by **Intelligent Textbooks (McCreary)**. Nodes are competencies, edges are prerequisites. Bloom's taxonomy maps to node groups (1-12). Topological sort determines session ordering.

```python
class ConceptGraph:
    """
    Directed Acyclic Graph of learning concepts with Bloom's group levels.

    Bloom's → Group mapping:
      Groups 1-2:  Remember     (Navigator foundations)
      Groups 3-4:  Understand   (Navigator core)
      Groups 5-6:  Apply        (Navigator advanced / Builder foundations)
      Groups 7-8:  Analyze      (Builder core)
      Groups 9-10: Evaluate     (Builder advanced / Architect foundations)
      Groups 11-12: Create      (Architect core)
    """

    def __init__(self, nodes=None, edges=None):
        self.nodes = nodes or []  # [{"id", "label", "group", "bloom_level"}]
        self.edges = edges or []  # [{"from", "to"}]

    @classmethod
    def from_research(cls, research_output):
        """Build graph from curriculum_researcher output."""
        graph_data = research_output.get("concept_graph", {})
        return cls(graph_data.get("nodes", []), graph_data.get("edges", []))

    def topological_order(self):
        """Return node IDs in prerequisite-respecting order (Kahn's algorithm)."""
        # Standard topological sort on the DAG
        # Raises ValueError if cycle detected

    def session_sequence(self, target_count):
        """
        Group topologically-sorted concepts into N sessions.
        Early sessions get low-group (foundation) concepts.
        Later sessions get high-group (goal) concepts.
        Returns: [{"session_number", "concept_ids", "bloom_range"}]
        """

    def validate(self):
        """Check DAG is acyclic, all edge endpoints exist, groups are monotonic on paths."""

    def to_vis_json(self):
        """Export to vis-network compatible JSON for Streamlit visualization."""
        return {
            "nodes": [{"id": n["id"], "label": n["label"], "group": n["group"],
                       "title": f"{n['bloom_level']} (group {n['group']})"} for n in self.nodes],
            "edges": [{"from": e["from"], "to": e["to"], "arrows": "to"} for e in self.edges],
        }
```

**Reuses:**
- No external dependencies (pure Python graph algorithms)
- Outputs feed into `session_planner.py` for ordering
- `to_vis_json()` feeds Streamlit visualization in `control_tower.py`

### File 2: `_factory/core/content_generator.py` (CREATE)

Generates full session markdown from a session spec (title, learning objectives, tools, portfolio artifact). No Jinja2 templates — pure LLM generation.

```python
class ContentGenerator:
    TRACK_SPECS = {
        "navigator": {"depth": "no-code", "tools": "Google AI Studio, n8n, NotebookLM",
                       "format": "step-by-step GUI walkthrough with screenshots placeholders"},
        "builder":   {"depth": "low-code", "tools": "Python + APIs, Gemini, LangChain",
                       "format": "lab guide with code blocks and explanations"},
        "architect": {"depth": "full-code", "tools": "Python, Docker, local models",
                       "format": "engineering spec with implementation code"},
    }

    def generate_session(self, session_spec, track, tone, industry, role, llm_caller):
        """
        Args:
            session_spec: {title, description, learning_objectives, tools_used, portfolio_artifact}
            track: "navigator" | "builder" | "architect"
            tone: "Practical & Applied" | etc.
            industry, role: strings
            llm_caller: callable

        Returns:
            {
                "markdown": "# Session N: ...\n\n## Learning Outcomes\n...",
                "metadata": {tokens_used, bloom_levels, tools_referenced}
            }
        """
        # Build prompt with:
        #   - Session spec (title, objectives, tools, artifact)
        #   - Track depth spec (no-code vs low-code vs full-code)
        #   - Tone instruction
        #   - Role + industry context
        #   - Output format: markdown with ## Learning Outcomes, ## Lab, ## Deliverable sections
```

**Reuses:**
- `model_router.py` — this is `md_refine` quality (gemini-2.5-flash)
- `cost_tracker.py` — records token usage per session generated
- `skeleton_refiner.py` (Plan 09, currently unused) — could use skeleton-of-thought for structured generation

### File 4: `_factory/core/quality_evaluator.py` (CREATE)

CIDDP-inspired LLM-as-judge that scores generated content against the 5-dimension rubric. Each dimension maps to EduPlanner's evaluation framework adapted for our context.

```python
class QualityEvaluator:
    """
    Evaluation dimensions (from EduPlanner CIDDP, adapted):
      - Pertinence (CIDDP: Pertinence) → Role Relevance
      - Bloom's Alignment (new, from Intelligent Textbooks)
      - Depth + Practicality (CIDDP: Depth + Practicality merged)
      - Clarity (CIDDP: Clarity)
      - Integrity (CIDDP: Integrity) → Completeness
    """

    WEIGHTS = {
        "pertinence": 0.25,
        "bloom_alignment": 0.20,
        "depth_practicality": 0.25,
        "clarity": 0.15,
        "integrity": 0.15,
    }

    def evaluate(self, content, session_spec, role, industry, rubric, llm_caller,
                 concept_graph_context=None):
        """
        Args:
            concept_graph_context: Optional dict with prerequisite info for this session
                                   (from ConceptGraph — validates Bloom's progression)
        Returns:
            {
                "score": 7.5,          # 0-10 weighted composite
                "dimensions": {
                    "pertinence": 8,           # Role relevance (CIDDP)
                    "bloom_alignment": 7,      # Matches target cognitive level
                    "depth_practicality": 8,   # Achievable + deep enough (CIDDP)
                    "clarity": 7,              # Instructions clear (CIDDP)
                    "integrity": 7,            # All objectives covered (CIDDP)
                },
                "critique": "Session focuses too heavily on developer tasks. For a BA,
                             replace Python coding with dashboard configuration and
                             data interpretation exercises.",
                "pass": True  # score >= threshold
            }
        """
        # Uses gemini-2.5-flash-lite (structured eval, cheap task)
        # Prompt includes rubric text, session spec, role context, and
        # concept graph prerequisites (if provided) for Bloom's validation
```

### File 4: `_factory/core/quality_loop.py` (CREATE)

The Karpathy Loop orchestrator.

```python
class QualityLoop:
    def __init__(self, generator, evaluator, max_iterations=3, threshold=7.0):
        self.generator = generator
        self.evaluator = evaluator
        self.max_iterations = max_iterations
        self.threshold = threshold

    def run(self, session_spec, track, tone, industry, role, rubric, llm_caller):
        """
        Generate → Evaluate → Keep/Regenerate loop.

        Returns:
            {
                "content": final_markdown,
                "iterations": 2,
                "final_score": 8.1,
                "history": [{iteration, score, critique}, ...]
            }
        """
        history = []
        feedback = None
        for i in range(self.max_iterations):
            # Generate (with feedback from previous iteration if any)
            result = self.generator.generate_session(
                session_spec, track, tone, industry, role, llm_caller,
                prior_critique=feedback
            )
            # Evaluate
            eval_result = self.evaluator.evaluate(
                result["markdown"], session_spec, role, industry, rubric, llm_caller
            )
            history.append({"iteration": i+1, "score": eval_result["score"],
                           "critique": eval_result["critique"]})
            if eval_result["pass"]:
                return {"content": result["markdown"], "iterations": i+1,
                        "final_score": eval_result["score"], "history": history}
            feedback = eval_result["critique"]
        # Return best attempt after max iterations
        return {"content": result["markdown"], "iterations": self.max_iterations,
                "final_score": eval_result["score"], "history": history}
```

### File 6: `_factory/quality_rubric.md` (CREATE)

Rubric inspired by **EduPlanner's CIDDP** (Clarity, Integrity, Depth, Practicality, Pertinence) adapted for our curriculum context. We rename and reweight dimensions to fit role-based AI training.

```markdown
# Quality Rubric for Generated Curriculum Sessions
# Inspired by EduPlanner CIDDP + Bloom's Taxonomy alignment

## Dimensions (each scored 0-10)

### 1. Pertinence / Role Relevance (weight: 25%) — from CIDDP "Pertinence"
- Does the content address tasks this role actually performs?
- Are examples drawn from the role's daily work context?
- Would a professional in this role find this immediately applicable?
- (CIDDP: "Is the lesson relevant to the learner's needs and goals?")

### 2. Bloom's Alignment (weight: 20%) — from Intelligent Textbooks group mapping
- Navigator track: target Remember/Understand/Apply (groups 1-6)
- Builder track: target Apply/Analyze (groups 5-8)
- Architect track: target Analyze/Evaluate/Create (groups 7-12)
- Do the activities match the target cognitive level?
- Does session position in concept graph match Bloom's progression?

### 3. Depth & Practicality (weight: 25%) — from CIDDP "Depth" + "Practicality"
- Can the learner produce the portfolio artifact by end of session?
- Are tools specified and accessible (browser-based or Codespace-ready)?
- Is the 2-hour time constraint respected?
- Does the lab go deep enough for the track level?

### 4. Clarity (weight: 15%) — from CIDDP "Clarity"
- Are instructions unambiguous?
- Is technical jargon appropriate for the role's skill level?
- Can the learner follow the lab without instructor intervention?

### 5. Integrity / Completeness (weight: 15%) — from CIDDP "Integrity"
- Are all learning objectives from the session spec addressed?
- Is there a clear deliverable/artifact?
- Does the session reference the correct industry context?
- Are prerequisite concepts (from concept graph) properly referenced?

## Composite Score
weighted_score = (pertinence * 0.25) + (bloom_alignment * 0.20) +
                 (depth_practicality * 0.25) + (clarity * 0.15) +
                 (integrity * 0.15)

## Threshold
- Pass: >= 7.0
- Regenerate with critique: < 7.0
- Max iterations: 3
```

### File 7: `_factory/core/session_planner.py` (MODIFY)

Remove hardcoded 8-module fallback. Accept research output + concept graph. Use **topological sort** for session ordering (Intelligent Textbooks pattern).

**Current:** `_fallback_plan()` returns the same 8 titles. Session order is arbitrary.

**New:** Planner takes `curriculum_research` output + `ConceptGraph`. Topological sort determines which concepts come first. LLM groups concepts into sessions respecting prerequisites.

```python
from .concept_graph import ConceptGraph

def plan_sessions(persona_dict, tools_list, curriculum_research, llm_caller):
    """
    Now accepts curriculum_research with competencies, learning objectives, and concept graph.
    Session ordering follows topological sort of concept dependency DAG.
    """
    graph = ConceptGraph.from_research(curriculum_research)
    graph.validate()  # Ensure DAG is acyclic

    # Step 1: Topological sort → ordered concept sequence
    ordered_concepts = graph.topological_order()

    # Step 2: Group concepts into sessions (respecting prerequisites)
    session_groups = graph.session_sequence(
        target_count=curriculum_research.get("recommended_session_count", 8)
    )

    # Step 3: LLM generates titles, descriptions, artifacts for each group
    # Foundation concepts (groups 1-4) → early sessions
    # Goal concepts (groups 9-12) → later sessions / capstone
    # Each session's Bloom's level matches its concept group range
```

### File 7: `_factory/core/compiler.py` (MODIFY)

Add a new build mode: `generative`. The existing `compile()` (template-based) remains as `compile_template()` for backward compat. New `compile_generative()` uses the quality loop.

```python
def compile_generative(self):
    """Full generative build: research → plan → generate → evaluate → output."""
    # 1. Research competencies
    researcher = CurriculumResearcher()
    research = researcher.research(
        role=self.context['role'],
        industry=self.context['industry_name'],
        use_cases=self.context['use_cases'],
        llm_caller=lambda p: self.call_llm(p, is_json=True, task_type="general")
    )
    self.context["curriculum_research"] = research

    # 2. Plan sessions from research
    session_plan = plan_sessions(
        persona_dict=self.context.get("persona", {}),
        tools_list=self.context.get("tools", []),
        curriculum_research=research,
        llm_caller=lambda p: self.call_llm(p, is_json=True, task_type="general")
    )

    # 3. For each session × each track: generate + evaluate via quality loop
    loop = QualityLoop(ContentGenerator(), QualityEvaluator())
    for session_spec in session_plan["sessions"]:
        for track in self.context["tracks"]:
            result = loop.run(
                session_spec, track, self.context["tone"],
                self.context["industry_name"], self.context["role"],
                rubric, lambda p: self.call_llm(p, task_type="md_refine")
            )
            # Write to dist/
            self._write_session(session_spec, track, result)

    # 4. Generate dynamic README + cost report
    self._generate_dynamic_readme(session_plan)
    self.cost_tracker.save(os.path.join(self.build_dir, "cost_report.json"))

def compile(self):
    """Route to template-based or generative build based on manifest."""
    if self.manifest.get("build_mode") == "generative":
        self.compile_generative()
    else:
        self.compile_pass1()
        self.compile_pass2()
        # ... existing post-build steps
```

### File 8: `_factory/core/manifest_validator.py` (MODIFY)

Add new fields:
```python
DEFAULTS = {
    # ... existing fields ...
    "role": None,                    # NEW — separate from audience
    "build_mode": "template",        # NEW — "template" or "generative"
    "quality_threshold": 7.0,        # NEW — minimum score for keep/discard
    "max_iterations": 3,             # NEW — quality loop iterations
}
```

Relax audience validation to accept any string (not just 5 hardcoded values).

### File 9: `_factory/ui/control_tower.py` (MODIFY)

**Step 1 — WHAT:** Split into Industry + Role as separate inputs
```
Industry: [dropdown from catalog OR free text]
Role:     [free text with suggestions: "Business Analyst", "Developer", "Data Scientist", ...]
```

**Step 2 — WHO + TONE:** Move Tone/Voice here, auto-suggest based on role
```
Audience persona: [free text, pre-filled from role]
Tone/Voice:       [auto-suggested based on role, overridable]
```

**Step 3 — HOW:** Session count selector (not fixed modules)
```
Duration: [Half-day 2 sessions | Full-day 4 | Sprint 6 | Bootcamp 8 | Custom N]
Build Mode: [Template (fast, fixed topics) | Generative (dynamic, role-specific)]
```

**Step 4 — CONTEXT:** Compliance + Region (tone moved out)

**Step 5 — PERSONA (new, optional):** Upload TeachMeAI CSV or select persona file
```
Persona Source: [None | Upload CSV | Select existing file]
```

**Step 6 — CONCEPT MAP (new, post-build):** Visualize the generated concept dependency graph
```
After generative build completes:
- Show interactive concept graph using streamlit-agraph or st.components.v1.html
- Nodes colored by Bloom's group (green=foundation, yellow=apply, red=create)
- Edges show prerequisite relationships
- Click a node to see the session it maps to
```

**Manifest output** now includes:
```yaml
industry: "AI for Global Finance"
role: "Business Analyst"
build_mode: "generative"
quality_threshold: 7.0
persona_source: "path/to/persona.yaml"  # optional
```

### File 10: `compiler.py` → `generate_readme()` (MODIFY)

Replace hardcoded 8-row table with dynamic generation from actual sessions built:
```python
def _generate_dynamic_readme(self, session_plan):
    rows = []
    for s in session_plan["sessions"]:
        rows.append(f"| {s['session_number']} | {s['title']} | {s.get('portfolio_artifact', '')} |")
    table = "\n".join(rows)
    # Render README with dynamic table
```

---

## Execution Order

### Phase A: Quick UI fixes (no pipeline changes)
1. Modify `control_tower.py` — split role/industry, move tone, add build mode toggle
2. Modify `manifest_validator.py` — add role, build_mode, quality_threshold, relax audience

### Phase B: Research + Concept Graph + Planning layer
3. Create `curriculum_researcher.py` — planner/executor research pattern + concept graph output
4. Create `concept_graph.py` — DAG data structure, topological sort, Bloom's group mapping, visualization export
5. Modify `session_planner.py` — accept research + concept graph; topological sort for session ordering

### Phase C: Generation + Evaluation layer (the Karpathy Loop)
6. Create `quality_rubric.md` — CIDDP-inspired rubric definition
7. Create `content_generator.py` — LLM generates full session markdown
8. Create `quality_evaluator.py` — CIDDP-inspired LLM-as-judge scoring
9. Create `quality_loop.py` — generate → evaluate → keep/regenerate orchestrator

### Phase D: Compiler integration + Visualization
10. Modify `compiler.py` — wire generative build mode, dynamic README
11. Add concept graph visualization to `control_tower.py` (post-build view)
12. End-to-end test: "Business Analyst in Global Finance" → generative build → cost report

### ADDIE Phase Mapping (Stanford Instructional Agents alignment)
| ADDIE Phase | Our Component | Mode |
|-------------|---------------|------|
| Analysis | `curriculum_researcher.py` | Autonomous (web search + LLM) |
| Design | `session_planner.py` + `concept_graph.py` | Autonomous (DAG + topological sort) |
| Development | `content_generator.py` + `quality_loop.py` | Autonomous (Karpathy Loop) |
| Implementation | `compiler.py` → `dist/` output | Automated |
| Evaluation | `quality_evaluator.py` | Autonomous (CIDDP rubric) |

---

## Backward Compatibility

- `build_mode: "template"` (default) → existing Plans 01-10 pipeline, unchanged
- `build_mode: "generative"` → new Plan 11 pipeline
- Both modes share: model_router, cost_tracker, tool_memory, cache, token budgets
- UI shows both options; user chooses

---

## Cost Estimate (Generative Build)

Per session × per track, estimated LLM calls:
| Phase | Calls | Model | Est. Tokens |
|-------|-------|-------|-------------|
| Research | 2 (search + synthesize) | flash | ~3K |
| Plan | 1 | flash | ~2K |
| Generate | 1-3 (with loop) | flash | ~4K per iteration |
| Evaluate | 1-3 | flash-lite | ~1K per iteration |

**8 sessions × 2 tracks × avg 2 iterations:**
- ~80 LLM calls
- ~80K tokens
- **~$0.02 USD / ₹1.70 INR** per full build

---

## Verification

1. **Unit test:** CurriculumResearcher returns competencies with Bloom's levels + concept graph for "BA in Finance"
2. **Unit test:** ConceptGraph validates DAG (no cycles), topological sort returns correct order, Bloom's groups are monotonic on prerequisite paths
3. **Unit test:** ContentGenerator produces markdown with ## Learning Outcomes section
4. **Unit test:** QualityEvaluator returns 5-dimension CIDDP score + critique; low-quality content scores < 7
5. **Unit test:** QualityLoop iterates and improves score on second pass
6. **Integration test:** Full generative build for "Business Analyst in Global Finance" produces:
   - `dist/ai_for_global_finance/` with N session directories
   - Each session has role-appropriate learning outcomes (not "Build a Pydantic cleaner")
   - Session ordering follows concept graph prerequisites (data literacy before predictive modeling)
   - `cost_report.json` with USD + INR breakdown
   - Quality scores logged per session with all 5 CIDDP dimensions
7. **Regression test:** Template build mode (`build_mode: template`) still works unchanged
8. **UI test:** Streamlit shows role + industry separately, tone near audience, build mode toggle works
9. **Visualization test:** Concept graph renders in Streamlit post-build, nodes clickable, colors match Bloom's groups
