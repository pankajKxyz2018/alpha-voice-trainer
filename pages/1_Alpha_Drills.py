import streamlit as st
import json
import random
import time
import os
import plotly.graph_objects as go
from voice_engine import analyze_mic_input # Ensure voice_engine.py is in your root folder

# --- SECTION 1: DATA LOADING ---
def load_alpha_words():
    try:
        with open('words.json', 'r') as f:
            data = json.load(f)
        return (
            data.get("Level_1_Chest_Resonance", []) + 
            data.get("Level_2_Belly_Involvement", []) + 
            data.get("Level_3_Gravel_Texture", []) + 
            data.get("Level_4_Alpha_Mastery", []) +
            data.get("Level_5_Sentences", [])
        )
    except Exception as e:
        return ["GROUND", "BOOM", "ALPHA VOICE", "RESONANCE"]

# --- SECTION 2: UI GENERATORS ---
def create_meter(label, value, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': label, 'font': {'size': 18, 'color': '#111'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "rgba(255,255,255,0.05)",
            'threshold': {'line': {'color': "white", 'width': 4}, 'value': 85}
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=220, margin=dict(l=20,r=20,t=50,b=20))
    return fig

# --- SECTION 3: SESSION STATE ---
if 'all_words' not in st.session_state: st.session_state.all_words = load_alpha_words()
if 'word_idx' not in st.session_state: st.session_state.word_idx = 0
if 'chance' not in st.session_state: st.session_state.chance = 1
if 'timer' not in st.session_state: st.session_state.timer = 30
if 'last_scores' not in st.session_state: 
    st.session_state.last_scores = {"chest": 0, "belly": 0, "gravel": 0, "sub100": 0, "alpha": 0}

# --- SECTION 4: MAIN DASHBOARD UI ---
st.title("🏋️ Alpha Drill: The 1,000 Word Gym")

current_word = st.session_state.all_words[st.session_state.word_idx % len(st.session_state.all_words)]
is_sentence = len(current_word.split()) > 1

# Progress Dashboard
c1, c2, c3 = st.columns(3)
c1.metric("⏳ Timer", f"{st.session_state.timer}s")
c2.metric("🎯 Chance", f"{st.session_state.chance} / 5")
c3.metric("📚 Progress", f"{st.session_state.word_idx + 1} / {len(st.session_state.all_words)}")

# Big Display
border_color = "#00FF00" if not is_sentence else "#00BCFF"
st.markdown(f"""
    <div style="text-align:center; padding:40px; background-color:#1e1e1e; border: 3px solid {border_color}; border-radius:15px; margin-bottom:20px;">
        <p style="color:#888; margin:0; text-transform:uppercase; font-size:12px;">Current Target</p>
        <h1 style="color:white; font-size:70px; margin:0; line-height:1.1;">{current_word}</h1>
    </div>
""", unsafe_allow_html=True)

# Gauges Grid
col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)
s = st.session_state.last_scores

with col1: st.plotly_chart(create_meter("Chest Power", s['chest'], "#3498db"), use_container_width=True)
with col2: st.plotly_chart(create_meter("Belly Drive", s['belly'], "#e67e22"), use_container_width=True)
with col3: st.plotly_chart(create_meter("Gravel", s['gravel'], "#2ecc71"), use_container_width=True)
with col4: st.plotly_chart(create_meter("Sub-100Hz", s['sub100'], "#e74c3c"), use_container_width=True)
with col5: st.plotly_chart(create_meter("Alpha Depth", s['alpha'], "#9b59b6"), use_container_width=True)

# --- SECTION 5: INTERACTION & SAVING ---
rec_duration = 5 if is_sentence else 2
btn_label = f"🎤 RECORD {'SENTENCE' if is_sentence else 'WORD'} ({rec_duration} Secs)"

if st.button(btn_label, use_container_width=True, type="primary"):
    with st.spinner(f"Alpha Ear listening for {rec_duration}s..."):
        scores = analyze_mic_input(duration=rec_duration) 
        st.session_state.last_scores = scores
        
        # Perfection Check: All parameters must be >= 85
        if all(val >= 85 for val in scores.values()):
            # --- PROGRESS SAVING LOGIC ---
            new_entry = scores.copy()
            new_entry['word'] = current_word
            new_entry['timestamp'] = time.time()
            
            history = []