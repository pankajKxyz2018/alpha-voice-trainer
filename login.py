import streamlit as st

st.title("🔐 Alpha Login")
st.write("Welcome to the 50-Member Alpha Inner Circle.")

if st.button("Enter Alpha Trainer"):
    st.session_state.logged_in = True
    st.rerun()