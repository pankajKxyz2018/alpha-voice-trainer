import streamlit as st
import json
import time
import os
import pandas as pd
from datetime import datetime
from voice_engine import analyze_mic_input

# -------------------------
# LOAD SENTENCES
# -------------------------
def load_alpha_content():
    try:
        with open("sentences.txt", "r", encoding="utf-8") as f:
            return [x.strip() for x in f.readlines() if x.strip()]
    except:
        return ["Focus on diaphragm support."]

all_sentences = load_alpha_content()

# -------------------------
# SESSION STATE INIT
# -------------------------
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

if "sentence_index" not in st.session_state:
    st.session_state.sentence_index = 0

if "last_sentence_switch" not in st.session_state:
    st.session_state.last_sentence_switch = 0

metrics = ["v_deep","v_alpha","v_tone","v_clarity","v_accent","v_pitch","v_freq","v_chest","v_belly","v_res"]

for m in metrics:
    if m not in st.session_state:
        st.session_state[m] = 0

# -------------------------
# UI
# -------------------------
st.title("⚡ Alpha Voice Mastery")

with st.sidebar:
    st.header("🎯 Training Target")
    target_goal = st.slider("Goal %",50,100,85)

c1,c2,c3 = st.columns([1,1,1])

with c1:
    session_mins = st.selectbox("⏳ Session Duration",[1,2,3,5],index=0)

with c2:
    if not st.session_state.is_recording:
        if st.button("🎤 START TRAINING",type="primary",use_container_width=True):
            st.session_state.is_recording = True
            st.session_state.start_time = time.time()
            st.session_state.last_sentence_switch = time.time()
            st.rerun()
    else:
        if st.button("🛑 STOP SESSION",use_container_width=True):
            st.session_state.is_recording=False
            st.rerun()

with c3:
    if st.session_state.is_recording:
        elapsed=time.time()-st.session_state.start_time
        remaining=max(0,(session_mins*60)-elapsed)
        st.metric("Time Remaining",f"{int(remaining)}s")

# -------------------------
# MAIN AREA
# -------------------------
col_left,col_right = st.columns([1.5,1])

with col_left:

    # ---------- AUTO LOOP (KEY FIX) ----------
    if st.session_state.is_recording:

        now=time.time()

        # change sentence every 5 sec
        if now - st.session_state.last_sentence_switch > 5:
            st.session_state.sentence_index +=1
            st.session_state.last_sentence_switch = now

        # analyze only every 5 sec
        res = analyze_mic_input(duration=3)

        # ignore fake silent values
        if res["alpha"] > 0:
            st.session_state.update({
                "v_deep":res["sub100"],
                "v_alpha":res["alpha"],
                "v_tone":res["chest"],
                "v_clarity":res["gravel"],
                "v_accent":res["gravel"],
                "v_pitch":res["sub100"],
                "v_freq":res["sub100"],
                "v_chest":res["chest"],
                "v_belly":res["belly"],
                "v_res":res["alpha"]
            })

        time.sleep(1)
        st.rerun()

    current_sentence = all_sentences[
        st.session_state.sentence_index % len(all_sentences)
    ]

    box_color="#2ecc71" if st.session_state.v_alpha>=target_goal else "#00BCFF"

    st.markdown(f"""
        <div style="background:#111;padding:60px;border-radius:15px;border:4px solid {box_color};
        min-height:280px;display:flex;align-items:center;justify-content:center;">
        <h1 style="color:white;text-align:center;font-family:serif;">
        "{current_sentence}"
        </h1>
        </div>
    """,unsafe_allow_html=True)

# -------------------------
# RIGHT SIDE METRICS
# -------------------------
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

