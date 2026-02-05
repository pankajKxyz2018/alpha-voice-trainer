import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Alpha Mastery Certificate", page_icon="📜")

st.title("📜 Alpha Mastery Recognition")

if not os.path.exists("alpha_progress.csv"):
    st.warning("No training data found. Start training in Alpha Home to unlock your path to mastery.")
else:
    df = pd.read_csv("alpha_progress.csv")
    total_goals_met = len(df)
    highest_score = df["Alpha_Score"].max()

    # MASTER CRITERIA: 7 successful sessions
    if total_goals_met >= 7:
        st.balloons()
        st.success("### CONGRATULATIONS, ALPHA.")
        st.write("You have successfully rewired your vocal frequency to the Arjun Das standard.")
        
        # The Certificate UI
        st.markdown(f"""
            <div style="border: 10px solid #d4af37; padding: 50px; text-align: center; background-color: #111; color: white; border-radius: 15px;">
                <h1 style="color: #d4af37; font-family: serif; font-size: 50px;">CERTIFICATE OF COMPLETION</h1>
                <p style="font-size: 20px;">This certifies that the user has mastered the</p>
                <h2 style="letter-spacing: 5px; color: #00BCFF;">ALPHA MALE DEEP VOICE</h2>
                <p style="font-size: 20px;">Standard: <b>Arjun Das Resonance</b></p>
                <hr style="width: 50%; border: 1px solid #d4af37;">
                <p style="font-size: 18px;">Peak Performance Score: <b>{highest_score}%</b></p>
                <p style="font-size: 15px; color: gray;">Verified by Alpha Training Engine v2.0</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.button("🖨️ Print Certificate (Screenshot)")
        
    else:
        # Progress Bar towards Certificate
        st.info(f"Mastery Status: {total_goals_met} / 7 sessions completed.")
        progress = total_goals_met / 7
        st.progress(progress)
        st.write("Complete 7 high-performance sessions to unlock your official Alpha Certificate.")