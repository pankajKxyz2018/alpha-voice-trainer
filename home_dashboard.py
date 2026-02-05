import streamlit as st
import json
import time
import os
import random
import pandas as pd
from datetime import datetime
from voice_engine import analyze_mic_input

# --- 1. DATA & HISTORY LOGGING ---
def load_alpha_content():
    try:
        paths = ['words.json', 'Alpha_Male_Deep_Voice/words.json']
        data = {}
        for p in paths:
            if os.path.exists(p):
                with open(p, 'r') as f: data = json.load(f)
                break
        all_content = []
        for cat in data: 
            all_content.extend([s for s in data[cat] if len(str(s).split()) > 3])
        return all_content if all_content else ["Command the room with your resonance."]
    except: return ["Focus on diaphragm support."]

def log_progress(score, target):
    file_path = "alpha_progress.csv"
    data = {"Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "Alpha_Score": [score]}
    df = pd.DataFrame(data)
    df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)

# --- 2. SESSION STATE ---
if 'is_recording' not in st.session_state: st.session_state.is_recording = False
if 'start_time' not in st.session_state: st.session_state.start_time = 0
if 'current_sentence' not in st.session_state: st.session_state.current_sentence = "Ready to start."

metrics = ["v_deep", "v_alpha", "v_tone", "v_clarity", "v_accent", "v_pitch", "v_freq", "v_chest", "v_belly", "v_res"]
for m in metrics: 
    if m not in st.session_state: st.session_state[m] = 0

all_sentences = load_alpha_content()

# --- 3. THE UI LAYOUT ---
st.title("⚡ Alpha Voice Mastery")

# Sidebar: Target Goal
with st.sidebar:
    st.header("🎯 Training Target")
    target_goal = st.slider("Goal %", 50, 100, 85)
    st.divider()
    if os.path.exists("alpha_progress.csv"):
        st.subheader("📈 History")
        history_df = pd.read_csv("alpha_progress.csv")
        st.line_chart(history_df.set_index("Date")["Alpha_Score"])

# Center Section: Timer and Controls
c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    session_mins = st.selectbox("⏳ Session Duration", [1, 2, 3, 5], index=0)

with c2:
    st.write("") 
    if not st.session_state.is_recording:
        # FIXED: Changed use_container_width to width='stretch'
        if st.button("🎤 START TRAINING", width='stretch', type="primary"):
            st.session_state.is_recording = True
            st.session_state.start_time = time.time()
            st.session_state.current_sentence = random.choice(all_sentences)
            st.rerun()
    else:
        # FIXED: Changed use_container_width to width='stretch'
        if st.button("🛑 STOP SESSION", width='stretch'):
            st.session_state.is_recording = False
            st.rerun()

with c3:
    if st.session_state.is_recording:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, (session_mins * 60) - elapsed)
        st.metric("Time Remaining", f"{int(remaining)}s")
        if remaining <= 0:
            st.session_state.is_recording = False
            st.rerun()

st.divider()

# Main Training Area
col_left, col_right = st.columns([1.5, 1])

with col_left:
    box_color = "#2ecc71" if st.session_state.v_alpha >= target_goal else "#00BCFF"
    st.markdown(f"""
        <div style="background-color:#111; padding:60px; border-radius:15px; border: 4px solid {box_color}; min-height:280px; display:flex; align-items:center; justify-content:center;">
            <h1 style="color:white; text-align:center; font-family:serif; line-height:1.4;">"{st.session_state.current_sentence}"</h1>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.is_recording:
        with st.spinner("Analyzing Resonance..."):
            res = analyze_mic_input(duration=5)
            st.session_state.update({
                "v_deep": res['sub100'], "v_alpha": res['alpha'], "v_tone": res['chest'],
                "v_clarity": res['gravel'], "v_accent": res['gravel'], "v_pitch": res['sub100'],
                "v_freq": res['sub100'], "v_chest": res['chest'], "v_belly": res['belly'],
                "v_res": res['alpha']
            })
            if res['alpha'] >= target_goal:
                log_progress(res['alpha'], target_goal)
                st.balloons()
            
            # Move sequentially instead of random fast change
if "sentence_index" not in st.session_state:
    st.session_state.sentence_index = 0

st.session_state.sentence_index += 1
st.session_state.current_sentence = all_sentences[
    st.session_state.sentence_index % len(all_sentences)
]

st.rerun()

with col_right:
    st.subheader("📊 Alpha Metrics")
    # These sliders are fine; they use 'key' which is not deprecated.
    st.slider("Alpha Deep Voice", 0, 100, key="v_deep")
    st.slider("Alpha Depth (Overall)", 0, 100, key="v_alpha")
    st.slider("Alpha Male Tone", 0, 100, key="v_tone")
    st.slider("Alpha Clarity", 0, 100, key="v_clarity")
    st.slider("Alpha Accent", 0, 100, key="v_accent")
    st.slider("Alpha Pitch", 0, 100, key="v_pitch")
    st.slider("Alpha Frequency", 0, 100, key="v_freq")
    st.slider("Chest Power Usage", 0, 100, key="v_chest")
    st.slider("Belly (Diaphragm) Usage", 0, 100, key="v_belly")
    
    st.markdown("---")
    st.write(f"### Current Resonance: {st.session_state.v_res}%")