import streamlit as st
import os
import yaml
import subprocess
import time
import sys
import json
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(page_title="AI Curriculum Factory | Control Tower", layout="wide", page_icon="🛡️")
st.title("🛡️ Curriculum Factory | Mission Control")
st.markdown("---")


def load_catalog():
    catalog_path = Path("_factory/catalog/courses.yaml")
    if not catalog_path.exists():
        return []
    with open(catalog_path) as f:
        data = yaml.safe_load(f)
    return data.get("courses", [])


# Sidebar
st.sidebar.header("🚀 Mission Configuration")
engine_mode = st.sidebar.selectbox("LLM Engine", ["Local (Ollama)", "Turbo (Gemini)"], index=0)
mode_val = "cloud" if "Turbo" in engine_mode else "local"

st.sidebar.markdown("---")
st.sidebar.header("⚔️ Build Guardian")
dist_dir = "dist"
if os.path.exists(dist_dir):
    builds = [d for d in os.listdir(dist_dir) if os.path.isdir(os.path.join(dist_dir, d))]
    selected_build = st.sidebar.selectbox("Select Build to Verify", builds if builds else ["None"])
    if st.sidebar.button("🛡️ Run Guardian Check"):
        if selected_build != "None":
            st.sidebar.info(f"Running Guardian for {selected_build}...")
            test_script = os.path.join(dist_dir, selected_build, "tests.py")
            if os.path.exists(test_script):
                result = subprocess.run([sys.executable, test_script], capture_output=True, text=True)
                st.sidebar.text_area("Guardian Report", result.stdout, height=150)
            else:
                st.sidebar.error("Tests script not found in build.")

tab1, tab2, tab3 = st.tabs(["🏗️ Course Builder", "📊 Live Mission Feed", "🧬 Industry DNA"])

with tab1:
    st.subheader("Course Builder")

    catalog = load_catalog()
    catalog_labels = [c["label"] for c in catalog]
    catalog_map = {c["label"]: c for c in catalog}

    # ── Step 1: WHAT ──────────────────────────────────────────────────────────
    st.markdown("### Step 1 — WHAT: Course Selection")
    course_mode = st.radio("", ["Select from catalog", "Build custom course"], horizontal=True, key="course_mode")

    if course_mode == "Select from catalog" and catalog_labels:
        selected_label = st.selectbox("Choose a course", catalog_labels)
        selected_course = catalog_map[selected_label]
        industry = selected_course["industry"]
        default_use_cases = selected_course.get("use_cases", [])
        default_sessions = selected_course.get("default_sessions", list(range(1, 9)))
        default_tracks = selected_course.get("default_tracks", ["base", "integrated", "architect"])
        default_tone = selected_course.get("tone", "Practical & Applied")
        default_compliance = selected_course.get("compliance", ["None"])[0] if selected_course.get("compliance") else "None"
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
        "Executive / C-Suite":   ["base"],
        "Business Analyst":      ["base", "integrated"],
        "Developer / Engineer":  ["base", "integrated", "architect"],
        "Data Scientist":        ["integrated", "architect"],
        "Product Manager":       ["base", "integrated"],
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
        "Half-day (2 sessions)":      [1, 2],
        "Full-day (4 sessions)":      [1, 2, 3, 4],
        "3-Day Sprint (6 sessions)":  [1, 2, 3, 4, 6, 7],
        "Full Bootcamp (8 sessions)": list(range(1, 9)),
        "Custom":                     None,
    }

    duration = st.selectbox("Duration Preset", list(DURATION_PRESETS.keys()), index=3)
    preset_sessions = DURATION_PRESETS[duration] or default_sessions

    col1, col2 = st.columns(2)
    sessions = []
    for i, (num, label) in enumerate(SESSION_LABELS.items()):
        col = col1 if i < 4 else col2
        if col.checkbox(label, value=num in preset_sessions, key=f"session_{num}"):
            sessions.append(num)

    st.markdown("---")

    # ── Step 4: CONTEXT ───────────────────────────────────────────────────────
    st.markdown("### Step 4 — CONTEXT: Optional Configuration")
    ctx_col1, ctx_col2, ctx_col3 = st.columns(3)

    COMPLIANCE_OPTIONS = ["None", "GDPR", "HIPAA", "SOX", "ISO 27001"]
    REGION_OPTIONS = ["Global", "EU", "US", "APAC", "Middle East"]
    TONE_OPTIONS = ["Auto", "Strategic & Analytical", "Technical & Precise", "Practical & Applied", "Conversational & Accessible"]

    compliance = ctx_col1.selectbox(
        "Compliance Framework", COMPLIANCE_OPTIONS,
        index=COMPLIANCE_OPTIONS.index(default_compliance) if default_compliance in COMPLIANCE_OPTIONS else 0
    )
    region = ctx_col2.selectbox(
        "Region", REGION_OPTIONS,
        index=REGION_OPTIONS.index(default_region) if default_region in REGION_OPTIONS else 0
    )
    tone = ctx_col3.selectbox(
        "Tone / Voice", TONE_OPTIONS,
        index=TONE_OPTIONS.index(default_tone) if default_tone in TONE_OPTIONS else 0
    )
    resolved_tone = default_tone if tone == "Auto" else tone

    st.markdown("---")

    # ── Course Preview Card ───────────────────────────────────────────────────
    st.markdown("### Course Preview")
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

with tab2:
    st.subheader("Live Mission Feed (Telemetry)")
    if os.path.exists("_factory/logs/events.jsonl"):
        with open("_factory/logs/events.jsonl", "r") as f:
            log_entries = [json.loads(line) for line in f.readlines()]
        for entry in reversed(log_entries[-50:]):
            color = "blue" if entry['level'] == "INFO" else "orange" if entry['level'] == "WARNING" else "red"
            st.markdown(f"**[{entry['timestamp'].split('T')[1][:8]}]** :{color}[{entry['level']}] {entry['event']}")
    else:
        st.info("No active mission logs found.")

with tab3:
    st.subheader(f"Historical Evolution: {industry}")
    if st.button("Generate Timeline"):
        from _factory.core.compiler import FactoryCompiler
        temp_manifest = "_factory/manifests/temp.yaml"
        with open(temp_manifest, 'w') as f:
            yaml.dump({"industry": industry}, f)
        comp = FactoryCompiler(temp_manifest, engine_mode=mode_val)
        with st.spinner("Extracting DNA Milestone..."):
            prompt = f"Generate a 2011-2026 AI evolution timeline for {industry}. Markdown table: Year | Milestone | Impact."
            content = comp.call_llm(prompt)
            if content:
                st.markdown(content)
            else:
                st.error("Failed to generate timeline.")

st.sidebar.markdown("---")
st.sidebar.markdown("**Status:** Operational")
st.sidebar.markdown("**User:** Supportive Facilitator")
