# Plan 08 — Course Identification & Input System Redesign

**Status:** ✅ COMPLETE
**Scope:** 5 files to modify, 1 file already created
**Dependencies:** Plans 01–07 remain valid; this is additive only

---

## Execution Status

| # | File | Action | Status |
|---|---|---|---|
| 1 | `_factory/catalog/courses.yaml` | CREATE | ✅ DONE |
| 2 | `_factory/ui/control_tower.py` | MODIFY | ✅ DONE |
| 3 | `_factory/core/compiler.py` | MODIFY | ✅ DONE |
| 4 | `_factory/core/manifest_validator.py` | CREATE | ✅ DONE |
| 5 | `.agent/skills/factory/context_refiner.py` | MODIFY | ✅ DONE |

---

## File 1 — `_factory/catalog/courses.yaml` ✅ ALREADY CREATED

**Path:** `_factory/catalog/courses.yaml`
**Created:** 2026-03-12
**No further action needed.**

Contains 15 pre-built course definitions. Each entry has:
- `id` — machine-readable slug
- `label` — display name for UI
- `industry` — exact string passed to compiler
- `use_cases` — array of 3–4 scenario tags
- `default_tracks` — which tracks are pre-selected
- `default_sessions` — which session numbers are included by default
- `tone` — one of 4 voice options
- `compliance` — list of compliance frameworks
- `region` — geographic context string

Courses covered:
1. AI for Cyber-Security
2. AI for Global Finance
3. AI for Healthcare
4. AI for Supply Chain
5. AI for Legal
6. AI for Retail & E-Commerce
7. AI for Educators
8. AI for Marketing
9. AI for Sales
10. AI for Product Managers
11. AI for HR
12. AI for Manufacturing
13. AI for Energy
14. AI for Real Estate
15. AI for Government

---

## File 2 — `_factory/ui/control_tower.py` ✅ DONE

**Path:** `_factory/ui/control_tower.py`
**Action:** Full rewrite of `tab1` and sidebar; keep `tab2`, `tab3`, sidebar Guardian section intact.

### New imports to add (top of file)

```python
from pathlib import Path
```

### New helper function — add before `st.set_page_config`

```python
def load_catalog():
    catalog_path = Path("_factory/catalog/courses.yaml")
    if not catalog_path.exists():
        return []
    with open(catalog_path) as f:
        data = yaml.safe_load(f)
    return data.get("courses", [])
```

### Replace sidebar inputs (lines 17–23)

**Remove:**
```python
# Sidebar: Mission Configuration
st.sidebar.header("🚀 Mission Configuration")
industry = st.sidebar.text_input("Target Industry", "AI for Cyber-Security")
engine_mode = st.sidebar.selectbox("LLM Engine", ["Local (Ollama)", "Turbo (Gemini)"], index=0)
mode_val = "cloud" if "Turbo" in engine_mode else "local"

tracks = st.sidebar.multiselect("Active Tracks", ["Base", "Integrated", "Architect"], default=["Base", "Integrated", "Architect"])
```

**Replace with:**
```python
st.sidebar.header("🚀 Mission Configuration")
engine_mode = st.sidebar.selectbox("LLM Engine", ["Local (Ollama)", "Turbo (Gemini)"], index=0)
mode_val = "cloud" if "Turbo" in engine_mode else "local"
```

### Replace `tab1` block entirely (lines 44–86)

**Remove:** Everything inside `with tab1:` (lines 44–86)

**Replace with:**

```python
with tab1:
    st.subheader("Course Builder")

    catalog = load_catalog()
    catalog_labels = [c["label"] for c in catalog]
    catalog_map = {c["label"]: c for c in catalog}

    # ── Step 1: WHAT ──────────────────────────────────────────────────────────
    st.markdown("### Step 1 — WHAT: Course Selection")
    course_mode = st.radio("", ["Select from catalog", "Build custom course"], horizontal=True, key="course_mode")

    if course_mode == "Select from catalog":
        selected_label = st.selectbox("Choose a course", catalog_labels)
        selected_course = catalog_map[selected_label]
        industry = selected_course["industry"]
        default_use_cases = selected_course.get("use_cases", [])
        default_sessions = selected_course.get("default_sessions", list(range(1, 9)))
        default_tracks = selected_course.get("default_tracks", ["base", "integrated", "architect"])
        default_tone = selected_course.get("tone", "Practical & Applied")
        default_compliance = selected_course.get("compliance", ["None"])[0]
        default_region = selected_course.get("region", "Global")
        use_cases = st.multiselect("Use Case Focus", default_use_cases, default=default_use_cases)
    else:
        industry = st.text_input("Custom Industry Name", "AI for ...")
        use_cases = st.text_area("Use Cases (one per line)", "Use Case 1\nUse Case 2").splitlines()
        default_sessions = list(range(1, 9))
        default_tracks = ["base", "integrated", "architect"]
        default_tone = "Practical & Applied"
        default_compliance = "None"
        default_region = "Global"

    st.markdown("---")

    # ── Step 2: WHO ───────────────────────────────────────────────────────────
    st.markdown("### Step 2 — WHO: Audience")
    AUDIENCE_TRACK_MAP = {
        "Executive / C-Suite":    ["base"],
        "Business Analyst":       ["base", "integrated"],
        "Developer / Engineer":   ["base", "integrated", "architect"],
        "Data Scientist":         ["integrated", "architect"],
        "Product Manager":        ["base", "integrated"],
    }
    audience = st.radio(
        "Select audience persona",
        list(AUDIENCE_TRACK_MAP.keys()),
        horizontal=True,
        key="audience"
    )
    tracks = AUDIENCE_TRACK_MAP[audience]
    st.caption(f"Auto-selected tracks: {', '.join(t.title() for t in tracks)}")

    st.markdown("---")

    # ── Step 3: HOW ───────────────────────────────────────────────────────────
    st.markdown("### Step 3 — HOW: Scope & Duration")

    SESSION_LABELS = {
        1: "01 Data Pipeline Automation",
        2: "02 Executive Narrative Engine",
        3: "03 Multi-Agent Systems",
        4: "04 Sovereign Knowledge RAG",
        5: "05 Advanced UI / LobeChat",
        6: "06 Observability & Tracing",
        7: "07 Sovereign Security",
        8: "08 Grand Capstone",
    }
    DURATION_PRESETS = {
        "Half-day (2 sessions)":    [1, 2],
        "Full-day (4 sessions)":    [1, 2, 3, 4],
        "3-Day Sprint (6 sessions)": [1, 2, 3, 4, 6, 7],
        "Full Bootcamp (8 sessions)": list(range(1, 9)),
        "Custom":                   None,
    }

    duration = st.selectbox("Duration Preset", list(DURATION_PRESETS.keys()), index=3)
    preset_sessions = DURATION_PRESETS[duration]
    if preset_sessions is None:
        preset_sessions = default_sessions

    col1, col2 = st.columns(2)
    sessions = []
    for i, (num, label) in enumerate(SESSION_LABELS.items()):
        col = col1 if i < 4 else col2
        checked = num in preset_sessions
        if col.checkbox(label, value=checked, key=f"session_{num}"):
            sessions.append(num)

    st.markdown("---")

    # ── Step 4: CONTEXT ───────────────────────────────────────────────────────
    st.markdown("### Step 4 — CONTEXT: Optional Configuration")
    ctx_col1, ctx_col2, ctx_col3 = st.columns(3)

    compliance = ctx_col1.selectbox(
        "Compliance Framework",
        ["None", "GDPR", "HIPAA", "SOX", "ISO 27001"],
        index=["None", "GDPR", "HIPAA", "SOX", "ISO 27001"].index(default_compliance)
        if default_compliance in ["None", "GDPR", "HIPAA", "SOX", "ISO 27001"] else 0
    )
    region = ctx_col2.selectbox(
        "Region",
        ["Global", "EU", "US", "APAC", "Middle East"],
        index=["Global", "EU", "US", "APAC", "Middle East"].index(default_region)
        if default_region in ["Global", "EU", "US", "APAC", "Middle East"] else 0
    )
    tone = ctx_col3.selectbox(
        "Tone / Voice",
        ["Auto", "Strategic & Analytical", "Technical & Precise", "Practical & Applied", "Conversational & Accessible"],
        index=["Auto", "Strategic & Analytical", "Technical & Precise", "Practical & Applied", "Conversational & Accessible"].index(default_tone)
        if default_tone in ["Auto", "Strategic & Analytical", "Technical & Precise", "Practical & Applied", "Conversational & Accessible"] else 0
    )
    resolved_tone = default_tone if tone == "Auto" else tone

    st.markdown("---")

    # ── Course Preview Card ───────────────────────────────────────────────────
    st.markdown("### Course Preview")
    slug = industry.lower().replace(' ', '_').replace('&', 'and').replace('-', '_')
    preview_col1, preview_col2 = st.columns(2)
    with preview_col1:
        st.metric("Industry", industry)
        st.metric("Audience", audience)
        st.metric("Sessions", f"{len(sessions)} of 8")
    with preview_col2:
        st.metric("Tracks", ", ".join(t.title() for t in tracks))
        st.metric("Tone", resolved_tone)
        st.metric("Compliance", compliance)
    if use_cases:
        st.markdown("**Use Cases:**")
        for uc in use_cases:
            st.markdown(f"- {uc}")

    st.markdown("---")

    # ── Build Button ──────────────────────────────────────────────────────────
    if st.button("🚀 Initiate Factory Build", type="primary"):
        st.session_state['build_active'] = True

        manifest_data = {
            "industry": industry,
            "tracks": tracks,
            "audience": audience,
            "use_cases": use_cases,
            "sessions": sessions,
            "tone": resolved_tone,
            "compliance_framework": compliance,
            "region": region,
        }
        manifest_path = "_factory/manifests/mission_build.yaml"
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        with open(manifest_path, 'w') as f:
            yaml.dump(manifest_data, f)

        if os.path.exists("_factory/logs/events.jsonl"):
            os.remove("_factory/logs/events.jsonl")

        st.info(f"Launching Build: {industry} | {len(sessions)} sessions | {mode_val.upper()} mode")

        with st.spinner("Factory Engine Running..."):
            compiler_path = "_factory/factory_compiler.py"
            env = os.environ.copy()
            process = subprocess.Popen(
                [sys.executable, compiler_path, manifest_path, "--mode", mode_val],
                env=env
            )
            log_placeholder = st.empty()
            while process.poll() is None:
                if os.path.exists("_factory/logs/events.jsonl"):
                    with open("_factory/logs/events.jsonl", "r") as f:
                        lines = f.readlines()
                        if lines:
                            last_event = json.loads(lines[-1])
                            log_placeholder.info(f"Current Activity: {last_event['event']}")
                time.sleep(1)

            if process.returncode == 0:
                st.success(f"Build for '{industry}' completed successfully!")
                st.balloons()
            else:
                st.error("Build failed. Check the Mission Feed for details.")
```

### Lines to keep unchanged
- Lines 88–98: `tab2` (Live Mission Feed) — no changes
- Lines 100–113: `tab3` (Industry DNA) — update the `st.subheader` line to use `industry` variable (already works since `industry` is now set earlier in the flow)
- Lines 26–40: Sidebar Guardian section — no changes
- Lines 115–117: Sidebar footer — no changes

---

## File 3 — `_factory/core/compiler.py` ✅ DONE

**Path:** `_factory/core/compiler.py`

### Change 3a — `__init__`: read new manifest fields (after line 60)

**After this line:**
```python
        self.context = {
            'industry_name': self.industry,
            'industry_slug': self.slug,
            'tracks': self.manifest.get('tracks', ['base', 'integrated', 'architect'])
        }
```

**Replace with:**
```python
        self.context = {
            'industry_name': self.industry,
            'industry_slug': self.slug,
            'tracks': self.manifest.get('tracks', ['base', 'integrated', 'architect']),
            'audience': self.manifest.get('audience', 'Developer'),
            'use_cases': self.manifest.get('use_cases', []),
            'tone': self.manifest.get('tone', 'Practical & Applied'),
            'compliance_framework': self.manifest.get('compliance_framework', 'None'),
            'region': self.manifest.get('region', 'Global'),
        }
        self.allowed_sessions = self.manifest.get('sessions', list(range(1, 9)))
```

### Change 3b — `generate_llm_context()`: enrich the prompt (lines 107–116)

**Remove:**
```python
        prompt = f"""
        You are an expert AI curriculum architect. Generate industry-specific context for an AI Bootcamp focused on {self.industry}.
        Return ONLY a JSON object with this exact structure:
        {{
            "terminology": ["term1", "term2", "term3", "term4", "term5"],
            "data_scenario": "A short 2-sentence description of an industry-specific data challenge.",
            "dataset_name": "filename_without_spaces.csv",
            "primary_color": "#HEXCODE"
        }}
        """
```

**Replace with:**
```python
        use_cases_str = ", ".join(self.context.get('use_cases', [])) or "general AI applications"
        prompt = f"""
        You are an expert AI curriculum architect. Generate industry-specific context for an AI Bootcamp.

        Industry: {self.industry}
        Target Audience: {self.context.get('audience', 'Developer')}
        Use Cases to emphasize: {use_cases_str}
        Compliance context: {self.context.get('compliance_framework', 'None')}
        Region: {self.context.get('region', 'Global')}
        Tone: {self.context.get('tone', 'Practical & Applied')}

        Return ONLY a JSON object with this exact structure:
        {{
            "terminology": ["term1", "term2", "term3", "term4", "term5"],
            "data_scenario": "A 2-sentence description of an industry-specific data challenge tied to the use cases above.",
            "dataset_name": "filename_without_spaces.csv",
            "primary_color": "#HEXCODE"
        }}
        """
```

### Change 3c — `run_context_refiner()`: pass tone via env (lines 139–144)

**Remove:**
```python
    def run_context_refiner(self, dest_path):
        refiner_script = os.path.join(os.path.dirname(__file__), "../../.agent/skills/factory/context_refiner.py")
        try:
            subprocess.run([sys.executable, refiner_script, dest_path, self.industry, self.slug], check=True)
        except Exception as e:
            self.logger.log(f"Linguistic refinement failed for {os.path.basename(dest_path)}", level="WARNING")
```

**Replace with:**
```python
    def run_context_refiner(self, dest_path):
        refiner_script = os.path.join(os.path.dirname(__file__), "../../.agent/skills/factory/context_refiner.py")
        try:
            env = os.environ.copy()
            env["REFINER_TONE"] = self.context.get('tone', 'Practical & Applied')
            subprocess.run([sys.executable, refiner_script, dest_path, self.industry, self.slug], check=True, env=env)
        except Exception as e:
            self.logger.log(f"Linguistic refinement failed for {os.path.basename(dest_path)}", level="WARNING")
```

### Change 3d — `compile()`: session filter (line 153)

**Remove:**
```python
        for root, dirs, files in os.walk(self.template_dir):
```

**Replace with:**
```python
        for root, dirs, files in os.walk(self.template_dir):
            # Session filter: skip session directories not in allowed_sessions
            rel_root = os.path.relpath(root, self.template_dir)
            parts = rel_root.split(os.sep)
            if len(parts) >= 1 and parts[0] != '.':
                dir_name = parts[0]
                # Session dirs are named like "01_data_pipeline_automation"
                if len(dir_name) >= 2 and dir_name[:2].isdigit():
                    session_num = int(dir_name[:2])
                    if session_num not in self.allowed_sessions:
                        dirs[:] = []
                        continue
```

> **Note:** This block must be inserted as the FIRST lines inside the `for root, dirs, files in os.walk(...)` loop body, before the existing `# Skip noise directories` comment.

---

## File 4 — `_factory/core/manifest_validator.py` ✅ DONE

**Path:** `_factory/core/manifest_validator.py`
**Action:** Create new file

```python
VALID_AUDIENCES = [
    "Executive / C-Suite",
    "Business Analyst",
    "Developer / Engineer",
    "Data Scientist",
    "Product Manager",
]

VALID_TONES = [
    "Strategic & Analytical",
    "Technical & Precise",
    "Practical & Applied",
    "Conversational & Accessible",
]

VALID_COMPLIANCE = ["None", "GDPR", "HIPAA", "SOX", "ISO 27001"]
VALID_REGIONS = ["Global", "EU", "US", "APAC", "Middle East"]

DEFAULTS = {
    "industry": "Generic AI",
    "tracks": ["base", "integrated", "architect"],
    "audience": "Developer / Engineer",
    "use_cases": [],
    "sessions": [1, 2, 3, 4, 5, 6, 7, 8],
    "tone": "Practical & Applied",
    "compliance_framework": "None",
    "region": "Global",
}


def validate_and_fill(manifest: dict) -> tuple[dict, list[str]]:
    """
    Apply defaults for missing fields and validate known fields.
    Returns (filled_manifest, list_of_warnings).
    """
    warnings = []
    filled = {**DEFAULTS, **manifest}

    if filled["audience"] not in VALID_AUDIENCES:
        warnings.append(
            f"Invalid audience '{filled['audience']}'. Defaulting to 'Developer / Engineer'."
        )
        filled["audience"] = "Developer / Engineer"

    if not isinstance(filled["sessions"], list) or not all(
        isinstance(s, int) and 1 <= s <= 8 for s in filled["sessions"]
    ):
        warnings.append(
            f"Invalid sessions value '{filled['sessions']}'. Defaulting to all 8 sessions."
        )
        filled["sessions"] = list(range(1, 9))

    if filled["compliance_framework"] not in VALID_COMPLIANCE:
        warnings.append(
            f"Invalid compliance_framework '{filled['compliance_framework']}'. Defaulting to 'None'."
        )
        filled["compliance_framework"] = "None"

    if filled["region"] not in VALID_REGIONS:
        warnings.append(
            f"Invalid region '{filled['region']}'. Defaulting to 'Global'."
        )
        filled["region"] = "Global"

    if filled["tone"] not in VALID_TONES:
        warnings.append(
            f"Invalid tone '{filled['tone']}'. Defaulting to 'Practical & Applied'."
        )
        filled["tone"] = "Practical & Applied"

    return filled, warnings
```

### Wire validator into compiler `__init__`

After the manifest is loaded in `compiler.py` `__init__` (after line 45), add:

```python
        try:
            from _factory.core.manifest_validator import validate_and_fill
        except ImportError:
            from core.manifest_validator import validate_and_fill
        self.manifest, validation_warnings = validate_and_fill(self.manifest)
        for w in validation_warnings:
            print(f"[MANIFEST WARNING] {w}")
```

---

## File 5 — `.agent/skills/factory/context_refiner.py` ✅ DONE

**Path:** `.agent/skills/factory/context_refiner.py`

### Change 5a — Read REFINER_TONE at top of `refine_markdown()` (line 92)

**After:**
```python
def refine_markdown(file_path, industry_name, industry_slug):
    """Surgically rewrite only Introduction/Business Value sections for the target industry."""
    print(f"✨ Refining {os.path.basename(file_path)} for {industry_name}...")
```

**Add immediately after the docstring print:**
```python
    tone = os.environ.get("REFINER_TONE", "Practical & Applied")
```

### Change 5b — Inject tone into prompt (lines 109–121)

**Remove:**
```python
    prompt = f"""You are a technical curriculum expert rewriting sections for the {industry_name} industry.

Rewrite each section below. Rules:
1. Replace generic analogies with {industry_name}-specific ones
2. Keep all technical terms, commands, and code references identical
3. Match the tone and vocabulary of {industry_name} professionals
4. Return ONLY the rewritten sections in this exact format:
   ## SECTION: <original heading>
   <rewritten body>
   ## END_SECTION

Sections to rewrite:
{extracted_text}"""
```

**Replace with:**
```python
    TONE_INSTRUCTIONS = {
        "Strategic & Analytical": "Use executive language: ROI, stakeholder outcomes, governance, risk-adjusted returns, strategic imperatives.",
        "Technical & Precise":    "Use engineering register: system architecture, implementation details, performance characteristics, failure modes.",
        "Practical & Applied":    "Use practitioner language: step-by-step workflows, real-world constraints, operational trade-offs.",
        "Conversational & Accessible": "Use plain, approachable language: relatable analogies, jargon-free explanations, encourage curiosity.",
    }
    tone_instruction = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["Practical & Applied"])

    prompt = f"""You are a technical curriculum expert rewriting sections for the {industry_name} industry.

Tone: {tone}
Tone guidance: {tone_instruction}

Rewrite each section below. Rules:
1. Replace generic analogies with {industry_name}-specific ones
2. Keep all technical terms, commands, and code references identical
3. Match the tone and vocabulary described above
4. Return ONLY the rewritten sections in this exact format:
   ## SECTION: <original heading>
   <rewritten body>
   ## END_SECTION

Sections to rewrite:
{extracted_text}"""
```

> **Note:** The `TONE_INSTRUCTIONS` dict and `tone_instruction` variable must be defined **before** the `prompt = f"""...` line. The `tone` variable (from Change 5a) must already be in scope.

---

## Verification Tests

### Test 1 — Catalog loads correctly
```python
import yaml
with open("_factory/catalog/courses.yaml") as f:
    catalog = yaml.safe_load(f)
assert len(catalog["courses"]) >= 15
assert all("id" in c and "use_cases" in c for c in catalog["courses"])
print("PASS: Catalog has 15+ entries with required fields")
```

### Test 2 — Session filtering
Build with `sessions: [1, 3]` in manifest. Verify `dist/` output contains only:
- `01_data_pipeline_automation/`
- `03_multi_agent_systems/`

No directories starting with `02`, `04`, `05`, `06`, `07`, `08` should exist.

### Test 3 — use_cases appear in LLM context
Call `generate_llm_context()` with `use_cases: ["Fraud Detection"]` in manifest.
The returned `data_scenario` field should reference fraud-related concepts.

### Test 4 — Tone flows into refiner
```bash
REFINER_TONE="Strategic & Analytical" python3 .agent/skills/factory/context_refiner.py \
  dist/test/README.md "AI for Finance" "ai_for_finance"
# Output should contain words like: ROI, stakeholder, governance

REFINER_TONE="Technical & Precise" python3 .agent/skills/factory/context_refiner.py \
  dist/test/README.md "AI for Finance" "ai_for_finance"
# Output should contain engineering language
```

### Test 5 — UI renders without errors
```bash
streamlit run _factory/ui/control_tower.py
```
Checklist:
- [ ] Catalog dropdown shows 15 courses
- [ ] Selecting a course pre-fills use cases, sessions, tone, compliance, region
- [ ] Duration preset auto-checks session boxes
- [ ] Audience radio auto-sets tracks
- [ ] Preview card updates in real time
- [ ] Build button writes correct manifest with all 8 fields

---

## Summary of What Changes

| Dimension | Before | After |
|---|---|---|
| Industry | Free text box | Catalog of 15 + custom fallback |
| Use Case | Not captured | 1–4 use case tags, fed into LLM prompt |
| Audience | Not captured | 5 persona types → auto-set tracks |
| Session Scope | All 8 always | Duration picker or manual checkbox select |
| Compliance | Not captured | 5 frameworks → injected into LLM prompt |
| Region | Not captured | 5 regions → injected into LLM prompt |
| Tone / Voice | Manifest only, never used | UI picker → wired to context_refiner |
| Manifest fields used by compiler | 2 of 7 | All 8 fields consumed |
