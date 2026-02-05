# ==============================================
# ⚡ ALPHA VOICE MASTERY — REAL STREAM VERSION
# ==============================================

import streamlit as st
import json
import time
import os

# 🔴 REAL BROWSER MIC STREAM
from live_stream import start_live_stream


# --------------------------------------
# PAGE TITLE
# --------------------------------------
st.title("⚡ Alpha Voice Mastery")


# --------------------------------------
# LOAD SENTENCES
# --------------------------------------
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
            all_content.extend(
                [s for s in data[cat] if len(str(s).split()) > 3]
            )

        return all_content if all_content else [
            "Command the room with your resonance."
        ]

    except:
        return ["Focus on diaphragm support."]


all_sentences = load_alpha_content()


# --------------------------------------
# SESSION STATE INIT
# --------------------------------------
if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

if "sentence_index" not in st.session_state:
    st.session_state.sentence_index = 0

if "current_sentence" not in st.session_state:
    st.session_state.current_sentence = "Press START TRAINING"

if "v_res" not in st.session_state:
    st.session_state.v_res = 0


metrics = [
    "v_deep",
    "v_alpha",
    "v_tone",
    "v_clarity",
    "v_accent",
    "v_pitch",
    "v_freq",
    "v_chest",
    "v_belly"
]

for m in metrics:
    if m not in st.session_state:
        st.session_state[m] = 0


# --------------------------------------
# SIDEBAR
# --------------------------------------
with st.sidebar:
    target_goal = st.slider("🎯 Training Target", 50, 100, 85)


# --------------------------------------
# CONTROLS
# --------------------------------------
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    session_mins = st.selectbox("⏳ Session Duration", [1, 2, 3, 5])

with c2:
    if not st.session_state.is_recording:
        if st.button("🎤 START TRAINING", use_container_width=True):
            st.session_state.is_recording = True
            st.session_state.start_time = time.time()
            st.session_state.sentence_index = 0
            st.session_state.current_sentence = all_sentences[0]
    else:
        if st.button("🛑 STOP SESSION", use_container_width=True):
            st.session_state.is_recording = False

with c3:
    if st.session_state.is_recording:

        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, session_mins * 60 - elapsed)

        st.metric("Time Remaining", f"{remaining}s")

        if remaining <= 0:
            st.session_state.is_recording = False


st.divider()


# --------------------------------------
# MAIN LAYOUT
# --------------------------------------
col_left, col_right = st.columns([1.5, 1])


# --------------------------------------
# SENTENCE DISPLAY
# --------------------------------------
with col_left:

    border_color = "#2ecc71" if st.session_state.v_res >= target_goal else "#00BCFF"

    st.markdown(f"""
    <div style="
        background:#111;
        padding:60px;
        border-radius:15px;
        border:4px solid {border_color};
        min-height:260px;
        display:flex;
        align-items:center;
        justify-content:center;">
        <h1 style="color:white;text-align:center;font-family:serif;">
        "{st.session_state.current_sentence}"
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------
    # 🔴 REAL LIVE STREAM ENGINE
    # --------------------------------------
    if st.session_state.is_recording:

        res = start_live_stream()

        # Update sliders ONLY when audio exists
        if res:

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

            # 🔵 Move sentence SLOWLY
            if time.time() - st.session_state.start_time > 3:

                st.session_state.start_time = time.time()

                st.session_state.sentence_index += 1
                st.session_state.current_sentence = all_sentences[
                    st.session_state.sentence_index % len(all_sentences)
                ]


# --------------------------------------
# RIGHT SIDE SLIDERS
# --------------------------------------
with col_right:

    st.subheader("📊 Alpha Metrics")

    st.slider("Alpha Deep Voice", 0, 100, key="v_deep")
    st.slider("Alpha Depth", 0, 100, key="v_alpha")
    st.slider("Alpha Tone", 0, 100, key="v_tone")
    st.slider("Alpha Clarity", 0, 100, key="v_clarity")
    st.slider("Alpha Accent", 0, 100, key="v_accent")
    st.slider("Alpha Pitch", 0, 100, key="v_pitch")
    st.slider("Alpha Frequency", 0, 100, key="v_freq")
    st.slider("Chest Power", 0, 100, key="v_chest")
    st.slider("Belly Usage", 0, 100, key="v_belly")

    st.markdown("---")
    st.write(f"### Current Resonance: {st.session_state.v_res}%")


# --------------------------------------
# 🏆 HARD MODE MILESTONES
# --------------------------------------
scores = [st.session_state[m] for m in metrics]
min_score = min(scores)

st.markdown("---")

if min_score >= 97:
    st.success("🔥 EXCELLENT — Real Alpha Deep Male Voice Achieved.")
elif min_score >= 85:
    st.info("🚀 Bravo — Second Alpha Milestone reached.")
elif min_score >= 70:
    st.warning("🧭 Level 1 Alpha Deep Voice unlocked.")
