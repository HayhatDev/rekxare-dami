import streamlit as st
import json

# Load translations
with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

if "lang" not in st.session_state:
    st.session_state.lang = "badini"

def t(key):
    return TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)

st.set_page_config(page_title="Login | Rekxare Dami", page_icon="🔐", layout="centered", initial_sidebar_state="collapsed")

# Clear any leftover session data
for key in ["logged_in", "user_email", "data_key"]:
    st.session_state.pop(key, None)

# Custom CSS (same dark design as your original login gate)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp, [data-testid="stAppViewContainer"],
section[data-testid="stMain"], .main, .main .block-container {
    background: linear-gradient(135deg, #0f0c29, #1a1a2e, #16213e) !important;
    font-family: 'Inter', system-ui, sans-serif !important;
}
header[data-testid="stHeader"], #MainMenu, footer,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {
    display: none !important;
}
.main .block-container {
    padding-top: max(20px, calc(50vh - 220px)) !important;
    padding-bottom: 40px !important;
    padding-left: 20px !important;
    padding-right: 20px !important;
    max-width: 440px !important;
}
.login-wrap { width: 100%; display: flex; flex-direction: column; align-items: center; }
.login-logo { font-size: 64px; line-height: 1; margin-bottom: 12px; filter: drop-shadow(0 4px 16px rgba(76,175,80,0.4)); animation: float 3s ease-in-out infinite; }
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
.login-title { font-size: 30px; font-weight: 900; letter-spacing: -0.8px; color: #ffffff; text-align: center; margin-bottom: 4px; }
.login-sub { font-size: 14px; color: rgba(255,255,255,0.55); text-align: center; margin-bottom: 32px; font-weight: 500; }
.login-card { background: rgba(0, 0, 0, 0.5) !important; border: 1.5px solid rgba(255,255,255,0.13); border-radius: 24px; padding: 32px 28px 28px; width: 100%; box-shadow: 0 8px 40px rgba(0,0,0,0.40), 0 1px 0 rgba(255,255,255,0.06) inset; backdrop-filter: blur(12px); }
.login-label { font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: rgba(255,255,255,0.5); margin-bottom: 8px; display: block; }
.login-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(76,175,80,0.15); border: 1px solid rgba(76,175,80,0.25); color: #81c784; border-radius: 20px; padding: 5px 14px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 24px; }
.login-footer { font-size: 12px; color: rgba(255,255,255,0.30); text-align: center; margin-top: 24px; }
.stTextInput input { background: rgba(0, 0, 0, 0.6) !important; border: 1.5px solid rgba(255,255,255,0.15) !important; border-radius: 14px !important; color: #ffffff !important; font-size: 16px !important; padding: 14px 16px !important; min-height: 52px !important; }
.stTextInput input:focus { border-color: #4CAF50 !important; box-shadow: 0 0 0 3px rgba(76,175,80,0.20) !important; }
.stTextInput input::placeholder { color: rgba(255,255,255,0.30) !important; }
.stTextInput label { display: none !important; }
.stButton > button { background: linear-gradient(135deg, #388e3c, #4caf50) !important; color: #fff !important; border: none !important; border-radius: 40px !important; font-weight: 700 !important; font-size: 14px !important; min-height: 44px !important; box-shadow: 0 2px 8px rgba(76,175,80,0.3) !important; transition: all 0.18s ease !important; }
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 16px rgba(76,175,80,0.45) !important; filter: brightness(1.05) !important; }
.login-card .stButton > button { font-size: 16px !important; min-height: 52px !important; box-shadow: 0 4px 18px rgba(76,175,80,0.35) !important; }
.stAlert { background: rgba(0,0,0,0.7) !important; border-radius: 12px !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# UI
st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
st.markdown('<div class="login-logo">📚</div>', unsafe_allow_html=True)
st.markdown('<div class="login-title">Rekxare Dami</div>', unsafe_allow_html=True)
st.markdown(f'<div class="login-sub">{t("login_sub")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="login-badge">{t("login_badge")}</div>', unsafe_allow_html=True)

# Language buttons (green)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("بادينى", key="lang_badini", use_container_width=True):
        st.session_state.lang = "badini"
        st.rerun()
with col2:
    if st.button("English", key="lang_en", use_container_width=True):
        st.session_state.lang = "english"
        st.rerun()
with col3:
    if st.button("العربية", key="lang_ar", use_container_width=True):
        st.session_state.lang = "arabic"
        st.rerun()

st.markdown('<div class="login-card">', unsafe_allow_html=True)
st.markdown(f'<span class="login-label">{t("login_email_label")}</span>', unsafe_allow_html=True)
email = st.text_input("Email", placeholder=t("login_placeholder"), label_visibility="collapsed")

if st.button(t("login_btn"), use_container_width=True):
    if email and "@" in email and "." in email:
        st.session_state.user_email = email
        st.session_state.logged_in = True
        st.session_state.data_key = email.split("@")[0]
        # Redirect to the main app (Home.py)
        st.switch_page("pages/Home.py")
    else:
        st.error(t("login_error_email"))

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(f'<div class="login-footer">{t("login_footer")}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
