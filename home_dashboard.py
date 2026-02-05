import streamlit as st
import json
import time
import os
import random
import pandas as pd
from datetime import datetime
from voice_engine import analyze_mic_input

# -----------------------------
# 1. LOAD SENTENCES
# -----------------------------
def load_alpha_content():
    try:
        paths = ['words.json', 'Alpha_Male_Deep_Voice/words.json']
        data = {}
        for p in paths:
            if os.path.exists(p):
                with open(p, 'r') as f:
                    data = json.load(f)
                break

        all_content = []
        for cat in data:
            all_content.extend([s for s in data[cat] if len(str(s).split()) > 3])

        return all_content if all_content else ["Command the room with your resonance."]
    except:
        return ["Focus on diaphragm support."]

def log_progress(score):
    file_path = "alpha_progress.csv"
    data = {"Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")], "Alpha_Score": [score]}
    df = pd.DataFrame(data)
    df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)

all_sentences = load_alpha_content()

# -----------------------------
# 2. SESSION STATE
# -----------------------------
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

if "last_update" not in st.session_state:
    st.session_state.last_update = 0

if "sentence_index" not in st.session_state:
    st.session_state.sentence_index = 0

if "current_sentence" not in st.session_state:
    st.session_state.current_sentence = "Press START TRAINING"

metrics = [
    "v_deep","v_alpha","v_tone","v_clarity","v_accent",
    "v_pitch","v_freq","v_chest","v_belly","v_res"
]

for m in metrics:
    if m not in st.session_state:
        st.session_state[m] = 0

# -----------------------------
# 3. UI HEADER
# -----------------------------
st.title("⚡ Alpha Voice Mastery")

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.header("🎯 Training Target")
    target_goal = st.slider("Goal %", 50, 100, 85)

# -----------------------------
# TIMER CONTROLS
# -----------------------------
c1, c2, c3 = st.columns([1,1,1])

with c1:
    session_mins = st.selectbox("⏳ Session Duration", [1,2,3,5], index=0)

with c2:
    if not st.session_state.is_recording:
        if st.button("🎤 START TRAINING", use_container_width=True):
            st.session_state.is_recording = True
            st.session_state.start_time = time.time()
            st.session_state.last_update = time.time()
            st.session_state.sentence_index = 0
            st.session_state.current_sentence = all_sentences[0]
            st.rerun()
    else:
        if st.button("🛑 STOP SESSION", use_container_width=True):
            st.session_state.is_recording = False
            st.rerun()

with c3:
    if st.session_state.is_recording:
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, (session_mins * 60) - elapsed)
        st.metric("Time Remaining", f"{int(remaining)}s")

        if remaining <= 0:
            st.session_state.is_recording = False
            log_progress(st.session_state.v_alpha)
            st.balloons()
            st.rerun()

st.divider()

# -----------------------------
# MAIN LAYOUT
# -----------------------------
col_left, col_right = st.columns([1.5,1])

# -----------------------------
# LEFT: SENTENCE BOX
# -----------------------------
with col_left:

    box_color = "#2ecc71" if st.session_state.v_alpha >= target_goal else "#00BCFF"

    st.markdown(f"""
        <div style="background-color:#111; padding:60px; border-radius:15px;
        border:4px solid {box_color}; min-height:280px;
        display:flex; align-items:center; justify-content:center;">
        <h1 style="color:white; text-align:center; font-family:serif;">
        "{st.session_state.current_sentence}"
        </h1></div>
    """, unsafe_allow_html=True)

    # -----------------------------
    # REAL SESSION LOOP
    # -----------------------------
    if st.session_state.is_recording:

        now = time.time()

        # Every 5 sec update analysis + next sentence
        if now - st.session_state.last_update >= 5:

            res = analyze_mic_input(duration=2)

            st.session_state.update({
                "v_deep": res['sub100'],
                "v_alpha": res['alpha'],
                "v_tone": res['chest'],
                "v_clarity": res['gravel'],
                "v_accent": res['gravel'],
                "v_pitch": res['sub100'],
                "v_freq": res['sub100'],
                "v_chest": res['chest'],
                "v_belly": res['belly'],
                "v_res": res['alpha']
            })

            st.session_state.sentence_index += 1
            st.session_state.current_sentence = all_sentences[
                st.session_state.sentence_index % len(all_sentences)
            ]

            st.session_state.last_update = now
            st.rerun()

# -----------------------------
# RIGHT: SLIDERS
# -----------------------------
with col_right:
    st.subheader("📊 Alpha Metrics")

    st.slider("Alpha Deep Voice",0,100,key="v_deep")
    st.slider("Alpha Depth (Overall)",0,100,key="v_alpha")
    st.slider("Alpha Male Tone",0,100,key="v_tone")
    st.slider("Alpha Clarity",0,100,key="v_clarity")
    st.slider("Alpha Accent",0,100,key="v_accent")
    st.slider("Alpha Pitch",0,100,key="v_pitch")
    st.slider("Alpha Frequency",0,100,key="v_freq")
    st.slider("Chest Power Usage",0,100,key="v_chest")
    st.slider("Belly (Diaphragm) Usage",0,100,key="v_belly")

    st.markdown("---")
    st.write(f"### Current Resonance: {st.session_state.v_res}%")

# -----------------------------
# 🏆 ALPHA MILESTONE SYSTEM
# -----------------------------
scores = [
    st.session_state.v_deep,
    st.session_state.v_alpha,
    st.session_state.v_tone,
    st.session_state.v_clarity,
    st.session_state.v_accent,
    st.session_state.v_pitch,
    st.session_state.v_freq,
    st.session_state.v_chest,
    st.session_state.v_belly
]

min_score = min(scores)

st.markdown("---")

if min_score >= 97:
    st.success("🔥 EXCELLENT — You achieved REAL Alpha Deep Male Voice.")
elif min_score >= 85:
    st.info("🚀 Bravo — Second Alpha Milestone reached.")
elif min_score >= 70:
    st.warning("🧭 Level 1 Alpha Deep Voice unlocked.")


