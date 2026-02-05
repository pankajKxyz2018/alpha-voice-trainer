import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(page_title="Alpha Progress Stats", layout="wide")

# --- LOAD DATA ---
def load_history():
    if os.path.exists('progress.json'):
        with open('progress.json', 'r') as f:
            return json.load(f)
    return []

st.title("📈 Alpha Progress Analytics")

history = load_history()

if not history:
    st.info("No training data found. Complete some drills to see your stats!")
else:
    df = pd.DataFrame(history)
    
    # --- METRICS ROW ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Words Mastered", len(df))
    c2.metric("Avg Alpha Depth", f"{int(df['alpha'].mean())}%")
    c3.metric("Peak Resonance", f"{df['alpha'].max()}%")

    # --- PROGRESS OVER TIME ---
    st.subheader("Vocal Growth Timeline")
    fig_line = px.line(df, x=df.index, y=['chest', 'belly', 'gravel', 'alpha'],
                      title="Resonance Evolution",
                      labels={'index': 'Attempts', 'value': 'Percentage'},
                      template="plotly_dark",
                      color_discrete_sequence=["#3498db", "#e67e22", "#2ecc71", "#9b59b6"])
    st.plotly_chart(fig_line, use_container_width=True)

    # --- VOCAL PROFILE (Radar Chart) ---
    st.subheader("Alpha Vocal Profile")
    avg_scores = df[['chest', 'belly', 'gravel', 'sub100']].mean().reset_index()
    avg_scores.columns = ['Metric', 'Score']
    
    fig_radar = px.line_polar(avg_scores, r='Score', theta='Metric', line_close=True,
                             template="plotly_dark", color_discrete_sequence=["#00FF00"])
    fig_radar.update_traces(fill='toself')
    st.plotly_chart(fig_radar, use_container_width=True)