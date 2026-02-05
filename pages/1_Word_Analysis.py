import streamlit as st
import json
import os
from voice_engine import analyze_mic_input

# --- 1. DATA LOADING ---
def load_alpha_words():
    try:
        paths = ['words.json', 'Alpha_Male_Deep_Voice/words.json']
        data = {}
        for p in paths:
            if os.path.exists(p):
                with open(p, 'r') as f: data = json.load(f)
                break
        words = []
        for cat in data:
            words.extend([w for w in data[cat] if len(str(w).split()) == 1])
        return words if words else ["ALPHA"]
    except: return ["POWER"]

# --- 2. SESSION STATE ---
if 'w_idx' not in st.session_state: st.session_state.w_idx = 0
w_metrics = ["w_deep", "w_depth", "w_freq", "w_tone", "w_overall"]
for m in w_metrics:
    if m not in st.session_state: st.session_state[m] = 0

all_words = load_alpha_words()
current_word = all_words[st.session_state.w_idx % len(all_words)]

# --- 3. UI LAYOUT ---
st.set_page_config(layout="wide")
st.title("🎯 Word Analysis: Deep Resonance Drill")

# Word Display
st.markdown(f"""
    <div style="background:#000; padding:40px; border-radius:15px; border:2px solid #00BCFF; text-align:center;">
        <h1 style="color:white; font-size:80px; margin:0;">{current_word}</h1>
    </div>
""", unsafe_allow_html=True)

st.write("###")

# --- 4. THE LABELED METRICS ---
def display_stat(label, value):
    # Forced Label inside a blue box for maximum visibility
    st.markdown(f"""
        <div style="background:#00BCFF; color:black; padding:5px; border-radius:5px; text-align:center; font-weight:bold; margin-bottom:5px;">
            {label.upper()}
        </div>
    """, unsafe_allow_html=True)
    st.metric(label="", value=f"{value}%")
    st.progress(value / 100)

c1, c2, c3 = st.columns(3)
with c1: display_stat("Alpha Deep Voice", st.session_state.w_deep)
with c2: display_stat("Alpha Depth", st.session_state.w_depth)
with c3: display_stat("Frequency", st.session_state.w_freq)

st.write("###")
c4, c5 = st.columns(2)
with c4: display_stat("Alpha Male Tone", st.session_state.w_tone)
with c5: display_stat("Overall Score", st.session_state.w_overall)

# --- 5. ACTION (Fixing the 'width' error here) ---
st.write("###")
if st.button("🎤 ANALYZE WORD", width='stretch', type="primary"):
    with st.spinner("Processing Resonance..."):
        res = analyze_mic_input(duration=2)
        st.session_state.update({
            "w_deep": res['sub100'], "w_depth": res['alpha'],
            "w_freq": res['sub100'], "w_tone": res['chest'],
            "w_overall": res['alpha']
        })
        st.session_state.w_idx += 1
        st.rerun()