import streamlit as st

# --- 1. SET PAGE CONFIG ---
st.set_page_config(
    page_title="Alpha Deep Voice", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. AUTHENTICATION STATE ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 3. DEFINE THE PAGES (The Navigation Links) ---
login_page = st.Page("login.py", title="Login", icon="🔐")
home_page = st.Page("home_dashboard.py", title="Alpha Home", icon="🏠")
voice_lab = st.Page("pages/0_Voice_Lab.py", title="Voice Lab (Original)", icon="🎙️")
drill_page = st.Page("pages/1_Alpha_Drills.py", title="Alpha Drill Mode", icon="🏋️")
stats_page = st.Page("pages/2_Progress_Stats.py", title="My Progress", icon="📈")
# --- ADD THIS LINE BELOW TO FIX THE ERROR ---
sub_page = st.Page("pages/Subscription.py", title="Alpha Membership", icon="💎")

# --- 4. THE ROUTER LOGIC ---
if st.session_state.logged_in:
    # This structure creates the sections in your sidebar
    pg = st.navigation({
        "Main Hub": [home_page, voice_lab], 
        "Training Systems": [drill_page],
        "Intelligence": [stats_page, sub_page]  # Now sub_page is defined!
    })
else:
    pg = st.navigation([login_page])

# --- 5. RUN THE APP ---
pg.run()