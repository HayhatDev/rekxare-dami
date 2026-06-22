import streamlit as st

st.set_page_config(
    page_title="Rekxare Dami",
    page_icon="logo.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Navigation ──
pg = st.navigation([
    st.Page("Home.py", title="🏠 Home"),
    st.Page("01_Schedule.py", title="📅 Schedule"),
    st.Page("02_About.py", title="ℹ️ About"),
])

pg.run()
