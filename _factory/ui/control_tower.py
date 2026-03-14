import streamlit as st
import os
import yaml
import subprocess
import time
import sys
import json

# Add sibling directory to path to import compiler logic
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

st.set_page_config(page_title="AI Curriculum Factory | Control Tower", layout="wide", page_icon="🛡️")

st.title("🛡️ Curriculum Factory | Mission Control")
st.markdown("---")

# Sidebar: Mission Configuration
st.sidebar.header("🚀 Mission Configuration")
industry = st.sidebar.text_input("Target Industry", "AI for Cyber-Security")
engine_mode = st.sidebar.selectbox("LLM Engine", ["Local (Ollama)", "Turbo (Gemini)"], index=0)
mode_val = "cloud" if "Turbo" in engine_mode else "local"

tracks = st.sidebar.multiselect("Active Tracks", ["Base", "Integrated", "Architect"], default=["Base", "Integrated", "Architect"])

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

# Main Interface: Tabs
tab1, tab2, tab3 = st.tabs(["🏗️ Active Build", "📊 Live Mission Feed", "🧬 Industry DNA"])

with tab1:
    if st.sidebar.button("Initiate Factory Build"):
        st.session_state['build_active'] = True
        
        # Create manifest
        manifest_data = {
            "industry": industry,
            "tracks": [t.lower() for t in tracks]
        }
        manifest_path = "_factory/manifests/mission_build.yaml"
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        with open(manifest_path, 'w') as f:
            yaml.dump(manifest_data, f)
            
        # Clear old logs for fresh feed
        if os.path.exists("_factory/logs/events.jsonl"):
            os.remove("_factory/logs/events.jsonl")
            
        st.info(f"Launching Build: {industry} in {mode_val.upper()} mode...")
        
        # Run compiler in background process to allow UI updates via log tailing
        with st.spinner("Factory Engine Running..."):
            compiler_path = "_factory/factory_compiler.py"
            env = os.environ.copy()
            # Note: User needs to ensure GOOGLE_API_KEY is in env if using cloud
            process = subprocess.Popen([sys.executable, compiler_path, manifest_path, "--mode", mode_val], env=env)
            
            # Simple polling of the log file for UI feedback
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
                st.success(f"🌟 Build for '{industry}' completed successfully!")
                st.balloons()
            else:
                st.error("❌ Build failed. Check the Mission Feed for details.")

with tab2:
    st.subheader("Live Mission Feed (Telemetry)")
    if os.path.exists("_factory/logs/events.jsonl"):
        with open("_factory/logs/events.jsonl", "r") as f:
            log_entries = [json.loads(line) for line in f.readlines()]
            # Display last 50 entries
            for entry in reversed(log_entries[-50:]):
                color = "blue" if entry['level'] == "INFO" else "orange" if entry['level'] == "WARNING" else "red"
                st.markdown(f"**[{entry['timestamp'].split('T')[1][:8]}]** :{color}[{entry['level']}] {entry['event']}")
    else:
        st.info("No active mission logs found.")

with tab3:
    st.subheader(f"Historical Evolution: {industry}")
    if st.button("Generate Timeline"):
        from _factory.core.compiler import FactoryCompiler
        # Use a temporary compiler for timeline generation
        temp_manifest = "_factory/manifests/temp.yaml"
        with open(temp_manifest, 'w') as f: yaml.dump({"industry": industry}, f)
        comp = FactoryCompiler(temp_manifest, engine_mode=mode_val)
        
        with st.spinner("Extracting DNA Milestone..."):
            prompt = f"Generate a 2011-2026 AI evolution timeline for {industry}. Markdown table: Year | Milestone | Impact."
            content = comp.call_llm(prompt)
            if content: st.markdown(content)
            else: st.error("Failed to generate timeline.")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Status:** Operational")
st.sidebar.markdown(f"**User:** Supportive Facilitator")
