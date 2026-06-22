import streamlit as st

st.set_page_config(
    page_title="Rekxare Dami",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS for Nav Bar ──
st.markdown("""
<style>
/* Top Navigation Bar */
.stApp > header {
    background: rgba(26, 26, 46, 0.92) !important;
    backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
    padding: 4px 16px !important;
}
.stApp > header a {
    color: #e2e2e2 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 8px 16px !important;
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}
.stApp > header a:hover {
    background: rgba(76, 175, 80, 0.12) !important;
    color: #4CAF50 !important;
}
.stApp > header a[aria-current="page"] {
    background: rgba(76, 175, 80, 0.15) !important;
    color: #4CAF50 !important;
}
/* Hide the default Streamlit sidebar toggle */
[data-testid="collapsedControl"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ── Navigation ──
pg = st.navigation([
    st.Page("Home.py", title="🏠 Home", icon="🏠"),
    st.Page("01_Schedule.py", title="📅 Schedule", icon="📅"),
    st.Page("02_About.py", title="ℹ️ About", icon="ℹ️"),
])

pg.run()
