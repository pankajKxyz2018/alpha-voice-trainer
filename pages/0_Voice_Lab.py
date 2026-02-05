import streamlit as st
import plotly.graph_objects as go
from voice_engine import analyze_mic_input

# --- NO SET_PAGE_CONFIG HERE (It's already in app.py) ---

st.title("🎙️ Alpha Voice Lab: Original Full Analysis")
st.write("First 50 Alpha Members: This is your high-precision resonance lab.")

def create_gauge(label, value, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        title={'text': label, 'font': {'color': 'white', 'size': 16}},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': color}}
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=200, margin=dict(l=10,r=10,t=40,b=10))
    return fig

# Initialize session state for the "Auto-Flash" sliders if not present
if 'scores' not in st.session_state:
    st.session_state.scores = {"chest": 0, "belly": 0, "gravel": 0, "sub100": 0, "alpha": 0}

if st.button("🔴 START ANALYSIS", use_container_width=True):
    with st.spinner("Analyzing resonance, pitch, and accent..."):
        # Get data from the brain
        res = analyze_mic_input(duration=3)
        st.session_state.scores = res
        
        # --- TOP SECTION: THE ORIGINAL SLIDERS (HORIZONTAL) ---
        st.markdown("### 📊 Horizontal Metrics (Original View)")
        s = st.session_state.scores
        
        col_left, col_right = st.columns(2)
        with col_left:
            st.slider("Alpha Clarity (Accent)", 0, 100, s['gravel'], key="lab_acc")
            st.slider("Pitch Depth", 0, 100, s['sub100'], key="lab_pit")
        with col_right:
            st.slider("Chest Power", 0, 100, s['chest'], key="lab_chs")
            st.slider("Belly Involvement", 0, 100, s['belly'], key="lab_bel")

        st.divider()

        # --- BOTTOM SECTION: THE RADIAL GAUGES (PRO VIEW) ---
        st.markdown("### 🎯 Frequency Analysis")
        g1, g2, g3 = st.columns(3)
        with g1: st.plotly_chart(create_gauge("Chest Power", s['chest'], "#3498db"), use_container_width=True)
        with g2: st.plotly_chart(create_gauge("Belly Input", s['belly'], "#e67e22"), use_container_width=True)
        with g3: st.plotly_chart(create_gauge("Alpha Depth", s['alpha'], "#9b59b6"), use_container_width=True)

        st.success("Analysis Complete!")