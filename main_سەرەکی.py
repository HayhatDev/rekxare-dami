import streamlit as st
import time
import random
from datetime import datetime, date, timedelta
import json
import os
import streamlit.components.v1 as components

# --- PWA Manifest ---
st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js');
    }
</script>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="Rekxare Dami",
    page_icon="📚",
    initial_sidebar_state="expanded",
    layout="centered"
)

DATA_FILE = "study_data.json"

with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

if "lang" not in st.session_state:
    st.session_state.lang = "badini"

def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

SUBJECT_COLORS = TRANSLATIONS["badini"]["subjects_color"]

def subject_color(label: str) -> str:
    for key, col in SUBJECT_COLORS.items():
        if key in label:
            return col
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

def load_data():
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

def save_data():
    data = {
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
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if "data_loaded" not in st.session_state:
    load_data()
    st.session_state.data_loaded = True

DEFAULTS = {
    "total_study_seconds": 0, "completed_sessions": 0,
    "last_subject": "—", "study_history": [], "dark_mode": False,
    "streak": 0, "last_study_date": "", "daily_seconds": 0,
    "daily_goal_seconds": 7200, "timer_running": False,
    "end_time": None, "total_seconds": 0, "paused": False,
    "remaining_at_pause": 0,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
    PROG_TRACK     = "rgba(255,255,255,0.08)"
    GREET_BG       = "rgba(255,255,255,0.05)"
    GREET_BDR      = "rgba(255,255,255,0.09)"
    DIVIDER        = "rgba(255,255,255,0.08)"
    LANG_ACTIVE_BG = "rgba(76,175,80,0.25)"
    LANG_ACTIVE_C  = "#81c784"
    LANG_IDLE_BG   = "rgba(255,255,255,0.06)"
    LANG_IDLE_C    = "#8a8fa8"
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

st.markdown(f"""
<style>
*, *::before, *::after {{ box-sizing: border-box; }}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"],
section[data-testid="stMain"],
.main .block-container          {{ background-color: {APP_BG} !important; }}
[data-testid="stSidebar"]       {{ background-color: {SB_BG} !important; }}

.stApp *,
[data-testid="stSidebar"] *     {{ color: {TEXT_PRIMARY} !important; }}
h1, h2, h3                      {{ font-weight: 800 !important; letter-spacing: -0.3px; }}

.stTextInput input,
.stSelectbox > div > div,
.stTimeInput input              {{
    background-color: {INPUT_BG} !important;
    border: 1px solid {CARD_BORDER} !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    transition: border-color 0.2s ease !important;
}}
.stTextInput input:focus,
.stSelectbox > div > div:focus  {{ border-color: #4CAF50 !important; }}

[data-testid="stRadio"] > div   {{ gap: 6px !important; }}
[data-testid="stRadio"] label   {{
    background: {LANG_IDLE_BG} !important;
    color: {LANG_IDLE_C} !important;
    border-radius: 20px !important;
    padding: 4px 14px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    border: 1px solid {CARD_BORDER} !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}}
[data-testid="stRadio"] label:has(input:checked) {{
    background: {LANG_ACTIVE_BG} !important;
    color: {LANG_ACTIVE_C} !important;
    border-color: {LANG_ACTIVE_C} !important;
}}
[data-testid="stRadio"] input[type="radio"] {{ display: none !important; }}

.stButton > button {{
    background-color: {BTN_BG}    !important;
    color:            {BTN_COLOR} !important;
    border:           1px solid {BTN_BORDER} !important;
    border-radius:    12px !important;
    font-weight:      600  !important;
    font-size:        14px !important;
    padding:          10px 16px !important;
    transition:       all 0.18s ease !important;
    width:            100% !important;
}}
.stButton > button:hover:not(:disabled)  {{ opacity: 0.80 !important; transform: translateY(-1px) !important; }}
.stButton > button:active:not(:disabled) {{ transform: translateY(0px) !important; }}
.stButton > button:disabled              {{ opacity: 0.35 !important; cursor: not-allowed !important; }}

.btn-start  button {{ background: linear-gradient(135deg,#43a047,#66bb6a) !important; color:#fff !important; border-color:#388e3c !important; }}
.btn-resume button {{ background: linear-gradient(135deg,#43a047,#66bb6a) !important; color:#fff !important; border-color:#388e3c !important; }}
.btn-pause  button {{ background: linear-gradient(135deg,#ef6c00,#ffa726) !important; color:#fff !important; border-color:#e65100 !important; }}
.btn-reset  button {{ background: {BTN_BG} !important; color:{BTN_COLOR} !important; }}

.timer-card {{
    background:    {TIMER_CARD_BG};
    border:        1px solid {TIMER_CARD_BDR};
    border-radius: 24px;
    padding:       28px 16px 20px;
    margin:        12px 0 20px;
    text-align:    center;
    box-shadow:    0 2px 16px rgba(0,0,0,0.06);
}}
.timer-card svg {{
    width:  min(260px, 82vw) !important;
    height: min(260px, 82vw) !important;
}}

.sb-lbl {{
    font-size:      10px;
    font-weight:    700;
    letter-spacing: 1.4px;
    text-transform: uppercase;
    color:          {SECTION_LBL} !important;
    margin:         20px 0 8px 2px;
    display:        block;
}}

.stat-row   {{ display: flex; gap: 10px; margin-bottom: 4px; }}
.stat-card  {{
    flex: 1; background: {CARD_BG}; border: 1px solid {CARD_BORDER};
    border-radius: 14px; padding: 14px 10px; text-align: center;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}}
.stat-icon  {{ font-size: 20px; margin-bottom: 5px; line-height: 1; }}
.stat-val   {{ font-size: 16px; font-weight: 800; line-height: 1.2; }}
.stat-lbl   {{ font-size: 10px; color: {TEXT_MUTED} !important; margin-top: 3px; letter-spacing: 0.2px; }}

.streak-card {{
    background: {CARD_BG}; border: 1px solid {CARD_BORDER};
    border-radius: 14px; padding: 12px 14px;
    display: flex; align-items: center; gap: 12px; margin-bottom: 4px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}}
.streak-num {{ font-size: 24px; font-weight: 800; color: #FF9800 !important; line-height: 1; }}
.streak-sub {{ font-size: 11px; color: {TEXT_MUTED} !important; margin-top: 3px; }}

.goal-wrap {{
    background: {CARD_BG}; border: 1px solid {CARD_BORDER};
    border-radius: 14px; padding: 12px 14px; margin-bottom: 4px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.04);
}}
.goal-header {{
    display: flex; justify-content: space-between; align-items: center;
    font-size: 12px; color: {TEXT_MUTED} !important; margin-bottom: 8px;
}}
.goal-title {{ font-weight: 700; color: {TEXT_PRIMARY} !important; font-size: 13px; }}
.goal-track {{ background: {PROG_TRACK}; border-radius: 99px; height: 7px; overflow: hidden; }}
.goal-fill  {{ height: 7px; border-radius: 99px; transition: width 0.5s ease; }}

.subject-tag {{
    display: inline-block; background: {TAG_BG}; color: {TAG_COLOR} !important;
    border-radius: 20px; padding: 5px 14px; font-size: 13px; font-weight: 700;
}}

.act-list  {{ background: {ACTIVITY_BG}; border-radius: 12px; padding: 4px; overflow: hidden; }}
.act-item  {{
    display: flex; align-items: center; gap: 9px;
    padding: 7px 10px; border-radius: 9px; font-size: 12px;
}}
.act-dot   {{ width:7px;height:7px;border-radius:50%;background:#4CAF50;flex-shrink:0; }}
.act-empty {{ font-size:12px;color:{TEXT_MUTED} !important;padding:12px;text-align:center; }}

.settings-box {{
    background: {SETTINGS_BG}; border: 1px solid {SETTINGS_BDR};
    border-radius: 14px; padding: 14px;
}}

.greet-card {{
    background: {GREET_BG}; border: 1px solid {GREET_BDR};
    border-radius: 18px; padding: 22px 24px; margin-bottom: 20px;
    display: flex; align-items: center; gap: 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}}
.greet-emoji {{ font-size: 44px; line-height: 1; flex-shrink: 0; }}
.greet-name  {{ font-size: 21px; font-weight: 800; line-height: 1.2; }}
.greet-sub   {{ font-size: 13px; color: {TEXT_MUTED} !important; margin-top: 4px; }}
.greet-time  {{ font-size: 11px; color: {TEXT_MUTED} !important; margin-top: 3px; opacity: 0.8; }}

hr {{ border-color: {DIVIDER} !important; margin: 18px 0 !important; }}

@media (max-width: 640px) {{
    .greet-card     {{ padding: 16px 18px; gap: 14px; }}
    .greet-emoji    {{ font-size: 34px; }}
    .greet-name     {{ font-size: 17px; }}
    .stat-card      {{ padding: 10px 6px; }}
    .stat-val       {{ font-size: 14px; }}
    .timer-card     {{ padding: 16px 8px 14px; border-radius: 18px; }}
    .stButton > button {{ font-size: 13px !important; padding: 9px 10px !important; }}
    .streak-card    {{ padding: 10px 12px; gap: 10px; }}
    .goal-wrap      {{ padding: 10px 12px; }}
}}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
    <div style="padding:22px 4px 8px;">
        <div style="font-size:23px;font-weight:900;letter-spacing:-0.5px;">📚 Rekxare Dami</div>
        <div style="font-size:12px;color:{TEXT_MUTED};margin-top:3px;">{t("app_title")}</div>
    </div>
    <div style="height:1px;background:{DIVIDER};margin:10px 0 4px;"></div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sb-lbl">زمان | Language</span>', unsafe_allow_html=True)
    lang = st.radio("", ["badini", "english", "arabic"],
                    index=["badini", "english", "arabic"].index(st.session_state.lang),
                    horizontal=True, label_visibility="collapsed")
    if lang != st.session_state.lang:
        st.session_state.lang = lang
        save_data()
        st.rerun()

    st.markdown('<div style="height:4px;"></div>', unsafe_allow_html=True)

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
    """, unsafe_allow_html=True)

    st.markdown(f'<span class="sb-lbl">{t("streak_section")}</span>', unsafe_allow_html=True)
    sv = st.session_state.streak
    smsg = (t("streak_start") if sv == 0 else
            t("streak_ready") if sv < 3  else
            t("streak_keep")  if sv < 7  else
            t("streak_champ"))
    st.markdown(f"""
    <div class="streak-card">
        <div style="font-size:30px;line-height:1;">🔥</div>
        <div>
            <div class="streak-num">{sv}
                <span style="font-size:14px;font-weight:400;color:{TEXT_MUTED};">رۆژ</span>
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
    st.markdown(f'<div style="padding:2px 0 8px;"><span class="subject-tag">📖 {st.session_state.last_subject}</span></div>', unsafe_allow_html=True)

    st.markdown(f'<span class="sb-lbl">{t("recent_activity")}</span>', unsafe_allow_html=True)
    hist = st.session_state.study_history[-4:][::-1]
    if hist:
        rows = "".join(
            f'<div class="act-item"><div class="act-dot"></div><span>{e}</span></div>'
            for e in hist
        )
        st.markdown(f'<div class="act-list">{rows}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="act-list"><div class="act-empty">{t("no_activity")}</div></div>', unsafe_allow_html=True)

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
        st.markdown(f'<div style="font-size:13px;padding-top:6px;font-weight:500;">{t("dark_mode")}</div>', unsafe_allow_html=True)
    with tc:
        dark_btn = st.checkbox("", value=is_dark, label_visibility="collapsed")
    if dark_btn != is_dark:
        st.session_state.dark_mode = dark_btn
        save_data()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
    if st.button(t("clear_stats"), use_container_width=True):
        for k, v in [("total_study_seconds", 0), ("completed_sessions", 0),
                     ("last_subject", "—"), ("study_history", []),
                     ("streak", 0), ("daily_seconds", 0), ("last_study_date", "")]:
            st.session_state[k] = v
        save_data()
        st.rerun()

nav = st.text_input(t("enter_name"), t("default_name"), label_visibility="collapsed")

kurd_greet, eng_greet = get_greeting()
h_now = datetime.now().hour
greet_emoji = ("🌅" if 5 <= h_now < 12 else
               "☀️" if 12 <= h_now < 17 else
               "🌆" if 17 <= h_now < 21 else "🌙")
now_str = datetime.now().strftime("%A, %d %B %Y  •  %H:%M")

st.markdown(f"""
<div class="greet-card">
    <div class="greet-emoji">{greet_emoji}</div>
    <div style="min-width:0;">
        <div class="greet-name">{kurd_greet}، {nav}!</div>
        <div class="greet-sub">{eng_greet} — {t('welcome')} 📚</div>
        <div class="greet-time">{now_str}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

subjects_list = t("subjects")
if isinstance(subjects_list, str):
    subjects_list = TRANSLATIONS[st.session_state.lang]["subjects"]
ders = st.selectbox(t("select_subject"), subjects_list)
arc_color = subject_color(ders)

deqe = st.slider(t("minutes_question"), 1, 240, 25)
total_seconds = deqe * 60

col1, col2, col3 = st.columns(3)

with col1:
    if not st.session_state.timer_running and not st.session_state.paused:
        st.markdown('<div class="btn-start">', unsafe_allow_html=True)
        dest_pe_bike = st.button(t("start_btn"), use_container_width=True, key="start")
        st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.paused:
        st.markdown('<div class="btn-resume">', unsafe_allow_html=True)
        resume = st.button(t("resume_btn"), use_container_width=True, key="resume")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.button(t("start_btn"), disabled=True, use_container_width=True)

with col2:
    if st.session_state.timer_running:
        st.markdown('<div class="btn-pause">', unsafe_allow_html=True)
        stop_timer = st.button(t("pause_btn"), use_container_width=True, key="pause")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.button(t("pause_btn"), disabled=True, use_container_width=True)

with col3:
    st.markdown('<div class="btn-reset">', unsafe_allow_html=True)
    dubare = st.button(t("reset_btn"), use_container_width=True, key="reset")
    st.markdown('</div>', unsafe_allow_html=True)

hezt = t("quotes")

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

def render_circle(mins_val, secs_val, progress, color):
    dash = progress * 100.0
    glow = f"filter:drop-shadow(0 0 10px {color}aa);" if progress > 0 else ""
    st.markdown(f"""
    <div class="timer-card">
        <div style="display:flex;justify-content:center;">
            <svg width="260" height="260" viewBox="0 0 36 36" style="{glow}">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831
                         a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{TIMER_TRACK}" stroke-width="2.2"/>
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831
                         a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{color}" stroke-width="2.2"
                      stroke-linecap="round"
                      stroke-dasharray="{dash:.2f}, 200"/>
                <text x="18" y="17" text-anchor="middle"
                      fill="{TIMER_TEXT}" font-size="6.5" font-weight="700">
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
        prog = min(1.0, 1.0 - (remaining / st.session_state.total_seconds))
        render_circle(mv, sv_, prog, arc_color)
        st.success(t("timer_running", name=nav, minutes=deqe, subject=ders))
        st.info(f"💬 {random.choice(hezt)}")
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
            note(659, 0.0, 1.2);
            note(830, 0.22, 1.2);
            note(988, 0.44, 1.4);
        })();
        </script>
        """, height=0)
        st.balloons()
        st.success(t("timer_done"))

elif st.session_state.paused and st.session_state.remaining_at_pause > 0:
    mv, sv_ = divmod(int(st.session_state.remaining_at_pause), 60)
    prog = min(1.0, 1.0 - (st.session_state.remaining_at_pause / st.session_state.total_seconds))
    render_circle(mv, sv_, prog, "#FFA500")

else:
    render_circle(deqe, 0, 0.0, arc_color)
