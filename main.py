import streamlit as st
import time
import random
from datetime import datetime, date, timedelta
import json
import os
import streamlit.components.v1 as components

# ══════════════════════════════════════════════════════════
#  PWA MANIFEST & PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.markdown("""
<link rel="manifest" href="/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js');
    }
</script>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Rekxare Dami",
    page_icon="📚",
    initial_sidebar_state="collapsed",
    layout="centered"
)

# ══════════════════════════════════════════════════════════
#  TRANSLATIONS & DEFAULTS
# ══════════════════════════════════════════════════════════
with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

if "lang" not in st.session_state:
    st.session_state.lang = "badini"
if "data_key" not in st.session_state:
    st.session_state.data_key = "default"
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

SCHEDULE_FILE = "schedule_data.json"

# ══════════════════════════════════════════════════════════
#  DATA FUNCTIONS
# ══════════════════════════════════════════════════════════
def get_data_file():
    key = st.session_state.get("data_key", "default")
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
        st.session_state.dark_mode           = data.get("dark_mode", False)
        st.session_state.streak              = data.get("streak", 0)
        st.session_state.last_study_date     = data.get("last_study_date", "")
        st.session_state.daily_seconds       = data.get("daily_seconds", 0)
        st.session_state.daily_goal_seconds  = data.get("daily_goal_seconds", 7200)
        st.session_state.lang                = data.get("lang", "badini")
        st.session_state.student_name        = data.get("student_name", "")

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
        }, f, ensure_ascii=False, indent=2)

# ══════════════════════════════════════════════════════════
#  SIMPLE LOGIN
# ══════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.title("📚 Rekxare Dami")
    st.markdown("### Welcome! Enter your email to continue.")
    
    email = st.text_input("Email", placeholder="example@gmail.com")
    
    if email.strip() and "@" not in email and "." not in email:
        st.error("Please enter a valid email address.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🚀 Enter", use_container_width=True) and email.strip() and "@" in email and "." in email:
            st.session_state.user_email = email.strip()
            st.session_state.logged_in = True
            st.session_state.data_key = email.split("@")[0]
            load_data()
            st.rerun()
    
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="stSidebarCollapsedControl"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.stop()

st.session_state.data_key = st.session_state.user_email.split("@")[0]

# ══════════════════════════════════════════════════════════
#  TRANSLATION HELPER
# ══════════════════════════════════════════════════════════
def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

# ══════════════════════════════════════════════════════════
#  SUBJECT COLORS
# ══════════════════════════════════════════════════════════
SUBJECT_COLOR_LIST = [
    "#2196F3", "#9C27B0", "#FF5722", "#00BCD4", "#4CAF50",
    "#795548", "#FF9800", "#607D8B", "#FFC107"
]

def subject_color(label: str) -> str:
    try:
        idx = subjects_list.index(label)
        return SUBJECT_COLOR_LIST[idx]
    except (ValueError, IndexError):
        return "#4CAF50"

# ══════════════════════════════════════════════════════════
#  GREETING & SCHEDULE HELPERS
# ══════════════════════════════════════════════════════════
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
    if os.path.exists(SCHEDULE_FILE):
        try:
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return today_key, data.get("schedule", {}).get(today_key, [])
        except Exception:
            return today_key, []
    return today_key, []

# ══════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ══════════════════════════════════════════════════════════
DEFAULTS = {
    "total_study_seconds": 0, "completed_sessions": 0,
    "last_subject": "—", "study_history": [], "dark_mode": False,
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

# ══════════════════════════════════════════════════════════
#  DAILY RESET & CALCULATIONS
# ══════════════════════════════════════════════════════════
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

_days_map = {"badini": "رۆژ", "english": "days", "arabic": "يوم"}
days_lbl  = _days_map.get(st.session_state.lang, "رۆژ")

# ══════════════════════════════════════════════════════════
#  THEME TOKENS
# ══════════════════════════════════════════════════════════
if is_dark:
    APP_BG         = "#1a1a2e"
    SB_BG          = "#16213e"
    CARD_BG        = "rgba(255,255,255,0.04)"
    CARD_BORDER    = "rgba(255,255,255,0.08)"
    TEXT_PRIMARY   = "#e2e2e2"
    TEXT_MUTED     = "#8a8fa8"
    SECTION_LBL    = "#555c72"
    TAG_BG         = "rgba(76,175,80,0.15)"
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
    GREET_BG       = "rgba(255,255,255,0.04)"
    GREET_BDR      = "rgba(255,255,255,0.08)"
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
    SETUP_BDR      = "rgba(255,255,255,0.08)"
    GOAL_WIN_BG    = "rgba(76,175,80,0.14)"
    GOAL_WIN_BDR   = "rgba(76,175,80,0.30)"
    PRESET_BG      = "rgba(255,255,255,0.06)"
    PRESET_BDR     = "rgba(255,255,255,0.10)"
    SHADOW         = "rgba(0,0,0,0.35)"
    AI_EXP_BG      = "rgba(255,255,255,0.03)"
    AI_EXP_BDR     = "rgba(171,71,188,0.25)"
else:
    APP_BG         = "#eef1f8"
    SB_BG          = "#f5f7fc"
    CARD_BG        = "#ffffff"
    CARD_BORDER    = "#dde4f0"
    TEXT_PRIMARY   = "#1a1a2e"
    TEXT_MUTED     = "#6b7280"
    SECTION_LBL    = "#9ca3af"
    TAG_BG         = "rgba(76,175,80,0.08)"
    TAG_COLOR      = "#2e7d32"
    ACTIVITY_BG    = "#f0f3fa"
    SETTINGS_BG    = "#f0f3fa"
    SETTINGS_BDR   = "#d0d8ea"
    INPUT_BG       = "#ffffff"
    BTN_BG         = "#e2e8f5"
    BTN_COLOR      = "#1a1a2e"
    BTN_BORDER     = "#c5d0e6"
    TIMER_TRACK    = "#dde4f0"
    TIMER_TEXT     = "#1a1a2e"
    TIMER_CARD_BG  = "#ffffff"
    TIMER_CARD_BDR = "#dde4f0"
    PROG_TRACK     = "#dde4f0"
    GREET_BG       = "#ffffff"
    GREET_BDR      = "#dde4f0"
    DIVIDER        = "#e2e8f5"
    LANG_ACTIVE_BG = "rgba(76,175,80,0.12)"
    LANG_ACTIVE_C  = "#2e7d32"
    LANG_IDLE_BG   = "#eef1f8"
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
    SCHED_BDR      = "#dde4f0"
    SCHED_DONE_BG  = "rgba(76,175,80,0.05)"
    SCHED_TODO_BG  = "#fafbfd"
    QUOTE_BG       = "#ffffff"
    QUOTE_BDR      = "#dde4f0"
    QUOTE_COLOR    = "#3949ab"
    SETUP_BG       = "#ffffff"
    SETUP_BDR      = "#dde4f0"
    GOAL_WIN_BG    = "rgba(76,175,80,0.08)"
    GOAL_WIN_BDR   = "rgba(76,175,80,0.22)"
    PRESET_BG      = "#eef1f8"
    PRESET_BDR     = "#c5d0e6"
    SHADOW         = "rgba(0,0,0,0.06)"
    AI_EXP_BG      = "#faf8ff"
    AI_EXP_BDR     = "rgba(171,71,188,0.18)"

# ══════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

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

.stTextInput input,
.stSelectbox > div > div,
.stTimeInput input {{
    background-color: {INPUT_BG} !important;
    border: 1.5px solid {CARD_BORDER} !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    padding: 10px 14px !important;
}}
.stTextInput input:focus {{
    border-color: #4CAF50 !important;
    box-shadow: 0 0 0 3px rgba(76,175,80,0.13) !important;
    outline: none !important;
}}

/* ── Selectbox Selected Text FIX ── */
.stSelectbox [data-testid="stMarkdownContainer"] p,
.stSelectbox span,
.stSelectbox div[role="combobox"] {{
    color: {TEXT_PRIMARY} !important;
}}

[data-testid="stRadio"] > div {{ gap: 6px !important; flex-wrap: wrap !important; }}
[data-testid="stRadio"] label {{
    background: {LANG_IDLE_BG} !important;
    color: {LANG_IDLE_C} !important;
    border-radius: 20px !important;
    padding: 6px 16px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    border: 1.5px solid {CARD_BORDER} !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    min-height: 36px !important;
    display: flex !important; align-items: center !important;
}}
[data-testid="stRadio"] label:has(input:checked) {{
    background: {LANG_ACTIVE_BG} !important;
    color: {LANG_ACTIVE_C} !important;
    border-color: {LANG_ACTIVE_C} !important;
}}
[data-testid="stRadio"] input[type="radio"] {{ display: none !important; }}

/* ── Buttons ── */
.stButton > button {{
    background-color: {BTN_BG} !important;
    color:            {BTN_COLOR} !important;
    border:           1.5px solid {BTN_BORDER} !important;
    border-radius:    12px !important;
    font-weight:      600 !important;
    font-size:        14px !important;
    font-family:      'Inter', system-ui, sans-serif !important;
    padding:          10px 16px !important;
    min-height:       44px !important;
    transition:       all 0.18s ease !important;
    width:            100% !important;
    -webkit-tap-highlight-color: transparent !important;
}}
.stButton > button:hover:not(:disabled) {{
    filter: brightness(1.07) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 14px {SHADOW} !important;
}}
.stButton > button:active:not(:disabled) {{
    transform: translateY(0) !important;
    box-shadow: none !important;
}}
.stButton > button:disabled {{
    opacity: 0.35 !important;
    cursor: not-allowed !important;
}}

/* ── Timer control buttons ── */
.tcb-anchor {{ display: none !important; }}
.element-container:has(.tcb-anchor) + div
    [data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton button:not(:disabled) {{
    background: linear-gradient(135deg, #388e3c, #4caf50) !important;
    color: #fff !important; border-color: #2e7d32 !important;
    box-shadow: 0 3px 12px rgba(67,160,71,0.35) !important;
}}
.element-container:has(.tcb-anchor) + div
    [data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton button:not(:disabled) {{
    background: linear-gradient(135deg, #e65100, #ff9800) !important;
    color: #fff !important; border-color: #bf360c !important;
    box-shadow: 0 3px 12px rgba(239,108,0,0.35) !important;
}}

/* ── Quick preset buttons ── */
.preset-anchor {{ display: none !important; }}
.element-container:has(.preset-anchor) + div
    [data-testid="stHorizontalBlock"] .stButton button {{
    background: {PRESET_BG} !important;
    color: {TEXT_PRIMARY} !important;
    border: 1.5px solid {PRESET_BDR} !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    padding: 8px 6px !important;
    font-weight: 700 !important;
    min-height: 40px !important;
}}
.element-container:has(.preset-anchor) + div
    [data-testid="stHorizontalBlock"] .stButton button:hover:not(:disabled) {{
    border-color: #4CAF50 !important;
    color: #4CAF50 !important;
    background: {TAG_BG} !important;
    box-shadow: none !important;
    filter: none !important;
}}

/* ── Cards ── */
.timer-card {{
    background: {TIMER_CARD_BG}; border: 1.5px solid {TIMER_CARD_BDR};
    border-radius: 24px; padding: 28px 16px 20px;
    margin: 8px 0 16px; text-align: center;
    box-shadow: 0 4px 20px {SHADOW};
}}
.timer-card svg {{
    width: min(260px, 78vw) !important;
    height: min(260px, 78vw) !important;
}}
.setup-card {{
    background: {SETUP_BG}; border: 1.5px solid {SETUP_BDR};
    border-radius: 20px; padding: 20px 24px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px {SHADOW};
}}
.quote-card {{
    background: {QUOTE_BG}; border: 1.5px solid {QUOTE_BDR};
    border-radius: 16px; padding: 18px 20px;
    margin: 4px 0 14px;
    box-shadow: 0 2px 12px {SHADOW};
    position: relative;
}}
.quote-mark {{ font-size: 36px; line-height: 1; opacity: 0.12; position: absolute; top: 12px; left: 16px; }}
.quote-text {{
    font-size: 14px; font-weight: 500; font-style: italic;
    color: {QUOTE_COLOR} !important; line-height: 1.6;
    padding-left: 22px; padding-right: 8px;
}}
.paused-banner {{
    background: {WARN_BG}; border: 1.5px solid {WARN_BDR};
    border-radius: 14px; padding: 14px 18px; text-align: center;
    font-size: 15px; font-weight: 700; color: {WARN_COLOR} !important;
    margin-bottom: 12px;
}}
.goal-win-banner {{
    background: {GOAL_WIN_BG}; border: 1.5px solid {GOAL_WIN_BDR};
    border-radius: 16px; padding: 16px 20px;
    display: flex; align-items: center; gap: 16px;
    margin-bottom: 18px;
    box-shadow: 0 4px 16px rgba(76,175,80,0.15);
}}
.goal-win-icon {{ font-size: 36px; line-height: 1; flex-shrink: 0; }}
.goal-win-text {{ font-size: 15px; font-weight: 800; color: #4CAF50 !important; }}
.goal-win-sub  {{ font-size: 12px; color: {TEXT_MUTED} !important; margin-top: 3px; font-weight: 500; }}

.subject-color-dot {{
    display: inline-block; width: 12px; height: 12px;
    border-radius: 50%; margin-right: 8px; flex-shrink: 0;
    box-shadow: 0 0 6px currentColor;
}}
.subject-pill {{
    display: inline-flex; align-items: center;
    background: {TAG_BG}; color: {TAG_COLOR} !important;
    border-radius: 24px; padding: 6px 16px; font-size: 14px; font-weight: 700;
    margin-bottom: 14px;
}}

.section-hdr {{
    display: flex; align-items: center; gap: 10px;
    font-size: 11px; font-weight: 800; letter-spacing: 1.4px;
    text-transform: uppercase; color: {SECTION_LBL} !important;
    margin: 24px 0 14px;
}}
.section-hdr span {{ color: {SECTION_LBL} !important; }}
.section-line {{ flex: 1; height: 1.5px; background: {DIVIDER}; border-radius: 99px; }}

/* ── Sidebar labels ── */
.sb-lbl {{
    font-size: 10px; font-weight: 800; letter-spacing: 1.5px;
    text-transform: uppercase; color: {SECTION_LBL} !important;
    margin: 20px 0 10px 2px; display: block;
}}
.stat-row  {{ display: flex; gap: 10px; margin-bottom: 10px; }}
.stat-card {{
    flex: 1; background: {CARD_BG}; border: 1.5px solid {CARD_BORDER};
    border-radius: 16px; padding: 16px 10px; text-align: center;
    box-shadow: 0 2px 8px {SHADOW};
}}
.stat-icon {{ font-size: 22px; margin-bottom: 6px; line-height: 1; }}
.stat-val  {{ font-size: 16px; font-weight: 800; line-height: 1.2; }}
.stat-lbl  {{ font-size: 10px; color: {TEXT_MUTED} !important; margin-top: 4px; font-weight: 500; }}
.today-stat {{
    background: {TODAY_CARD_BG}; border: 1.5px solid {TODAY_CARD_BDR};
    border-radius: 16px; padding: 12px 16px; margin-bottom: 6px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 2px 8px {SHADOW};
}}
.today-stat-label {{ font-size: 12px; font-weight: 700; }}
.today-stat-val   {{ font-size: 16px; font-weight: 800; color: #4CAF50 !important; }}

.streak-card {{
    background: {CARD_BG}; border: 1.5px solid {CARD_BORDER};
    border-radius: 16px; padding: 14px 16px;
    display: flex; align-items: center; gap: 14px; margin-bottom: 6px;
    box-shadow: 0 2px 8px {SHADOW};
}}
.streak-num {{ font-size: 26px; font-weight: 800; color: #FF9800 !important; line-height: 1; }}
.streak-sub {{ font-size: 11px; color: {TEXT_MUTED} !important; margin-top: 4px; font-weight: 500; }}

.goal-wrap {{
    background: {CARD_BG}; border: 1.5px solid {CARD_BORDER};
    border-radius: 16px; padding: 14px 16px; margin-bottom: 6px;
    box-shadow: 0 2px 8px {SHADOW};
}}
.goal-header {{ display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: {TEXT_MUTED} !important; margin-bottom: 10px; }}
.goal-title  {{ font-weight: 700; color: {TEXT_PRIMARY} !important; font-size: 13px; }}
.goal-track  {{ background: {PROG_TRACK}; border-radius: 99px; height: 8px; overflow: hidden; }}
.goal-fill   {{ height: 8px; border-radius: 99px; transition: width 0.5s ease; }}

.subject-tag {{ display: inline-block; background: {TAG_BG}; color: {TAG_COLOR} !important; border-radius: 20px; padding: 6px 16px; font-size: 13px; font-weight: 700; }}
.act-list  {{ background: {ACTIVITY_BG}; border-radius: 14px; padding: 6px; overflow: hidden; }}
.act-item  {{ display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 10px; font-size: 12px; }}
.act-dot   {{ width: 7px; height: 7px; border-radius: 50%; background: #4CAF50; flex-shrink: 0; }}
.act-empty {{ font-size: 12px; color: {TEXT_MUTED} !important; padding: 14px; text-align: center; }}

.settings-box {{ background: {SETTINGS_BG}; border: 1.5px solid {SETTINGS_BDR}; border-radius: 16px; padding: 16px; }}
.danger-box {{
    background: {DANGER_BG}; border: 1.5px solid {DANGER_BDR};
    border-radius: 14px; padding: 12px 16px; margin-bottom: 8px;
    font-size: 13px; font-weight: 700; color: {DANGER_COLOR} !important; text-align: center;
}}

.greet-card {{
    background: {GREET_BG}; border: 1.5px solid {GREET_BDR};
    border-radius: 20px; padding: 24px 28px; margin-bottom: 20px;
    display: flex; align-items: center; gap: 20px;
    box-shadow: 0 4px 18px {SHADOW};
}}
.greet-emoji {{ font-size: 48px; line-height: 1; flex-shrink: 0; }}
.greet-name  {{ font-size: 22px; font-weight: 800; line-height: 1.2; letter-spacing: -0.3px; }}
.greet-sub   {{ font-size: 13px; color: {TEXT_MUTED} !important; margin-top: 5px; font-weight: 500; }}
.greet-time  {{ font-size: 11px; color: {TEXT_MUTED} !important; margin-top: 4px; opacity: 0.75; }}

.sched-card {{ background: {SCHED_BG}; border: 1.5px solid {SCHED_BDR}; border-radius: 18px; padding: 18px 20px; margin-bottom: 18px; box-shadow: 0 2px 12px {SHADOW}; }}
.sched-title {{ font-size: 12px; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; color: {TEXT_MUTED} !important; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }}
.sched-item      {{ display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 10px; margin-bottom: 5px; font-size: 13px; }}
.sched-item-done {{ background: {SCHED_DONE_BG}; opacity: 0.65; }}
.sched-item-todo {{ background: {SCHED_TODO_BG}; }}
.sched-time      {{ font-size: 11px; font-weight: 700; color: {TEXT_MUTED} !important; min-width: 72px; flex-shrink: 0; background: {PROG_TRACK}; padding: 2px 8px; border-radius: 6px; text-align: center; }}
.sched-task      {{ font-weight: 500; flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.sched-task-done {{ text-decoration: line-through; color: {TEXT_MUTED} !important; }}
.sched-check     {{ flex-shrink: 0; }}
.sched-prog-wrap {{ margin-top: 12px; background: {PROG_TRACK}; border-radius: 99px; height: 6px; overflow: hidden; }}
.sched-prog-fill {{ height: 6px; border-radius: 99px; }}

hr {{ border-color: {DIVIDER} !important; margin: 20px 0 !important; }}

/* ── Mobile ── */
@media (max-width: 640px) {{
    .greet-card  {{ padding: 16px 18px; gap: 14px; }}
    .greet-emoji {{ font-size: 34px; }}
    .greet-name  {{ font-size: 18px; }}
    .greet-sub   {{ font-size: 12px; }}
    .greet-time  {{ display: none; }}
    .stat-card   {{ padding: 12px 6px; }}
    .stat-val    {{ font-size: 14px; }}
    .timer-card  {{ padding: 16px 8px 14px; border-radius: 18px; }}
    .stButton > button {{ font-size: 13px !important; }}
    .setup-card  {{ padding: 16px 14px; }}
    .quote-card  {{ padding: 16px 14px; }}
    .quote-text  {{ font-size: 13px; }}
    .goal-win-banner {{ padding: 14px 16px; gap: 12px; }}
    .goal-win-icon   {{ font-size: 28px; }}
    .goal-win-text   {{ font-size: 14px; }}
}}

@media (max-width: 380px) {{
    .greet-emoji {{ font-size: 28px; }}
    .greet-name  {{ font-size: 16px; }}
    .stat-val    {{ font-size: 13px; }}
    .stat-icon   {{ font-size: 18px; }}
    .stButton > button {{ font-size: 12px !important; padding: 8px 6px !important; }}
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding:24px 4px 10px;">
        <div style="font-size:24px;font-weight:900;letter-spacing:-0.5px;">📚 Rekxare Dami</div>
        <div style="font-size:12px;color:{TEXT_MUTED};margin-top:3px;font-weight:500;">{t("app_title")}</div>
    </div>
    <div style="height:1.5px;background:{DIVIDER};margin:12px 0 6px;border-radius:99px;"></div>
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
    st.markdown(f'<div style="padding:2px 0 10px;"><span class="subject-tag">📖 {st.session_state.last_subject}</span></div>', unsafe_allow_html=True)

    st.markdown(f'<span class="sb-lbl">{t("recent_activity")}</span>', unsafe_allow_html=True)
    hist = st.session_state.study_history[-4:][::-1]
    if hist:
        rows = "".join(f'<div class="act-item"><div class="act-dot"></div><span>{e}</span></div>' for e in hist)
        st.markdown(f'<div class="act-list">{rows}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="act-list"><div class="act-empty">{t("no_activity")}</div></div>', unsafe_allow_html=True)

    st.markdown(f'<span class="sb-lbl">{t("settings")}</span>', unsafe_allow_html=True)
    st.markdown('<div class="settings-box">', unsafe_allow_html=True)
    goal_mins = st.slider(f'🎯 {t("today_goal")} ({t("minutes_unit")})',
                          30, 480, st.session_state.daily_goal_seconds // 60, step=15)
    if goal_mins * 60 != st.session_state.daily_goal_seconds:
        st.session_state.daily_goal_seconds = goal_mins * 60
        save_data()
        st.rerun()
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
    dc, tc = st.columns([3, 1])
    with dc:
        st.markdown(f'<div style="font-size:13px;padding-top:6px;font-weight:600;">{t("dark_mode")}</div>', unsafe_allow_html=True)
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
                             ("streak", 0), ("daily_seconds", 0), ("last_study_date", "")]:
                    st.session_state[k] = v
                st.session_state.confirm_clear = False
                save_data()
                st.rerun()
        with cc2:
            if st.button("✗", use_container_width=True, key="confirm_no"):
                st.session_state.confirm_clear = False
                st.rerun()

# ══════════════════════════════════════════════════════════
#  MAIN PAGE
# ══════════════════════════════════════════════════════════

# ── Name input ──
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

# ── Greeting card ──
kurd_greet, eng_greet = get_greeting()
h_now       = datetime.now().hour
greet_emoji = ("🌅" if 5 <= h_now < 12 else "☀️" if 12 <= h_now < 17 else
               "🌆" if 17 <= h_now < 21 else "🌙")
now_str     = datetime.now().strftime("%A, %d %B  •  %H:%M")

st.markdown(f"""
<div class="greet-card">
    <div class="greet-emoji">{greet_emoji}</div>
    <div style="min-width:0;">
        <div class="greet-name">{kurd_greet}، {_effective_name}!</div>
        <div class="greet-sub">{eng_greet} — {t('welcome')} 📚</div>
        <div class="greet-time">{now_str}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Daily goal achieved banner ──
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

# ── Today's schedule preview ──
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
    html_content += f'<div class="sched-title">{sched_title_text} <span style="margin-left:auto;font-size:11px;color:{TEXT_MUTED};font-weight:500;letter-spacing:0;">{done_count}/{total_count} — {pct_sched}%</span></div>'
    
    for ti in today_tasks_named[:6]:
        done_cls  = "sched-item-done" if ti.get("done") else "sched-item-todo"
        task_cls  = "sched-task-done" if ti.get("done") else "sched-task"
        check_ico = "✅" if ti.get("done") else "⬜"
        html_content += f'<div class="sched-item {done_cls}"><span class="sched-time">{ti.get("start","")}–{ti.get("end","")}</span><span class="{task_cls}">{ti.get("task","")}</span><span class="sched-check">{check_ico}</span></div>'
    
    if len(today_tasks_named) > 6:
        extra = len(today_tasks_named) - 6
        if st.session_state.lang == "english":
            extra_lbl = f"+{extra} more"
        elif st.session_state.lang == "badini":
            extra_lbl = f"+{extra} زێدەکرن"
        else:
            extra_lbl = f"+{extra} أكثر"
        html_content += f'<div style="font-size:11px;color:{TEXT_MUTED};padding:4px 10px;">{extra_lbl}</div>'
    
    html_content += f'<div class="sched-prog-wrap"><div class="sched-prog-fill" style="width:{pct_sched}%;background:{prog_color};"></div></div>'
    html_content += '</div>'
    
    st.markdown(html_content, unsafe_allow_html=True)

# ── Timer section ──
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
    unsafe_allow_html=True
)

duration_lbl = {"badini":"⏱ دەمێ خواندنێ","english":"⏱ Duration","arabic":"⏱ المدة"}.get(st.session_state.lang,"⏱ Duration")
st.markdown(f'<div style="font-size:12px;font-weight:700;color:{TEXT_MUTED};margin-bottom:6px;">{duration_lbl}</div>', unsafe_allow_html=True)

# Quick preset buttons
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

# ── Timer control buttons ──
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

# ── Quote card ──
hezt = t("quotes")
if not isinstance(hezt, list):
    hezt = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get("quotes", ["Keep going!"])
current_quote = hezt[st.session_state.quote_idx % len(hezt)]

refresh_lbl = {"badini":"نوى","english":"New quote","arabic":"اقتباس جديد"}.get(st.session_state.lang,"New quote")
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

# ── Button actions ──
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

# ── SVG circle timer ──
def render_circle(mins_val, secs_val, progress, color):
    dash = progress * 100.0
    glow = f"filter:drop-shadow(0 0 14px {color}cc);" if progress > 0 else ""
    st.markdown(f"""
    <div class="timer-card">
        <div style="display:flex;justify-content:center;">
            <svg width="260" height="260" viewBox="0 0 36 36" style="{glow}">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{TIMER_TRACK}" stroke-width="2.5"/>
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{color}" stroke-width="2.5"
                      stroke-linecap="round" stroke-dasharray="{dash:.2f}, 200"/>
                <text x="18" y="17" text-anchor="middle"
                      fill="{TIMER_TEXT}" font-size="6.5" font-weight="800" font-family="monospace">
                    {mins_val:02d}:{secs_val:02d}
                </text>
                <text x="18" y="22.5" text-anchor="middle"
                      fill="{TIMER_TEXT}aa" font-size="2.6" font-weight="600">{t('min_sec_labels')}</text>
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
    pause_lbl = {"badini":"⏸️ دەمژمێر راوەستیایە","english":"⏸️ Timer paused","arabic":"⏸️ الموقت متوقف"}
    st.markdown(f'<div class="paused-banner">{pause_lbl.get(st.session_state.lang,"⏸️ Timer paused")}</div>', unsafe_allow_html=True)

else:
    render_circle(deqe, 0, 0.0, arc_color)
