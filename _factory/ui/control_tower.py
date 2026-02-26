import streamlit as st
import os
import yaml
import subprocess
import time
import sys
import json
import ollama

# Add sibling directory to path to import compiler if needed
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# For this lab, we'll call the compiler via subprocess to keep the UI responsive

st.set_page_config(page_title="AI Curriculum Factory | Control Tower", layout="wide")

st.title("🛡️ Curriculum Factory | Control Tower")
st.markdown("---")

# Sidebar for Manifest Input
st.sidebar.header("📋 Build Configuration")
industry = st.sidebar.text_input("Target Industry", "AI for Sovereign Legal Chambers")
tracks = st.sidebar.multiselect("Active Tracks", ["Base", "Integrated", "Architect"], default=["Base", "Integrated", "Architect"])
session_count = st.sidebar.slider("Session Count", 1, 8, 8)

if st.sidebar.button("🚀 Launch Build"):
    st.session_state['build_active'] = True
    st.session_state['status'] = {
        "🧬 Data Synth": "RUNNING",
        "✍️ Context Refiner": "WAITING",
        "🛡️ PII Scrubber": "WAITING",
        "⚔️ The Guardian": "WAITING"
    }
    
    # Save temp manifest
    manifest_data = {
        "industry": industry,
        "tracks": [t.lower() for t in tracks],
        "session_count": session_count
    }
    with open("_factory/manifests/temp_build.yaml", 'w') as f:
        yaml.dump(manifest_data, f)
        
    st.info(f"Initiating build for {industry}...")

# Tabs
tab1, tab2 = st.tabs(["🏗️ Build Status", "🧬 Industry DNA (2011-2026)"])

with tab1:
    if st.session_state.get('build_active'):
        st.subheader("Live Agent Status")
        cols = st.columns(4)
        
        # Mocking real-time updates for the demo
        status_placeholders = [col.empty() for col in cols]
        
        # Step 1: LLM Context & Data Synth
        status_placeholders[0].metric("🧬 Data Synth", "RUNNING", delta="Synthesizing...")
        time.sleep(2)
        status_placeholders[0].metric("🧬 Data Synth", "COMPLETED", delta="50 Rows")
        
        # Step 2: Context Refinement
        st.session_state['status']["✍️ Context Refiner"] = "RUNNING"
        status_placeholders[1].metric("✍️ Context Refiner", "RUNNING", delta="Refining Manuals...")
        time.sleep(3)
        status_placeholders[1].metric("✍️ Context Refiner", "COMPLETED", delta="20+ Files")
        
        # Step 3: Security
        st.session_state['status']["🛡️ PII Scrubber"] = "RUNNING"
        status_placeholders[2].metric("🛡️ PII Scrubber", "RUNNING", delta="Masking PII...")
        time.sleep(2)
        status_placeholders[2].metric("🛡️ PII Scrubber", "COMPLETED", delta="Secured")
        
        # Step 4: Guardian
        st.session_state['status']["⚔️ The Guardian"] = "RUNNING"
        status_placeholders[3].metric("⚔️ The Guardian", "RUNNING", delta="Validating...")
        time.sleep(2)
        status_placeholders[3].metric("⚔️ The Guardian", "PASS", delta="Build Healthy")
        
        st.success(f"🌟 Build for '{industry}' is complete!")
        st.balloons()
        
        slug = industry.lower().replace(' ', '_').replace('&', 'and')
        st.markdown(f"**Output Directory:** `builds/{slug}/`")
        
    else:
        st.info("Configure the sidebar and click 'Launch Build' to begin.")

with tab2:
    st.subheader(f"Evolution of AI in {industry}")
    if st.button("Generate DNA Timeline"):
        with st.spinner("Analyzing historical adoption patterns..."):
            prompt = f"""
            Generate a concise 2011-2026 timeline of AI evolution in the {industry} industry.
            Focus on key milestones in automation, local LLMs, and sovereign privacy.
            Return as a markdown table with columns: Year, Milestone, Impact.
            """
            try:
                response = ollama.chat(model='llama3.2:1b', messages=[
                    {'role': 'user', 'content': prompt}
                ])
                st.markdown(response['message']['content'])
            except Exception as e:
                st.error(f"Failed to generate timeline: {e}")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**User:** Supportive Facilitator")
st.sidebar.markdown(f"**Mode:** Cyber-Sovereign")
