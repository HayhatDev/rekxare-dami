import streamlit as st
import time
import random
from datetime import datetime, date, timedelta
import json
import os
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Rekxare Dami",
    page_icon="📚",
    initial_sidebar_state="expanded"
)

DATA_FILE = "study_data.json"

SUBJECT_COLORS = {
    "بیرکاری":      "#2196F3",
    "فیزیا":        "#9C27B0",
    "کیمیا":        "#FF5722",
    "ئینگلیزی":     "#00BCD4",
    "زیندەوەرزانی": "#4CAF50",
    "مێژوو":        "#795548",
    "جوگرافیا":     "#FF9800",
    "کۆمپیوتەر":    "#607D8B",
    "ئايين":        "#FFC107",
}

def subject_color(label: str) -> str:
    for key, col in SUBJECT_COLORS.items():
        if key in label:
            return col
    return "#4CAF50"

def get_greeting():
    h = datetime.now().hour
    if 5 <= h < 12:
        return "سبەی خوش", "Good Morning"
    elif 12 <= h < 17:
        return "نیوڕۆیێ خوش", "Good Afternoon"
    elif 17 <= h < 21:
        return "ئێڤارێ خوش", "Good Evening"
    else:
        return "شەڤێ خوش", "Good Night"

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
    GREET_BG       = "rgba(255,255,255,0.04)"
    GREET_BDR      = "rgba(255,255,255,0.09)"
    DIVIDER        = "rgba(255,255,255,0.08)"
else:
    APP_BG         = "#eef1f7"
    SB_BG          = "#f8fafc"
    CARD_BG        = "#ffffff"
    CARD_BORDER    = "#dde3ed"
    TEXT_PRIMARY   = "#1a1a2e"
    TEXT_MUTED     = "#6b7280"
    SECTION_LBL    = "#9ca3af"
    TAG_BG         = "rgba(76,175,80,0.10)"
    TAG_COLOR      = "#2e7d32"
    ACTIVITY_BG    = "#e8edf5"
    SETTINGS_BG    = "#e8edf5"
    SETTINGS_BDR   = "#d0d8e8"
    INPUT_BG       = "#ffffff"
    BTN_BG         = "#e2e8f4"
    BTN_COLOR      = "#1a1a2e"
    BTN_BORDER     = "#c8d0df"
    TIMER_TRACK    = "#dde3ed"
    TIMER_TEXT     = "#1a1a2e"
    TIMER_CARD_BG  = "rgba(76,175,80,0.05)"
    TIMER_CARD_BDR = "rgba(76,175,80,0.15)"
    PROG_TRACK     = "#dde3ed"
    GREET_BG       = "#ffffff"
    GREET_BDR      = "#dde3ed"
    DIVIDER        = "#dde3ed"

st.markdown(f"""
<style>
    .stApp                              {{ background-color: {APP_BG}  !important; }}
    [data-testid="stSidebar"]           {{ background-color: {SB_BG}  !important; }}
    .stApp *, [data-testid="stSidebar"] * {{ color: {TEXT_PRIMARY} !important; }}
    .stTextInput input, .stSelectbox > div > div, .stSlider > div {{
        background-color: {INPUT_BG} !important;
        border-color: {CARD_BORDER} !important;
        border-radius: 10px !important;
    }}
    .stButton > button {{
        background-color: {BTN_BG} !important; color: {BTN_COLOR} !important;
        border: 1px solid {BTN_BORDER} !important;
        border-radius: 10px !important; font-weight: 600 !important;
        transition: opacity 0.18s ease !important;
    }}
    .stButton > button:hover:not(:disabled) {{ opacity: 0.75 !important; }}
    .timer-card {{
        background: {TIMER_CARD_BG}; border: 1px solid {TIMER_CARD_BDR};
        border-radius: 20px; padding: 24px 16px 16px; margin: 16px 0; text-align: center;
    }}
    div[data-testid="metric-container"] {{ display: none !important; }}
    .sb-lbl {{
        font-size: 10px; font-weight: 700; letter-spacing: 1.2px;
        text-transform: uppercase; color: {SECTION_LBL} !important; margin: 18px 0 8px 2px;
    }}
    .stat-row {{ display: flex; gap: 10px; margin-bottom: 4px; }}
    .stat-card {{
        flex: 1; background: {CARD_BG}; border: 1px solid {CARD_BORDER};
        border-radius: 12px; padding: 12px 10px; text-align: center;
    }}
    .stat-icon {{ font-size: 18px; margin-bottom: 4px; }}
    .stat-val  {{ font-size: 17px; font-weight: 700; line-height: 1.2; }}
    .stat-lbl  {{ font-size: 10px; color: {TEXT_MUTED} !important; margin-top: 2px; }}
    .streak-card {{
        background: {CARD_BG}; border: 1px solid {CARD_BORDER};
        border-radius: 12px; padding: 10px 14px;
        display: flex; align-items: center; gap: 10px; margin-bottom: 4px;
    }}
    .streak-num {{ font-size: 22px; font-weight: 800; color: #FF9800 !important; }}
    .streak-sub {{ font-size: 10px; color: {TEXT_MUTED} !important; margin-top: 2px; }}
    .goal-wrap {{
        background: {CARD_BG}; border: 1px solid {CARD_BORDER};
        border-radius: 12px; padding: 11px 14px; margin-bottom: 4px;
    }}
    .goal-header {{
        display: flex; justify-content: space-between;
        font-size: 12px; color: {TEXT_MUTED} !important; margin-bottom: 7px;
    }}
    .goal-title {{ font-weight: 600; color: {TEXT_PRIMARY} !important; }}
    .goal-track {{ background: {PROG_TRACK}; border-radius: 99px; height: 8px; overflow: hidden; }}
    .goal-fill  {{ height: 8px; border-radius: 99px; transition: width 0.4s ease; }}
    .subject-tag {{
        display: inline-block; background: {TAG_BG}; color: {TAG_COLOR} !important;
        border-radius: 20px; padding: 4px 12px; font-size: 13px; font-weight: 600;
    }}
    .act-list  {{ background: {ACTIVITY_BG}; border-radius: 10px; padding: 6px 4px; }}
    .act-item  {{ display: flex; align-items: center; gap: 8px; padding: 6px 8px; font-size: 12px; }}
    .act-dot   {{ width:6px;height:6px;border-radius:50%;background:#4CAF50;flex-shrink:0; }}
    .act-empty {{ font-size:12px;color:{TEXT_MUTED} !important;padding:8px;text-align:center; }}
    .settings-box {{
        background: {SETTINGS_BG}; border: 1px solid {SETTINGS_BDR};
        border-radius: 12px; padding: 12px 14px;
    }}
    .greet-card {{
        background: {GREET_BG}; border: 1px solid {GREET_BDR};
        border-radius: 16px; padding: 20px 24px; margin-bottom: 16px;
        display: flex; align-items: center; gap: 16px;
    }}
    .greet-emoji {{ font-size: 40px; line-height: 1; }}
    .greet-name  {{ font-size: 20px; font-weight: 800; color: {TEXT_PRIMARY} !important; line-height: 1.2; }}
    .greet-sub   {{ font-size: 13px; color: {TEXT_MUTED} !important; margin-top: 3px; }}
    .greet-time  {{ font-size: 12px; color: {TEXT_MUTED} !important; margin-top: 2px; }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
    <div style="padding:20px 4px 6px 4px;">
        <div style="font-size:22px;font-weight:800;">📚 Rekxare Dami</div>
        <div style="font-size:12px;color:{TEXT_MUTED};margin-top:2px;">بو قوتابیان و خوێندەکاران</div>
    </div>
    <div style="height:1px;background:{DIVIDER};margin:12px 0 6px;"></div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-lbl">ئامارێن تە</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-icon">⏱️</div>
            <div class="stat-val">{hours_total}س {mins_total}خ</div>
            <div class="stat-lbl">هەمی دەمی خوێندن</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-val">{st.session_state.completed_sessions}</div>
            <div class="stat-lbl">دانیشتنێن تەواوبوو</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-lbl">زنجیرەیێ خوێندنێ</div>', unsafe_allow_html=True)
    sv = st.session_state.streak
    smsg = ("دەستپێک بکە! 💪" if sv == 0 else
            "ئامادەیی! 🌱"    if sv < 3  else
            "بەردەوام بە! 🔥"  if sv < 7  else
            "تو قەهرەمانێ! 🏆")
    st.markdown(f"""
    <div class="streak-card">
        <div style="font-size:28px;">🔥</div>
        <div>
            <div class="streak-num">{sv}
                <span style="font-size:13px;font-weight:400;color:{TEXT_MUTED};">رۆژ</span>
            </div>
            <div class="streak-sub">{smsg}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-lbl">ئامانجێ ئەمڕۆ</div>', unsafe_allow_html=True)
    gc = "#2196F3" if daily_pct >= 100 else "#4CAF50"
    st.markdown(f"""
    <div class="goal-wrap">
        <div class="goal-header">
            <span class="goal-title">🎯 ئامانجێ ئەمڕۆ</span>
            <span>{daily_done_min} / {daily_goal_min} خ — {daily_pct}%</span>
        </div>
        <div class="goal-track">
            <div class="goal-fill" style="width:{daily_pct}%;background:{gc};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-lbl">دوماهيك دەرس</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding:2px 0 8px;"><span class="subject-tag">📖 {st.session_state.last_subject}</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-lbl">دوماهيك چالاکی</div>', unsafe_allow_html=True)
    hist = st.session_state.study_history[-4:][::-1]
    if hist:
        rows = "".join(f'<div class="act-item"><div class="act-dot"></div><span>{e}</span></div>' for e in hist)
        st.markdown(f'<div class="act-list">{rows}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="act-list"><div class="act-empty">هێش چالاکیێ نینە</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-lbl">ڕێکخستن</div>', unsafe_allow_html=True)
    st.markdown('<div class="settings-box">', unsafe_allow_html=True)
    goal_mins = st.slider("🎯 ئامانجێ ئەمڕۆ (خ)", 30, 480,
                          st.session_state.daily_goal_seconds // 60, step=15)
    if goal_mins * 60 != st.session_state.daily_goal_seconds:
        st.session_state.daily_goal_seconds = goal_mins * 60
        save_data()
        st.rerun()
    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)
    dc, tc = st.columns([3, 1])
    with dc:
        st.markdown('<div style="font-size:13px;padding-top:6px;">🌙 دەم شەڤ</div>', unsafe_allow_html=True)
    with tc:
        dark_btn = st.checkbox("", value=is_dark, label_visibility="collapsed")
    if dark_btn != is_dark:
        st.session_state.dark_mode = dark_btn
        save_data()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
    if st.button("🧹 ئاماران پاک بکە", use_container_width=True):
        for k, v in [("total_study_seconds",0),("completed_sessions",0),
                     ("last_subject","—"),("study_history",[]),
                     ("streak",0),("daily_seconds",0),("last_study_date","")]:
            st.session_state[k] = v
        save_data()
        st.rerun()

# ── Main page ──────────────────────────────────────────────────────────────────
nav = st.text_input("ناڤێ خوە بنڤیسە:", "قوتابی", label_visibility="collapsed")

kurd_greet, eng_greet = get_greeting()
h_now = datetime.now().hour
greet_emoji = ("🌅" if 5 <= h_now < 12 else "☀️" if 12 <= h_now < 17
               else "🌆" if 17 <= h_now < 21 else "🌙")
now_str = datetime.now().strftime("%A, %d %B %Y  •  %H:%M")

st.markdown(f"""
<div class="greet-card">
    <div class="greet-emoji">{greet_emoji}</div>
    <div>
        <div class="greet-name">{kurd_greet}، {nav}!</div>
        <div class="greet-sub">{eng_greet} — بخێر هاتێ بۆ Rekxare Dami 📚</div>
        <div class="greet-time">{now_str}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

ders = st.selectbox("تو كيژ دەرسێ دخوینی؟",
    ["🧮 بیرکاری", "⚛️ فیزیا", "🧪 کیمیا", "🇬🇧 ئینگلیزی",
     "🧬 زیندەوەرزانی", "📜 مێژوو", "🌍 جوگرافیا", "💻 کۆمپیوتەر", "☪️ ئايين"])
arc_color = subject_color(ders)

deqe = st.slider("چەند دەقیقە؟", 1, 240, 25)
total_seconds = deqe * 60

col1, col2, col3 = st.columns(3)
with col1:
    if not st.session_state.timer_running and not st.session_state.paused:
        dest_pe_bike = st.button("🚀 دەست پێ بکە", use_container_width=True)
    elif st.session_state.paused:
        resume = st.button("▶️ بەردەوام بە", use_container_width=True)
    else:
        st.button("🚀 دەست پێ بکە", disabled=True, use_container_width=True)
with col2:
    if st.session_state.timer_running:
        stop_timer = st.button("⏸️ راوەستاندن", use_container_width=True)
    else:
        st.button("⏸️ راوەستاندن", disabled=True, use_container_width=True)
with col3:
    dubare = st.button("🔄 دووبارە", use_container_width=True)

hezt = [
    "بەردەوام بە!", "تو دێ سەرکەڤێ!", "ئەڤ چەندە باشە!",
    "بەرێ خوە بدە ئارمانجان!",
    "You've got this! 💪", "Every minute counts! ⏱️",
    "Stay focused, stay strong! 🔥", "Small steps lead to big results! 🌱",
    "Knowledge is power — keep going! ⚡", "You're building your future right now! 🏆",
    "Consistency beats perfection! ✅", "One session at a time! 📖",
    "Push through — the results are worth it! 🌟",
    "Champions are made in moments like this! 🥇",
    "Your future self will thank you! 🚀",
]

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
    glow = f"filter:drop-shadow(0 0 8px {color}99);" if progress > 0 else ""
    st.markdown(f"""
    <div class="timer-card">
        <div style="display:flex;justify-content:center;">
            <svg width="260" height="260" viewBox="0 0 36 36" style="{glow}">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831
                         a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{TIMER_TRACK}" stroke-width="2.5"/>
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831
                         a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{color}" stroke-width="2.5"
                      stroke-linecap="round" stroke-dasharray="{dash:.2f}, 200"/>
                <text x="18" y="17.5" text-anchor="middle"
                      fill="{TIMER_TEXT}" font-size="6.5" font-weight="700">
                    {mins_val:02d}:{secs_val:02d}
                </text>
                <text x="18" y="22.5" text-anchor="middle"
                      fill="{TIMER_TEXT}88" font-size="2.8">دەقیقە : چرکە</text>
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
        st.success(f"✅ باشە {nav}! تو دێ {deqe} دەقیقان بۆ {ders} تەرخان دکەی.")
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
        st.session_state.study_history.append(f"{now_ts} - {subject_name} ({minutes} خ)")
        save_data()
        components.html(""
        <script>
        (function(){
            var AC = window.AudioContext || window.webkitAudioContext;
            var ctx = new AC();
            function note(f
