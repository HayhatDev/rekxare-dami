import streamlit as st
import time
import random
from datetime import datetime, date, timedelta
import json
import os
import streamlit.components.v1 as components
import hashlib
import pandas as pd


# ══════════════════════════════════════════════════════════
#  TRANSLATIONS  (load before set_page_config)
# ══════════════════════════════════════════════════════════
with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

# ── Early session-state defaults (needed before login gate)
if "lang" not in st.session_state:
    st.session_state.lang = "badini"
if "data_key" not in st.session_state:
    st.session_state.data_key = "default"
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def get_schedule_file():
    if st.user.is_logged_in:
        email = st.user.email
    else:
        email = st.session_state.get("user_email", "default")
    user_hash = hashlib.md5(email.encode()).hexdigest()[:8]
    return f"schedule_data_{user_hash}.json"
    
# ══════════════════════════════════════════════════════════
#  PAGE CONFIG  ← must be the FIRST Streamlit call
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Rekxare Dami",
    page_icon="📚",
    initial_sidebar_state="collapsed",
    layout="centered",
)

# ══════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════
SCHEDULE_FILE = "schedule_data.json"

# ══════════════════════════════════════════════════════════
#  DATA HELPERS
# ══════════════════════════════════════════════════════════
def get_schedule_data():
    filename = get_schedule_file() 
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("schedule", {})
        except Exception as e:
            print(f"Error loading schedule: {e}")
    return {}
    
    
def get_data_file():
    if st.user.is_logged_in:
        email = st.user.email
    else:
        email = st.session_state.get("user_email", "default")
    key = hashlib.md5(email.encode()).hexdigest()[:8]
    return f"study_data_{key}.json"

def load_data():
    DATA_FILE = get_data_file()
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        st.session_state.total_study_seconds = data.get("total_seconds", 0)
        st.session_state.completed_sessions  = data.get("sessions", 0)
        st.session_state.last_subject        = data.get("last_subject", "—")
        st.session_state.study_history       = data.get("history", [])
        st.session_state.dark_mode           = data.get("dark_mode", True)
        st.session_state.streak              = data.get("streak", 0)
        st.session_state.last_study_date     = data.get("last_study_date", "")
        st.session_state.daily_seconds       = data.get("daily_seconds", 0)
        st.session_state.daily_goal_seconds  = data.get("daily_goal_seconds", 7200)
        st.session_state.lang                = data.get("lang", "badini")
        st.session_state.student_name        = data.get("student_name", "")
        st.session_state.user_email = data.get("user_email", "")
        if st.session_state.user_email:
            st.session_state.logged_in = True
            st.session_state.data_key = st.session_state.user_email.split("@")[0]


def save_data():
    DATA_FILE = get_data_file()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "total_seconds":      st.session_state.total_study_seconds,
            "sessions":           st.session_state.completed_sessions,
            "last_subject":       st.session_state.last_subject,
            "history":            st.session_state.study_history,
            "dark_mode":          st.session_state.dark_mode,
            "streak":             st.session_state.streak,
            "last_study_date":    st.session_state.last_study_date,
            "daily_seconds":      st.session_state.daily_seconds,
            "daily_goal_seconds": st.session_state.daily_goal_seconds,
            "lang":               st.session_state.lang,
            "student_name":       st.session_state.get("student_name", ""),
            "user_email":         st.session_state.get("user_email", ""),
        }, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════
#  TRANSLATION HELPER  (available before and after login)
# ══════════════════════════════════════════════════════════
def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text


if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# ========== LOAD TRANSLATIONS & DEFINE t() ==========
with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

if "lang" not in st.session_state:
    st.session_state.lang = "badini"

def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

# ========== LOGIN GATE (Google OAuth) ==========
if not st.user.is_logged_in:
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    *, *::before, *::after {{ box-sizing: border-box; }}
    
    html, body, .stApp, [data-testid="stAppViewContainer"],
    section[data-testid="stMain"], .main, .main .block-container {{
        background: linear-gradient(135deg, #0f0c29, #1a1a2e, #16213e) !important;
        font-family: 'Inter', system-ui, sans-serif !important;
    }}
    
    header[data-testid="stHeader"], #MainMenu, footer,
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {{
        display: none !important;
    }}
    
    .main .block-container {{
        padding-top: max(20px, calc(50vh - 260px)) !important;
        padding-bottom: 40px !important;
        padding-left: 20px !important;
        padding-right: 20px !important;
        max-width: 480px !important;
    }}
    
    .login-wrap {{
        width: 100%;
        display: flex; flex-direction: column; align-items: center;
    }}
    
    .login-logo {{
        font-size: 72px; line-height: 1; margin-bottom: 12px;
        filter: drop-shadow(0 4px 16px rgba(76,175,80,0.4));
        animation: float 3s ease-in-out infinite;
    }}
    @keyframes float {{
        0%,100% {{ transform: translateY(0); }}
        50%      {{ transform: translateY(-8px); }}
    }}
    
    .login-title {{
        font-size: 32px; font-weight: 900; letter-spacing: -0.8px;
        color: #ffffff; text-align: center; margin-bottom: 4px;
    }}
    
    .login-sub {{
        font-size: 14px; color: rgba(255,255,255,0.55);
        text-align: center; margin-bottom: 24px; font-weight: 500;
    }}
    
    .login-badge {{
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(76,175,80,0.15); border: 1px solid rgba(76,175,80,0.25);
        color: #81c784; border-radius: 20px; padding: 5px 14px;
        font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
        margin-bottom: 24px;
    }}
    
    .login-card {{
        background: rgba(0, 0, 0, 0.5);
        border: 1.5px solid rgba(255,255,255,0.13);
        border-radius: 28px;
        padding: 32px 28px 28px;
        width: 100%;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 40px rgba(0,0,0,0.40);
    }}
    
    /* Language buttons - green gradient + hover effect */
    .stButton > button {{
        background: linear-gradient(135deg, #388e3c, #4caf50) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 40px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        min-height: 44px !important;
        box-shadow: 0 2px 8px rgba(76,175,80,0.3) !important;
        transition: all 0.18s ease !important;
        width: 100% !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(76,175,80,0.45) !important;
        filter: brightness(1.05) !important;
    }}
    
    /* The Google sign-in button (inside the card) gets the same style + bigger */
    .login-card .stButton > button {{
        font-size: 16px !important;
        min-height: 52px !important;
        box-shadow: 0 4px 18px rgba(76,175,80,0.35) !important;
    }}
    
    .divider {{
        display: flex; align-items: center; gap: 12px;
        margin: 24px 0 20px;
        color: rgba(255,255,255,0.35);
        font-size: 12px; font-weight: 600;
    }}
    .divider::before, .divider::after {{
        content: ""; flex: 1; height: 1px;
        background: rgba(255,255,255,0.15);
    }}
    
    .login-footer {{
        font-size: 12px; color: rgba(255,255,255,0.30);
        text-align: center; margin-top: 24px;
    }}
    </style>
    
    <div class="login-wrap">
        <div class="login-logo">📚</div>
        <div class="login-title">Rekxare Dami</div>
        <div class="login-sub">{t('login_sub')}</div>
        <div class="login-badge">{t('login_badge')}</div>
        <div class="login-card">
    """, unsafe_allow_html=True)
    
    # Language switcher (three green buttons side by side)
    st.markdown('<div style="display: flex; gap: 12px; margin-bottom: 28px;">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("بادينى", key="lang_badini_login", use_container_width=True):
            st.session_state.lang = "badini"
            st.rerun()
    with col2:
        if st.button("English", key="lang_en_login", use_container_width=True):
            st.session_state.lang = "english"
            st.rerun()
    with col3:
        if st.button("العربية", key="lang_ar_login", use_container_width=True):
            st.session_state.lang = "arabic"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Divider (translated via your JSON)
    st.markdown(f'<div class="divider">{t("login_divider")}</div>', unsafe_allow_html=True)
    
    # Google login button (centered)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("🔐 Google", on_click=st.login, use_container_width=True)
    
    # Footer
    st.markdown(f'<div class="login-footer">{t("login_footer")}</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()


# ========== AFTER LOGIN: SET USER SESSION ==========
if st.user.is_logged_in and "user_email" not in st.session_state:
    st.session_state.user_email = st.user.email
    st.session_state.data_key = hashlib.md5(st.user.email.encode()).hexdigest()[:8]
    st.session_state.logged_in = True
    load_data()   # load their existing data
    st.rerun()
# ══════════════════════════════════════════════════════════
#  POST-LOGIN SETUP
# ══════════════════════════════════════════════════════════
st.session_state.data_key = st.session_state.user_email.split("@")[0]

def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS.get("badini", {})).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text


SUBJECT_COLOR_LIST = [
    "#2196F3", "#9C27B0", "#FF5722", "#00BCD4",
    "#4CAF50", "#795548", "#FF9800", "#607D8B", "#FFC107",
]


def subject_color(label: str) -> str:
    try:
        idx = subjects_list.index(label)
        return SUBJECT_COLOR_LIST[idx]
    except (ValueError, IndexError):
        return "#4CAF50"


def get_greeting():
    h = datetime.now().hour
    if 5 <= h < 12:
        return t("greeting_morning"), t("greeting_morning_en")
    elif 12 <= h < 17:
        return t("greeting_afternoon"), t("greeting_afternoon_en")
    elif 17 <= h < 21:
        return t("greeting_evening"), t("greeting_evening_en")
    else:
        return t("greeting_night"), t("greeting_night_en")


def load_today_schedule():
    today_map = {6: "sun", 0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat"}
    today_key = today_map[datetime.now().weekday()]
    filename = get_schedule_file()
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return today_key, data.get("schedule", {}).get(today_key, [])
        except Exception:
            return today_key, []
    return today_key, []

def total_day_minutes(day_entries):
    total = 0
    for e in day_entries:
        if not e.get("task", "").strip():
            continue
        try:
            s   = datetime.strptime(e.get("start", "00:00"), "%H:%M")
            end = datetime.strptime(e.get("end", "00:00"), "%H:%M")
            diff = int((end - s).total_seconds() // 60)
            if diff > 0:
                total += diff
        except Exception:
            pass
    return total
    
# ── Defaults
DEFAULTS = {
    "total_study_seconds": 0, "completed_sessions": 0,
    "last_subject": "—", "study_history": [], "dark_mode": True,
    "streak": 0, "last_study_date": "", "daily_seconds": 0,
    "daily_goal_seconds": 7200, "timer_running": False,
    "end_time": None, "total_seconds": 0, "paused": False,
    "remaining_at_pause": 0, "student_name": "",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

if "data_loaded" not in st.session_state:
    load_data()
    st.session_state.data_loaded = True

if "confirm_clear" not in st.session_state:
    st.session_state.confirm_clear = False

if "quote_idx" not in st.session_state:
    st.session_state.quote_idx = random.randint(0, 99)

# ── Daily reset
today_str = date.today().isoformat()
if (st.session_state.last_study_date
        and st.session_state.last_study_date != today_str
        and st.session_state.daily_seconds > 0):
    st.session_state.daily_seconds = 0
    save_data()

is_dark        = st.session_state.dark_mode
total_minutes  = st.session_state.total_study_seconds // 60
hours_total    = total_minutes // 60
mins_total     = total_minutes % 60
daily_pct      = min(100, int(st.session_state.daily_seconds /
                               max(1, st.session_state.daily_goal_seconds) * 100))
daily_done_min = st.session_state.daily_seconds // 60
daily_goal_min = st.session_state.daily_goal_seconds // 60
today_h        = st.session_state.daily_seconds // 3600
today_m        = (st.session_state.daily_seconds % 3600) // 60

_days_map = {"badini": "رۆژ", "english": "days", "arabic": "أيام"}
days_lbl  = _days_map.get(st.session_state.lang, "رۆژ")

# ══════════════════════════════════════════════════════════
#  COLOUR TOKENS
# ══════════════════════════════════════════════════════════
if is_dark:
    APP_BG         = "#1a1a2e"
    SB_BG          = "#16213e"
    CARD_BG        = "rgba(255,255,255,0.06)"
    CARD_BORDER    = "rgba(255,255,255,0.09)"
    TEXT_PRIMARY   = "#e2e2e2"
    TEXT_MUTED     = "#8a8fa8"
    SECTION_LBL    = "#555c72"
    TAG_BG         = "rgba(76,175,80,0.18)"
    TAG_COLOR      = "#81c784"
    ACTIVITY_BG    = "rgba(255,255,255,0.04)"
    SETTINGS_BG    = "rgba(255,255,255,0.04)"
    SETTINGS_BDR   = "rgba(255,255,255,0.08)"
    INPUT_BG       = "#252542"
    BTN_BG         = "#252542"
    BTN_COLOR      = "#e2e2e2"
    BTN_BORDER     = "#3a3a5c"
    TIMER_TRACK    = "#252542"
    TIMER_TEXT     = "#ffffff"
    TIMER_CARD_BG  = "rgba(255,255,255,0.04)"
    TIMER_CARD_BDR = "rgba(255,255,255,0.09)"
    PROG_TRACK     = "rgba(255,255,255,0.10)"
    GREET_BG       = "rgba(255,255,255,0.05)"
    GREET_BDR      = "rgba(255,255,255,0.09)"
    DIVIDER        = "rgba(255,255,255,0.08)"
    LANG_ACTIVE_BG = "rgba(76,175,80,0.25)"
    LANG_ACTIVE_C  = "#81c784"
    LANG_IDLE_BG   = "rgba(255,255,255,0.06)"
    LANG_IDLE_C    = "#8a8fa8"
    TODAY_CARD_BG  = "rgba(76,175,80,0.10)"
    TODAY_CARD_BDR = "rgba(76,175,80,0.20)"
    WARN_BG        = "rgba(255,152,0,0.12)"
    WARN_BDR       = "rgba(255,152,0,0.25)"
    WARN_COLOR     = "#ffb74d"
    DANGER_BG      = "rgba(239,83,80,0.12)"
    DANGER_BDR     = "rgba(239,83,80,0.25)"
    DANGER_COLOR   = "#ef9a9a"
    SCHED_BG       = "rgba(255,255,255,0.04)"
    SCHED_BDR      = "rgba(255,255,255,0.10)"
    SCHED_DONE_BG  = "rgba(76,175,80,0.10)"
    SCHED_TODO_BG  = "rgba(255,255,255,0.03)"
    QUOTE_BG       = "rgba(255,255,255,0.04)"
    QUOTE_BDR      = "rgba(255,255,255,0.08)"
    QUOTE_COLOR    = "#c5cae9"
    SETUP_BG       = "rgba(255,255,255,0.04)"
    SETUP_BDR      = "rgba(255,255,255,0.09)"
    GOAL_WIN_BG    = "rgba(76,175,80,0.14)"
    GOAL_WIN_BDR   = "rgba(76,175,80,0.30)"
    PRESET_BG      = "rgba(255,255,255,0.06)"
    PRESET_BDR     = "rgba(255,255,255,0.10)"
else:
    APP_BG         = "#e8edf5"
    SB_BG          = "#f4f7fb"
    CARD_BG        = "#ffffff"
    CARD_BORDER    = "#dde3ed"
    TEXT_PRIMARY   = "#1a1a2e"
    TEXT_MUTED     = "#6b7280"
    SECTION_LBL    = "#9ca3af"
    TAG_BG         = "rgba(76,175,80,0.10)"
    TAG_COLOR      = "#2e7d32"
    ACTIVITY_BG    = "#dde5f0"
    SETTINGS_BG    = "#dde5f0"
    SETTINGS_BDR   = "#c8d4e8"
    INPUT_BG       = "#ffffff"
    BTN_BG         = "#dde5f0"
    BTN_COLOR      = "#1a1a2e"
    BTN_BORDER     = "#c0cce0"
    TIMER_TRACK    = "#dde3ed"
    TIMER_TEXT     = "#1a1a2e"
    TIMER_CARD_BG  = "#ffffff"
    TIMER_CARD_BDR = "#dde3ed"
    PROG_TRACK     = "#dde3ed"
    GREET_BG       = "#ffffff"
    GREET_BDR      = "#dde3ed"
    DIVIDER        = "#dde3ed"
    LANG_ACTIVE_BG = "rgba(76,175,80,0.12)"
    LANG_ACTIVE_C  = "#2e7d32"
    LANG_IDLE_BG   = "#edf0f7"
    LANG_IDLE_C    = "#6b7280"
    TODAY_CARD_BG  = "rgba(76,175,80,0.07)"
    TODAY_CARD_BDR = "rgba(76,175,80,0.18)"
    WARN_BG        = "#fff8e1"
    WARN_BDR       = "#ffe082"
    WARN_COLOR     = "#e65100"
    DANGER_BG      = "#ffebee"
    DANGER_BDR     = "#ef9a9a"
    DANGER_COLOR   = "#c62828"
    SCHED_BG       = "#ffffff"
    SCHED_BDR      = "#dde3ed"
    SCHED_DONE_BG  = "rgba(76,175,80,0.07)"
    SCHED_TODO_BG  = "#f9fafb"
    QUOTE_BG       = "#ffffff"
    QUOTE_BDR      = "#dde3ed"
    QUOTE_COLOR    = "#3949ab"
    SETUP_BG       = "#ffffff"
    SETUP_BDR      = "#dde3ed"
    GOAL_WIN_BG    = "rgba(76,175,80,0.08)"
    GOAL_WIN_BDR   = "rgba(76,175,80,0.22)"
    PRESET_BG      = "#edf0f7"
    PRESET_BDR     = "#c0cce0"

# ══════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

/* ── Base ── */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"],
section[data-testid="stMain"],
.main .block-container {{
    background-color: {APP_BG} !important;
    font-family: 'Inter', system-ui, sans-serif !important;
}}
[data-testid="stSidebar"] {{ background-color: {SB_BG} !important; }}
.stApp *, [data-testid="stSidebar"] * {{ color: {TEXT_PRIMARY} !important; }}
h1, h2, h3 {{ font-weight: 800 !important; letter-spacing: -0.3px; }}

/* ── MOBILE: prevent double-tap zoom ── */
button, input, select, textarea, label {{
    touch-action: manipulation !important;
}}

/* ── MOBILE: safe-area insets for notched phones ── */
.main .block-container {{
    padding-left:   max(1rem, env(safe-area-inset-left))   !important;
    padding-right:  max(1rem, env(safe-area-inset-right))  !important;
    padding-bottom: max(1rem, env(safe-area-inset-bottom)) !important;
}}

/* ── Text / time inputs (16px → no iOS auto-zoom) ── */
.stTextInput input,
.stTimeInput input {{
    background-color: {INPUT_BG} !important;
    border: 1.5px solid {CARD_BORDER} !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    padding: 10px 14px !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    min-height: 48px !important;
}}

/* ── Selectbox — kept separate so height:auto prevents text clipping ── */
.stSelectbox [data-baseweb="select"] {{
    background-color: {INPUT_BG} !important;
    border: 1.5px solid {CARD_BORDER} !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    overflow: visible !important;
}}
/* The inner clickable row — height:auto lets wrapped text breathe */
.stSelectbox [data-baseweb="select"] > div:first-child {{
    height: auto !important;
    min-height: 48px !important;
    padding: 10px 44px 10px 14px !important;
    overflow: visible !important;
    background: transparent !important;
    border: none !important;
    border-radius: 12px !important;
    line-height: 1.4 !important;
    display: flex !important;
    align-items: center !important;
}}
.stTextInput input:focus {{
    border-color: #4CAF50 !important;
    box-shadow: 0 0 0 3px rgba(76,175,80,0.15) !important;
    outline: none !important;
}}

/* ── Radio language switcher ── */
[data-testid="stRadio"] > div {{ gap: 8px !important; flex-wrap: wrap !important; }}
[data-testid="stRadio"] label {{
    background: {LANG_IDLE_BG} !important;
    color: {LANG_IDLE_C} !important;
    border-radius: 20px !important;
    padding: 8px 18px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    border: 1.5px solid {CARD_BORDER} !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    min-height: 44px !important;
    display: flex !important; align-items: center !important;
}}
[data-testid="stRadio"] label:has(input:checked) {{
    background: {LANG_ACTIVE_BG} !important;
    color: {LANG_ACTIVE_C} !important;
    border-color: {LANG_ACTIVE_C} !important;
}}
[data-testid="stRadio"] input[type="radio"] {{ display: none !important; }}

/* ── Buttons (48px min touch target per Apple HIG) ── */
.stButton > button {{
    background-color: {BTN_BG}    !important;
    color:            {BTN_COLOR} !important;
    border:           1.5px solid {BTN_BORDER} !important;
    border-radius:    12px !important;
    font-weight:      600  !important;
    font-size:        15px !important;
    font-family:      'Inter', system-ui, sans-serif !important;
    padding:          12px 16px !important;
    min-height:       48px !important;
    transition:       all 0.18s ease !important;
    width:            100% !important;
    -webkit-tap-highlight-color: transparent !important;
    letter-spacing:   0.1px !important;
}}
.stButton > button:hover:not(:disabled) {{
    filter: brightness(1.07) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.12) !important;
}}
.stButton > button:active:not(:disabled) {{
    transform: translateY(0px) !important;
    box-shadow: none !important;
}}
.stButton > button:disabled {{ opacity: 0.35 !important; cursor: not-allowed !important; }}

/* ── Timer control buttons (green start / orange pause) ── */
.tcb-anchor {{ display: none !important; }}
.element-container:has(.tcb-anchor) + div
    [data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton button:not(:disabled) {{
    background: linear-gradient(135deg, #43a047, #66bb6a) !important;
    color: #fff !important; border-color: #388e3c !important;
    box-shadow: 0 3px 12px rgba(67,160,71,0.35) !important;
}}
.element-container:has(.tcb-anchor) + div
    [data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton button:not(:disabled) {{
    background: linear-gradient(135deg, #ef6c00, #ffa726) !important;
    color: #fff !important; border-color: #e65100 !important;
    box-shadow: 0 3px 12px rgba(239,108,0,0.30) !important;
}}
/* Style download buttons to match default .stButton */
.stDownloadButton button {{
    background-color: {BTN_BG} !important;
    color: {BTN_COLOR} !important;
    border: 1.5px solid {BTN_BORDER} !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 12px 16px !important;
    min-height: 48px !important;
    transition: all 0.18s ease !important;
    width: 100% !important;
}}
.stDownloadButton button:hover {{
    filter: brightness(1.07) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.12) !important;
}}
.stDownloadButton button:active {{
    transform: translateY(0px) !important;
    box-shadow: none !important;
}}
/* ── Preset buttons ── */
.preset-anchor {{ display: none !important; }}
.element-container:has(.preset-anchor) + div
    [data-testid="stHorizontalBlock"] .stButton button {{
    background: {PRESET_BG} !important;
    color: {TEXT_PRIMARY} !important;
    border: 1.5px solid {PRESET_BDR} !important;
    border-radius: 20px !important;
    font-size: 13px !important;
    padding: 8px 4px !important;
    font-weight: 700 !important;
    min-height: 44px !important;
}}
.element-container:has(.preset-anchor) + div
    [data-testid="stHorizontalBlock"] .stButton button:hover:not(:disabled) {{
    border-color: #4CAF50 !important;
    color: #4CAF50 !important;
    background: {TAG_BG} !important;
    box-shadow: none !important;
}}

/* ── Cards ── */
.timer-card {{
    background: {TIMER_CARD_BG}; border: 1.5px solid {TIMER_CARD_BDR};
    border-radius: 24px; padding: 28px 16px 20px;
    margin: 8px 0 16px; text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}}
.timer-card svg {{
    width: min(260px, 80vw) !important;
    height: min(260px, 80vw) !important;
}}
.setup-card {{
    background: {SETUP_BG}; border: 1.5px solid {SETUP_BDR};
    border-radius: 18px; padding: 18px 20px; margin-bottom: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}}
.quote-card {{
    background: {QUOTE_BG}; border: 1.5px solid {QUOTE_BDR};
    border-radius: 18px; padding: 20px 22px;
    margin: 4px 0 14px; position: relative;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}}
.quote-mark {{
    font-size: 48px; line-height: 1; opacity: 0.12;
    position: absolute; top: 10px; left: 16px;
    font-family: Georgia, serif;
}}
.quote-text {{
    font-size: 14px; font-weight: 500; font-style: italic;
    color: {QUOTE_COLOR} !important; line-height: 1.65;
    padding-left: 26px; padding-right: 8px;
}}
.paused-banner {{
    background: {WARN_BG}; border: 1.5px solid {WARN_BDR};
    border-radius: 12px; padding: 14px 18px; text-align: center;
    font-size: 14px; font-weight: 700; color: {WARN_COLOR} !important;
    margin-bottom: 8px;
}}
.goal-win-banner {{
    background: {GOAL_WIN_BG}; border: 1.5px solid {GOAL_WIN_BDR};
    border-radius: 16px; padding: 16px 20px;
    display: flex; align-items: center; gap: 16px;
    margin-bottom: 16px;
    box-shadow: 0 3px 16px rgba(76,175,80,0.14);
}}
.goal-win-icon {{ font-size: 36px; line-height: 1; flex-shrink: 0; }}
.goal-win-text {{ font-size: 14px; font-weight: 800; color: #4CAF50 !important; }}
.goal-win-sub  {{ font-size: 12px; color: {TEXT_MUTED} !important; margin-top: 3px; }}
.subject-color-dot {{
    display: inline-block; width: 10px; height: 10px;
    border-radius: 50%; margin-right: 7px; flex-shrink: 0; vertical-align: middle;
}}
.subject-pill {{
    display: inline-flex; align-items: center;
    background: {TAG_BG}; color: {TAG_COLOR} !important;
    border-radius: 20px; padding: 6px 14px;
    font-size: 13px; font-weight: 700; margin-bottom: 12px;
}}
.section-hdr {{
    display: flex; align-items: center; gap: 8px;
    font-size: 11px; font-weight: 800; letter-spacing: 1.2px;
    text-transform: uppercase; color: {SECTION_LBL} !important;
    margin: 22px 0 12px;
}}
.section-hdr span {{ color: {SECTION_LBL} !important; }}
.section-line {{ flex: 1; height: 1px; background: {DIVIDER}; }}

/* ── Sidebar ── */
.sb-lbl {{
    font-size: 10px; font-weight: 800; letter-spacing: 1.4px;
    text-transform: uppercase; color: {SECTION_LBL} !important;
    margin: 20px 0 8px 2px; display: block;
}}
.stat-row  {{ display: flex; gap: 10px; margin-bottom: 10px; }}
.stat-card {{
    flex: 1; background: {CARD_BG}; border: 1.5px solid {CARD_BORDER};
    border-radius: 16px; padding: 14px 10px; text-align: center;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05);
    transition: transform 0.15s ease;
}}
.stat-card:active {{ transform: scale(0.97); }}
.stat-icon {{ font-size: 22px; margin-bottom: 6px; line-height: 1; }}
.stat-val  {{ font-size: 17px; font-weight: 800; line-height: 1.2; }}
.stat-lbl  {{ font-size: 10px; color: {TEXT_MUTED} !important; margin-top: 4px; font-weight: 600; }}
.today-stat {{
    background: {TODAY_CARD_BG}; border: 1.5px solid {TODAY_CARD_BDR};
    border-radius: 14px; padding: 12px 16px; margin-bottom: 8px;
    display: flex; align-items: center; justify-content: space-between;
}}
.today-stat-label {{ font-size: 12px; font-weight: 700; }}
.today-stat-val   {{ font-size: 16px; font-weight: 800; color: #4CAF50 !important; }}
.streak-card {{
    background: {CARD_BG}; border: 1.5px solid {CARD_BORDER};
    border-radius: 16px; padding: 14px 16px;
    display: flex; align-items: center; gap: 14px; margin-bottom: 8px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05);
}}
.streak-num {{ font-size: 26px; font-weight: 900; color: #FF9800 !important; line-height: 1; }}
.streak-sub {{ font-size: 11px; color: {TEXT_MUTED} !important; margin-top: 4px; }}
.goal-wrap {{
    background: {CARD_BG}; border: 1.5px solid {CARD_BORDER};
    border-radius: 16px; padding: 14px 16px; margin-bottom: 8px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05);
}}
.goal-header {{ display: flex; justify-content: space-between; align-items: center;
                font-size: 12px; color: {TEXT_MUTED} !important; margin-bottom: 10px; }}
.goal-title  {{ font-weight: 700; color: {TEXT_PRIMARY} !important; font-size: 13px; }}
.goal-track  {{ background: {PROG_TRACK}; border-radius: 99px; height: 8px; overflow: hidden; }}
.goal-fill   {{ height: 8px; border-radius: 99px; transition: width 0.6s ease; }}
.subject-tag {{ display: inline-block; background: {TAG_BG}; color: {TAG_COLOR} !important;
                border-radius: 20px; padding: 6px 16px; font-size: 13px; font-weight: 700; }}
.act-list  {{ background: {ACTIVITY_BG}; border-radius: 14px; padding: 4px; overflow: hidden; }}
.act-item  {{ display: flex; align-items: flex-start; gap: 10px; padding: 8px 12px;
              border-radius: 10px; font-size: 12px; line-height: 1.4; }}
.act-dot   {{ width:8px; height:8px; border-radius:50%; background:#4CAF50;
              flex-shrink:0; margin-top:3px; }}
.act-empty {{ font-size:12px; color:{TEXT_MUTED} !important; padding:14px; text-align:center; }}
.settings-box {{ background: {SETTINGS_BG}; border: 1.5px solid {SETTINGS_BDR};
                 border-radius: 16px; padding: 16px; }}
.danger-box {{
    background: {DANGER_BG}; border: 1.5px solid {DANGER_BDR};
    border-radius: 12px; padding: 12px; margin-bottom: 8px;
    font-size: 12px; font-weight: 700; color: {DANGER_COLOR} !important; text-align: center;
}}
.greet-card {{
    background: {GREET_BG}; border: 1.5px solid {GREET_BDR};
    border-radius: 20px; padding: 20px 22px; margin-bottom: 16px;
    display: flex; align-items: center; gap: 16px;
    box-shadow: 0 3px 18px rgba(0,0,0,0.07);
}}
.greet-emoji {{ font-size: 48px; line-height: 1; flex-shrink: 0; }}
.greet-name  {{ font-size: 20px; font-weight: 900; line-height: 1.2; letter-spacing: -0.3px; }}
.greet-sub   {{ font-size: 13px; color: {TEXT_MUTED} !important; margin-top: 4px; font-weight: 500; }}
.greet-time  {{ font-size: 11px; color: {TEXT_MUTED} !important; margin-top: 4px; opacity: 0.7; }}
.sched-card {{
    background: {SCHED_BG}; border: 1.5px solid {SCHED_BDR};
    border-radius: 18px; padding: 16px 18px; margin-bottom: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}}
.sched-title {{
    font-size: 12px; font-weight: 700; letter-spacing: 0.6px;
    text-transform: uppercase; color: {TEXT_MUTED} !important;
    margin-bottom: 12px; display: flex; align-items: center; gap: 6px;
}}
.sched-item      {{ display: flex; align-items: center; gap: 10px; padding: 9px 10px;
                    border-radius: 10px; margin-bottom: 4px; font-size: 13px; }}
.sched-item-done {{ background: {SCHED_DONE_BG}; opacity: 0.65; }}
.sched-item-todo {{ background: {SCHED_TODO_BG}; }}
.sched-time      {{ font-size: 11px; font-weight: 700; color: {TEXT_MUTED} !important;
                    min-width: 72px; flex-shrink: 0; font-variant-numeric: tabular-nums; }}
.sched-task      {{ font-weight: 500; flex: 1; min-width: 0;
                    overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.sched-task-done {{ text-decoration: line-through; color: {TEXT_MUTED} !important; }}
.sched-check     {{ flex-shrink: 0; font-size: 14px; }}
.sched-prog-wrap {{ margin-top: 12px; background: {PROG_TRACK};
                    border-radius: 99px; height: 5px; overflow: hidden; }}
.sched-prog-fill {{ height: 5px; border-radius: 99px; }}

/* ── Slider ── */
[data-testid="stSlider"] > div > div {{ touch-action: none !important; }}

hr {{ border-color: {DIVIDER} !important; margin: 18px 0 !important; }}

/* ── Toasts / alerts ── */
.stAlert {{ border-radius: 14px !important; font-size: 14px !important; }}

{"""/* ── Arabic RTL ── */
.greet-card, .greet-name, .greet-sub, .greet-time,
.timer-card, .timer-subject, .stat-card, .stat-card-label,
.activity-card, .goal-banner, .xp-card, .xp-label, .xp-bar-wrap,
.streak-card, .streak-label, .goal-section, .quote-card,
.sched-card, .sched-item, .no-sched { direction: rtl; text-align: right; }
""" if st.session_state.lang == "arabic" else ""}

/* ── Mobile ── */
@media (max-width: 640px) {{
    .greet-card  {{ padding: 14px 16px; gap: 12px; border-radius: 16px; }}
    .greet-emoji {{ font-size: 36px; }}
    .greet-name  {{ font-size: 18px; }}
    .greet-sub   {{ font-size: 12px; }}
    .greet-time  {{ display: none; }}
    .stat-card   {{ padding: 12px 8px; border-radius: 14px; }}
    .stat-val    {{ font-size: 15px; }}
    .stat-icon   {{ font-size: 18px; }}
    .timer-card  {{ padding: 16px 8px 14px; border-radius: 20px; }}
    .stButton > button {{ font-size: 14px !important; padding: 11px 10px !important; }}
    .setup-card  {{ padding: 16px 14px; }}
    .quote-card  {{ padding: 16px 16px; }}
    .quote-text  {{ font-size: 13px; }}
    .goal-win-banner {{ padding: 14px 16px; gap: 12px; border-radius: 14px; }}
    .goal-win-icon   {{ font-size: 28px; }}
    .sched-time  {{ min-width: 64px; font-size: 10px; }}
    .sched-item  {{ padding: 8px 8px; font-size: 12px; }}
    .section-hdr {{ margin: 18px 0 10px; }}
}}

/* ── Very small phones ── */
@media (max-width: 380px) {{
    .greet-emoji {{ font-size: 28px; }}
    .greet-name  {{ font-size: 16px; }}
    .stat-val    {{ font-size: 13px; }}
    .stat-icon   {{ font-size: 16px; }}
    .stButton > button {{ font-size: 13px !important; padding: 10px 8px !important; }}
    .sched-time  {{ display: none; }}
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding:20px 4px 8px;">
        <div style="font-size:22px;font-weight:900;letter-spacing:-0.5px;">📚 Rekxare Dami</div>
        <div style="font-size:12px;color:{TEXT_MUTED};margin-top:3px;font-weight:500;">{t("app_title")}</div>
    </div>
    <div style="height:1px;background:{DIVIDER};margin:8px 0 4px;"></div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sb-lbl">زمان | Language</span>', unsafe_allow_html=True)
    lang = st.radio("", ["badini", "english", "arabic"],
                    index=["badini", "english", "arabic"].index(st.session_state.lang),
                    horizontal=True, label_visibility="collapsed")
    if lang != st.session_state.lang:
        st.session_state.lang = lang
        save_data()
        st.rerun()

    st.markdown(f'<span class="sb-lbl">{t("sidebar_title")}</span>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-icon">⏱️</div>
            <div class="stat-val">{hours_total}{t("hours_unit")} {mins_total}{t("minutes_unit")}</div>
            <div class="stat-lbl">{t("total_time")}</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-val">{st.session_state.completed_sessions}</div>
            <div class="stat-lbl">{t("sessions")}</div>
        </div>
    </div>
    <div class="today-stat">
        <span class="today-stat-label">📅 {t("today_goal")}</span>
        <span class="today-stat-val">{today_h}{t("hours_unit")} {today_m}{t("minutes_unit")}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<span class="sb-lbl">{t("streak_section")}</span>', unsafe_allow_html=True)
    sv   = st.session_state.streak
    smsg = (t("streak_start") if sv == 0 else t("streak_ready") if sv < 3
            else t("streak_keep") if sv < 7 else t("streak_champ"))
    st.markdown(f"""
    <div class="streak-card">
        <div style="font-size:32px;line-height:1;">🔥</div>
        <div>
            <div class="streak-num">{sv}
                <span style="font-size:14px;font-weight:500;color:{TEXT_MUTED};">{days_lbl}</span>
            </div>
            <div class="streak-sub">{smsg}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<span class="sb-lbl">{t("goal_section")}</span>', unsafe_allow_html=True)
    gc = "#2196F3" if daily_pct >= 100 else "#4CAF50"
    st.markdown(f"""
    <div class="goal-wrap">
        <div class="goal-header">
            <span class="goal-title">🎯 {t("today_goal")}</span>
            <span>{daily_done_min} / {daily_goal_min} {t("minutes_unit")} — {daily_pct}%</span>
        </div>
        <div class="goal-track">
            <div class="goal-fill" style="width:{daily_pct}%;background:{gc};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<span class="sb-lbl">{t("last_subject")}</span>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding:2px 0 8px;"><span class="subject-tag">📖 {st.session_state.last_subject}</span></div>',
                unsafe_allow_html=True)

    st.markdown(f'<span class="sb-lbl">{t("recent_activity")}</span>', unsafe_allow_html=True)
    hist = st.session_state.study_history[-4:][::-1]
    if hist:
        rows = "".join(f'<div class="act-item"><div class="act-dot"></div><span>{e}</span></div>' for e in hist)
        st.markdown(f'<div class="act-list">{rows}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="act-list"><div class="act-empty">{t("no_activity")}</div></div>',
                    unsafe_allow_html=True)

    st.markdown(f'<span class="sb-lbl">{t("settings")}</span>', unsafe_allow_html=True)
    st.markdown('<div class="settings-box">', unsafe_allow_html=True)
    goal_mins = st.slider(
        f'🎯 {t("today_goal")} ({t("minutes_unit")})',
        30, 480, st.session_state.daily_goal_seconds // 60, step=15
    )
    if goal_mins * 60 != st.session_state.daily_goal_seconds:
        st.session_state.daily_goal_seconds = goal_mins * 60
        save_data()
        st.rerun()
    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
    dc, tc = st.columns([3, 1])
    with dc:
        st.markdown(f'<div style="font-size:13px;padding-top:6px;font-weight:600;">{t("dark_mode")}</div>',
                    unsafe_allow_html=True)
    with tc:
        dark_btn = st.checkbox("", value=is_dark, label_visibility="collapsed", key="dark_mode_sb")
    if dark_btn != is_dark:
        st.session_state.dark_mode = dark_btn
        save_data()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)

    if not st.session_state.confirm_clear:
        if st.button(t("clear_stats"), use_container_width=True):
            st.session_state.confirm_clear = True
            st.rerun()
    else:
        st.markdown(f'<div class="danger-box">⚠️ {t("clear_stats")}?</div>', unsafe_allow_html=True)
        cc1, cc2 = st.columns(2)
        with cc1:
            if st.button("✓", use_container_width=True, key="confirm_yes"):
                for k, v in [("total_study_seconds", 0), ("completed_sessions", 0),
                             ("last_subject", "—"), ("study_history", []),
                             ("streak", 0), ("daily_seconds", 0), ("last_study_date", ""),
                             ("xp_points", 0), ("xp_level", 1)]:
                    st.session_state[k] = v
                st.session_state.confirm_clear = False
                save_data()
                st.rerun()
        with cc2:
            if st.button("✗", use_container_width=True, key="confirm_no"):
                st.session_state.confirm_clear = False
            st.rerun()
                
            
    st.markdown('<div style="height: 14px;"></div>', unsafe_allow_html=True) 
    if st.button("🚪 " + t("logout"), use_container_width=True):
        for key in ["user_email", "data_key", "logged_in"]:
            st.session_state.pop(key, None)
        st.logout()
        st.rerun()

    # ========== EXPORT DATA SECTION ==========
    st.markdown('<div style="height: 14px;"></div>', unsafe_allow_html=True)
    
    # Helper for JSON serialization
    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    # Prepare JSON data
    export_data = {
        "export_info": {
            "generated": datetime.now().isoformat(),
            "app_version": "Rekxare Dami 1.0",
            "user": st.session_state.get("user_email", "unknown")
        },
        "study_summary": {
            "total_time_minutes": st.session_state.total_study_seconds // 60,
            "completed_sessions": st.session_state.completed_sessions,
            "current_streak_days": st.session_state.streak,
            "daily_goal_minutes": st.session_state.daily_goal_seconds // 60,
            "today_study_minutes": st.session_state.daily_seconds // 60,
            "last_subject": st.session_state.last_subject
        },
        "preferences": {
            "dark_mode": st.session_state.dark_mode,
            "language": st.session_state.lang,
            "student_name": st.session_state.get("student_name", "")
        },
        "study_history": st.session_state.study_history,
        "weekly_schedule": {}
    }
    
    # Load schedule data
    try:
        schedule_file = get_schedule_file()
        if os.path.exists(schedule_file):
            with open(schedule_file, "r", encoding="utf-8") as f:
                schedule_data = json.load(f)
                export_data["weekly_schedule"] = schedule_data.get("schedule", {})
    except Exception as e:
        export_data["schedule_error"] = str(e)
    
    json_str = json.dumps(export_data, indent=2, ensure_ascii=False, default=json_serial)
    
    # Prepare CSV data
    csv_lines = ["timestamp,subject,minutes"]
    if st.session_state.study_history:
        for entry in st.session_state.study_history:
            parts = entry.split(" - ")
            time_part = parts[0] if len(parts) > 0 else ""
            rest = parts[1] if len(parts) > 1 else ""
            subject_part = rest.split(" (")[0] if "(" in rest else rest
            minutes_part = rest.split("(")[1].split(" ")[0] if "(" in rest else "0"
            csv_lines.append(f"{time_part},{subject_part},{minutes_part}")
    else:
        csv_lines.append("No history,,")
    csv_data = "\n".join(csv_lines)
    
    # Expander with translated title
    with st.expander(t("export_data"), expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📄 JSON",
                data=json_str,
                file_name=f"rekxare_export_{st.session_state.get('user_email', 'user').split('@')[0]}.json",
                mime="application/json",
                key="export_json_btn",
                use_container_width=True
            )
        with col2:
            st.download_button(
                label="📊 CSV",
                data=csv_data,
                file_name=f"study_history_{st.session_state.get('user_email', 'user').split('@')[0]}.csv",
                mime="text/csv",
                key="export_csv_btn",
                use_container_width=True
            )
# ══════════════════════════════════════════════════════════
#  MAIN PAGE
# ══════════════════════════════════════════════════════════

# ── Name input
_all_defaults = {
    TRANSLATIONS.get(lng, {}).get("default_name", "")
    for lng in ("badini", "english", "arabic")
}
_raw_name    = st.session_state.get("student_name", "")
_display_val = "" if _raw_name in _all_defaults else _raw_name

nav = st.text_input(
    t("enter_name"), value=_display_val,
    label_visibility="collapsed", placeholder=t("default_name"),
)
_effective_name = nav.strip() or t("default_name")
if nav != st.session_state.get("student_name", ""):
    st.session_state.student_name = nav
    save_data()

# ── Greeting card
kurd_greet, eng_greet = get_greeting()
h_now       = datetime.now().hour
greet_emoji = ("🌅" if 5 <= h_now < 12 else "☀️" if 12 <= h_now < 17
               else "🌆" if 17 <= h_now < 21 else "🌙")
now_str     = datetime.now().strftime("%A, %d %B  •  %H:%M")

st.markdown(f"""
<div class="greet-card">
    <div class="greet-emoji">{greet_emoji}</div>
    <div style="min-width:0;">
        <div class="greet-name">{kurd_greet}{t("greeting_comma")}{_effective_name}!</div>
        <div class="greet-sub">{eng_greet} — {t('welcome')} 📚</div>
        <div class="greet-time">{now_str}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Daily goal banner
if daily_pct >= 100:
    goal_win_msg = {
        "badini":  f"ئارمانجێن ئەڤرو تەواو بوون! {today_h}ک {today_m}خ خواندن.",
        "english": f"Daily goal reached! You studied {today_h}h {today_m}m today.",
        "arabic":  f"تم تحقيق هدف اليوم! درست {today_h}س {today_m}د اليوم.",
    }.get(st.session_state.lang, "Goal reached!")
    goal_win_sub = {
        "badini":  "زور باش تە کر! بەردەوام بە 🔥",
        "english": "Amazing work! Keep the momentum going 🔥",
        "arabic":  "عمل رائع! استمر في الزخم 🔥",
    }.get(st.session_state.lang, "Keep going! 🔥")
    st.markdown(f"""
    <div class="goal-win-banner">
        <div class="goal-win-icon">🏆</div>
        <div>
            <div class="goal-win-text">{goal_win_msg}</div>
            <div class="goal-win-sub">{goal_win_sub}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Today's schedule preview
_today_key, today_tasks = load_today_schedule()
DAYS_SHORT = {
    "sun": ("Sunday","☀️"), "mon": ("Monday","📖"), "tue": ("Tuesday","📖"),
    "wed": ("Wednesday","📖"), "thu": ("Thursday","📖"),
    "fri": ("Friday","🕌"), "sat": ("Saturday","🎉"),
}
_day_eng, _day_emoji = DAYS_SHORT.get(_today_key, ("Today","📅"))
today_tasks_named = [ti for ti in today_tasks if ti.get("task","").strip()]

if today_tasks_named:
    done_count  = sum(1 for ti in today_tasks_named if ti.get("done", False))
    total_count = len(today_tasks_named)
    pct_sched   = int((done_count / total_count) * 100) if total_count else 0
    prog_color  = "#2196F3" if done_count == total_count else "#4CAF50"
    sched_title_text = {
        "badini":  f"📅 خشتەیێ ئەڤروکە — {_day_emoji} {_day_eng}",
        "english": f"📅 Today's Schedule — {_day_emoji} {_day_eng}",
        "arabic":  f"📅 جدول اليوم — {_day_emoji} {_day_eng}",
    }.get(st.session_state.lang, f"📅 Today — {_day_eng}")

    html_content = '<div class="sched-card">'
    html_content += (
        f'<div class="sched-title">{sched_title_text}'
        f'<span style="margin-left:auto;font-size:11px;color:{TEXT_MUTED};font-weight:600;">'
        f'{done_count}/{total_count} — {pct_sched}%</span></div>'
    )
    for ti in today_tasks_named[:6]:
        done_cls  = "sched-item-done" if ti.get("done") else "sched-item-todo"
        task_cls  = "sched-task-done" if ti.get("done") else "sched-task"
        check_ico = "✅" if ti.get("done") else "⬜"
        html_content += (
            f'<div class="sched-item {done_cls}">'
            f'<span class="sched-time">{ti.get("start","")}–{ti.get("end","")}</span>'
            f'<span class="{task_cls}">{ti.get("task","")}</span>'
            f'<span class="sched-check">{check_ico}</span></div>'
        )
    if len(today_tasks_named) > 6:
        extra = len(today_tasks_named) - 6
        extra_lbl = {
            "badini": f"+{extra} زێدەکرن",
            "english": f"+{extra} more",
            "arabic": f"+{extra} أكثر",
        }.get(st.session_state.lang, f"+{extra} more")
        html_content += f'<div style="font-size:11px;color:{TEXT_MUTED};padding:6px 10px;font-weight:600;">{extra_lbl}</div>'
    html_content += (
        f'<div class="sched-prog-wrap">'
        f'<div class="sched-prog-fill" style="width:{pct_sched}%;background:{prog_color};"></div>'
        f'</div></div>'
    )
    st.markdown(html_content, unsafe_allow_html=True)
    

# ── Weekly Study Chart ──
st.markdown(f"""
<div class="sched-card">
    <div class="sched-title">📊 {t('weekly_chart')}</div>
""", unsafe_allow_html=True)

schedule_data = get_schedule_data()

if schedule_data:
    week_data = {}
    for day, tasks in schedule_data.items():
        minutes = total_day_minutes(tasks)
        week_data[day] = minutes
    
    if week_data and any(week_data.values()):
        df = pd.DataFrame(list(week_data.items()), columns=["Day", "Minutes"])
        day_order = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        df["Day"] = pd.Categorical(df["Day"], categories=day_order, ordered=True)
        df = df.sort_values("Day")
        
        st.bar_chart(df.set_index("Day"), height=220)
        
        total_minutes = sum(week_data.values())
        total_hours = total_minutes // 60
        total_mins = total_minutes % 60
        st.caption(f"📊 {total_hours}h {total_mins}m {t('total_this_week')}")
    else:
        st.caption(f"📭 {t('no_study_data')}")
else:
    st.caption(f"📭 {t('no_study_data')}")

st.markdown('</div>', unsafe_allow_html=True)

# ── Timer section header
timer_section_lbl = {
    "badini": "⏱ دەمژمێرێ خواندنێ",
    "english": "⏱ Study Timer",
    "arabic": "⏱ مؤقت الدراسة",
}.get(st.session_state.lang, "⏱ Study Timer")
st.markdown(f"""
<div class="section-hdr">
    <span>{timer_section_lbl}</span>
    <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

# ── Setup card
st.markdown('<div class="setup-card">', unsafe_allow_html=True)

subjects_list = t("subjects")
if not isinstance(subjects_list, list):
    subjects_list = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get("subjects", [])

ders      = st.selectbox(t("select_subject"), subjects_list)
arc_color = subject_color(ders)
subj_name = ders.split(" ", 1)[1] if " " in ders else ders
st.markdown(
    f'<div class="subject-pill">'
    f'<span class="subject-color-dot" style="background:{arc_color};"></span>'
    f'{subj_name}</div>',
    unsafe_allow_html=True,
)

duration_lbl = {
    "badini": "⏱ دەمێ خواندنێ",
    "english": "⏱ Duration",
    "arabic": "⏱ المدة",
}.get(st.session_state.lang, "⏱ Duration")
st.markdown(
    f'<div style="font-size:12px;font-weight:700;color:{TEXT_MUTED};margin-bottom:6px;">'
    f'{duration_lbl}</div>',
    unsafe_allow_html=True,
)

SLIDER_KEY = "duration_slider_v2"
if SLIDER_KEY not in st.session_state:
    st.session_state[SLIDER_KEY] = 25

st.markdown('<div class="preset-anchor"></div>', unsafe_allow_html=True)
p1, p2, p3, p4 = st.columns(4)
with p1:
    if st.button("🍅 25m", key="p25", use_container_width=True, help="Pomodoro"):
        st.session_state[SLIDER_KEY] = 25; st.rerun()
with p2:
    if st.button("⚡ 45m", key="p45", use_container_width=True, help="Deep work"):
        st.session_state[SLIDER_KEY] = 45; st.rerun()
with p3:
    if st.button("🎯 60m", key="p60", use_container_width=True, help="Focus block"):
        st.session_state[SLIDER_KEY] = 60; st.rerun()
with p4:
    if st.button("🔥 90m", key="p90", use_container_width=True, help="Power session"):
        st.session_state[SLIDER_KEY] = 90; st.rerun()

deqe          = st.slider(t("minutes_question"), 1, 240, key=SLIDER_KEY)
total_seconds = deqe * 60
st.markdown('</div>', unsafe_allow_html=True)

# ── Timer control buttons
st.markdown('<div class="tcb-anchor"></div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    if not st.session_state.timer_running and not st.session_state.paused:
        dest_pe_bike = st.button(t("start_btn"), use_container_width=True, key="start_btn")
    elif st.session_state.paused:
        resume = st.button(t("resume_btn"), use_container_width=True, key="resume_btn")
    else:
        st.button(t("start_btn"), disabled=True, use_container_width=True, key="start_disabled")
with col2:
    if st.session_state.timer_running:
        stop_timer = st.button(t("pause_btn"), use_container_width=True, key="pause_btn")
    else:
        st.button(t("pause_btn"), disabled=True, use_container_width=True, key="pause_disabled")
with col3:
    dubare = st.button(t("reset_btn"), use_container_width=True, key="reset_btn")

# ── Quote card
hezt = t("quotes")
if not isinstance(hezt, list):
    hezt = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get("quotes", ["Keep going!"])
current_quote = hezt[st.session_state.quote_idx % len(hezt)]

refresh_lbl = {"badini": "نوى", "english": "New quote", "arabic": "اقتباس جديد"}.get(
    st.session_state.lang, "New quote"
)
_, qbtn_col = st.columns([5, 2])
with qbtn_col:
    if st.button(f"🔄 {refresh_lbl}", key="refresh_quote", use_container_width=True):
        st.session_state.quote_idx = random.randint(0, len(hezt) - 1)
        st.rerun()
st.markdown(f"""
<div class="quote-card">
    <div class="quote-mark">"</div>
    <div class="quote-text">{current_quote}</div>
</div>
""", unsafe_allow_html=True)

# ── Button actions
if "dest_pe_bike" in locals() and dest_pe_bike:
    st.session_state.timer_running = True
    st.session_state.paused        = False
    st.session_state.end_time      = time.time() + total_seconds
    st.session_state.total_seconds = total_seconds
    st.rerun()

if "resume" in locals() and resume:
    st.session_state.timer_running = True
    st.session_state.paused        = False
    st.session_state.end_time      = time.time() + st.session_state.remaining_at_pause
    st.rerun()

if "stop_timer" in locals() and stop_timer:
    st.session_state.timer_running      = False
    st.session_state.paused             = True
    st.session_state.remaining_at_pause = max(0, st.session_state.end_time - time.time())
    st.rerun()

if dubare:
    st.session_state.timer_running      = False
    st.session_state.paused             = False
    st.session_state.end_time           = None
    st.session_state.total_seconds      = 0
    st.session_state.remaining_at_pause = 0
    st.rerun()


# ── SVG circle timer
def render_circle(mins_val, secs_val, progress, color):
    dash = progress * 100.0
    glow = f"filter:drop-shadow(0 0 14px {color}bb);" if progress > 0 else ""
    st.markdown(f"""
    <div class="timer-card">
        <div style="display:flex;justify-content:center;">
            <svg width="260" height="260" viewBox="0 0 36 36" style="{glow}">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{TIMER_TRACK}" stroke-width="2.2"/>
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{color}" stroke-width="2.2"
                      stroke-linecap="round" stroke-dasharray="{dash:.2f}, 200"/>
                <text x="18" y="17" text-anchor="middle"
                      fill="{TIMER_TEXT}" font-size="6.5" font-weight="700" font-family="monospace">
                    {mins_val:02d}:{secs_val:02d}
                </text>
                <text x="18" y="22" text-anchor="middle"
                      fill="{TIMER_TEXT}99" font-size="2.6">{t('min_sec_labels')}</text>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)


if st.session_state.timer_running and st.session_state.end_time:
    remaining = st.session_state.end_time - time.time()
    if remaining > 0:
        mv, sv_ = divmod(int(remaining), 60)
        prog = min(1.0, 1.0 - (remaining / max(1, st.session_state.total_seconds)))
        render_circle(mv, sv_, prog, arc_color)
        st.success(t("timer_running", name=_effective_name, minutes=deqe, subject=ders))
        st.info(f"💬 {current_quote}")
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.timer_running = False
        st.session_state.paused        = False
        st.session_state.total_study_seconds += st.session_state.total_seconds
        st.session_state.completed_sessions  += 1
        st.session_state.daily_seconds       += st.session_state.total_seconds
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        if st.session_state.last_study_date == today_str:
            pass
        elif st.session_state.last_study_date == yesterday:
            st.session_state.streak += 1
        else:
            st.session_state.streak = 1
        st.session_state.last_study_date = today_str
        subject_name = ders.split(" ", 1)[1] if " " in ders else ders
        st.session_state.last_subject = subject_name
        now_ts  = datetime.now().strftime("%H:%M")
        minutes = st.session_state.total_seconds // 60
        st.session_state.study_history.append(
            f"{now_ts} - {subject_name} ({minutes} {t('minutes_unit')})"
        )
        save_data()
        components.html("""
        <script>
        (function(){
            var AC = window.AudioContext || window.webkitAudioContext;
            if (!AC) return;
            var ctx = new AC();
            function note(f, d, dur){
                var o = ctx.createOscillator(), g = ctx.createGain();
                o.connect(g); g.connect(ctx.destination);
                o.type = 'sine'; o.frequency.value = f;
                var t = ctx.currentTime + d;
                g.gain.setValueAtTime(0, t);
                g.gain.linearRampToValueAtTime(0.25, t + 0.02);
                g.gain.exponentialRampToValueAtTime(0.001, t + dur);
                o.start(t); o.stop(t + dur);
            }
            note(659, 0.0, 1.2); note(830, 0.22, 1.2); note(988, 0.44, 1.4);
        })();
        </script>
        """, height=0)
        st.balloons()
        st.success(t("timer_done"))

elif st.session_state.paused and st.session_state.remaining_at_pause > 0:
    mv, sv_ = divmod(int(st.session_state.remaining_at_pause), 60)
    prog = min(1.0, 1.0 - (st.session_state.remaining_at_pause / max(1, st.session_state.total_seconds)))
    render_circle(mv, sv_, prog, "#FFA500")
    pause_lbl = {
        "badini":  "⏸️ دەمژمێر راوەستیایە",
        "english": "⏸️ Timer paused",
        "arabic":  "⏸️ الموقت متوقف",
    }.get(st.session_state.lang, "⏸️ Timer paused")
    st.markdown(f'<div class="paused-banner">{pause_lbl}</div>', unsafe_allow_html=True)

else:
    render_circle(deqe, 0, 0.0, arc_color)
