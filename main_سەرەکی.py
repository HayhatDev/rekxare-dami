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

# ── Subject → accent colour map ───────────────────────────────────────────────
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

def subject_color(ders_label: str) -> str:
    for key, col in SUBJECT_COLORS.items():
        if key in ders_label:
            return col
    return "#4CAF50"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            st.session_state.total_study_seconds  = data.get("total_seconds", 0)
            st.session_state.completed_sessions   = data.get("sessions", 0)
            st.session_state.last_subject         = data.get("last_subject", "—")
            st.session_state.study_history        = data.get("history", [])
            st.session_state.dark_mode            = data.get("dark_mode", False)
            st.session_state.streak               = data.get("streak", 0)
            st.session_state.last_study_date      = data.get("last_study_date", "")
            st.session_state.daily_seconds        = data.get("daily_seconds", 0)
            st.session_state.daily_goal_seconds   = data.get("daily_goal_seconds", 7200)

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

for key, default in [
    ("total_study_seconds", 0),
    ("completed_sessions",  0),
    ("last_subject",        "—"),
    ("study_history",       []),
    ("dark_mode",           False),
    ("streak",              0),
    ("last_study_date",     ""),
    ("daily_seconds",       0),
    ("daily_goal_seconds",  7200),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# Daily reset
today_str = date.today().isoformat()
if st.session_state.last_study_date and st.session_state.last_study_date != today_str:
    if st.session_state.daily_seconds > 0:
        st.session_state.daily_seconds = 0
        save_data()

# Derived display values
total_minutes = st.session_state.total_study_seconds // 60
hours_total   = total_minutes // 60
mins_total    = total_minutes % 60
is_dark       = st.session_state.dark_mode

daily_pct      = min(100, int(st.session_state.daily_seconds / max(1, st.session_state.daily_goal_seconds) * 100))
daily_done_min = st.session_state.daily_seconds // 60
daily_goal_min = st.session_state.daily_goal_seconds // 60

# Colour tokens
if is_dark:
    sb_bg          = "#16213e"
    card_bg        = "rgba(255,255,255,0.05)"
    card_border    = "rgba(255,255,255,0.08)"
    text_primary   = "#e0e0e0"
    text_muted     = "#8a8fa8"
    section_label  = "#6b7280"
    tag_bg         = "rgba(76,175,80,0.18)"
    tag_color      = "#81c784"
    activity_bg    = "rgba(255,255,255,0.04)"
    settings_bg    = "rgba(255,255,255,0.04)"
    settings_bdr   = "rgba(255,255,255,0.07)"
    app_bg         = "#1a1a2e"
    input_bg       = "#2d2d44"
    btn_bg         = "#2d2d44"
    btn_color      = "#e0e0e0"
    btn_border     = "#555"
    timer_track    = "#2d2d44"
    timer_text     = "#ffffff"
    timer_card_bg  = "rgba(255,255,255,0.04)"
    timer_card_bdr = "rgba(255,255,255,0.08)"
    prog_track     = "rgba(255,255,255,0.08)"
else:
    sb_bg          = "#f8fafc"
    card_bg        = "#ffffff"
    card_border    = "#e8edf3"
    text_primary   = "#1a1a2e"
    text_muted     = "#6b7280"
    section_label  = "#9ca3af"
    tag_bg         = "rgba(76,175,80,0.1)"
    tag_color      = "#2e7d32"
    activity_bg    = "#f1f5f9"
    settings_bg    = "#f1f5f9"
    settings_bdr   = "#e2e8f0"
    app_bg         = "#ffffff"
    input_bg       = "#ffffff"
    btn_bg         = "#f0f2f6"
    btn_color      = "#1a1a2e"
    btn_border     = "#d1d5db"
    timer_track    = "#e8eaf0"
    timer_text     = "#1a1a2e"
    timer_card_bg  = "rgba(76,175,80,0.05)"
    timer_card_bdr = "rgba(76,175,80,0.15)"
    prog_track     = "#e8eaf0"

st.markdown(f"""
<style>
    [data-testid="stSidebar"]  {{ background-color: {sb_bg}  !important; }}
    .stApp                     {{ background-color: {app_bg} !important; }}
    .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label,
    [data-testid="stSidebar"] * {{ color: {text_primary} !important; }}
    .stTextInput input, .stSelectbox > div > div {{
        background-color: {input_bg} !important;
        border-radius: 10px !important;
        border: 1px solid {card_border} !important;
    }}
    .stButton > button {{
        border-radius: 10px !important;
        font-weight: 600 !important;
        background-color: {btn_bg} !important;
        color: {btn_color} !important;
        border: 1px solid {btn_border} !important;
        transition: opacity 0.18s ease !important;
    }}
    .stButton > button:hover:not(:disabled) {{ opacity: 0.78 !important; }}
    .timer-card {{
        background: {timer_card_bg};
        border: 1px solid {timer_card_bdr};
        border-radius: 20px;
        padding: 24px 16px 16px;
        margin: 16px 0;
        text-align: center;
    }}
    div[data-testid="metric-container"] {{ display: none !important; }}
    .sb-section-label {{
        font-size: 10px; font-weight: 700; letter-spacing: 1.2px;
        text-transform: uppercase; color: {section_label} !important;
        margin: 18px 0 8px 2px;
    }}
    .stat-row  {{ display: flex; gap: 10px; margin-bottom: 4px; }}
    .stat-card {{
        flex: 1; background: {card_bg}; border: 1px solid {card_border};
        border-radius: 12px; padding: 12px 10px; text-align: center;
    }}
    .stat-card .stat-icon  {{ font-size: 18px; margin-bottom: 4px; }}
    .stat-card .stat-value {{ font-size: 17px; font-weight: 700; color: {text_primary} !important; line-height: 1.2; }}
    .stat-card .stat-label {{ font-size: 10px; color: {text_muted} !important; margin-top: 2px; }}
    .streak-card {{
        background: {card_bg}; border: 1px solid {card_border};
        border-radius: 12px; padding: 10px 14px;
        display: flex; align-items: center; gap: 10px; margin-bottom: 4px;
    }}
    .streak-flame {{ font-size: 26px; line-height: 1; }}
    .streak-num   {{ font-size: 22px; font-weight: 800; color: #FF9800 !important; line-height: 1; }}
    .streak-label {{ font-size: 10px; color: {text_muted} !important; margin-top: 1px; }}
    .goal-bar-wrap {{
        background: {card_bg}; border: 1px solid {card_border};
        border-radius: 12px; padding: 11px 14px; margin-bottom: 4px;
    }}
    .goal-bar-header {{
        display: flex; justify-content: space-between;
        font-size: 12px; color: {text_muted} !important; margin-bottom: 7px;
    }}
    .goal-bar-title {{ font-weight: 600; color: {text_primary} !important; }}
    .goal-bar-track {{ background: {prog_track}; border-radius: 99px; height: 8px; overflow: hidden; }}
    .goal-bar-fill  {{ height: 8px; border-radius: 99px; transition: width 0.4s ease; }}
    .subject-tag {{
        display: inline-block; background: {tag_bg}; color: {tag_color} !important;
        border-radius: 20px; padding: 4px 12px; font-size: 13px; font-weight: 600; margin-top: 2px;
    }}
    .activity-list {{ background: {activity_bg}; border-radius: 10px; padding: 6px 4px; }}
    .activity-item {{
        display: flex; align-items: center; gap: 8px;
        padding: 6px 8px; border-radius: 8px; font-size: 12px; color: {text_primary} !important;
    }}
    .activity-item .act-dot {{ width:6px;height:6px;border-radius:50%;background:#4CAF50;flex-shrink:0; }}
    .activity-empty {{ font-size:12px;color:{text_muted} !important;padding:8px;text-align:center; }}
    .settings-box {{
        background: {settings_bg}; border: 1px solid {settings_bdr};
        border-radius: 12px; padding: 12px 14px; margin-top: 4px;
    }}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    st.markdown(f"""
    <div style="padding:20px 4px 4px 4px;">
        <div style="font-size:22px;font-weight:800;color:{text_primary};">📚 Rekxare Dami</div>
        <div style="font-size:12px;color:{text_muted};margin-top:2px;">بو قوتابیان و خوێندەکاران</div>
    </div>
    <div style="height:1px;background:{card_border};margin:14px 0 6px 0;"></div>
    """, unsafe_allow_html=True)

    # Stats
    st.markdown('<div class="sb-section-label">ئامارێن تە</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-icon">⏱️</div>
            <div class="stat-value">{hours_total}س {mins_total}خ</div>
            <div class="stat-label">هەمی دەمی خوێندن</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-value">{st.session_state.completed_sessions}</div>
            <div class="stat-label">دانیشتنێن تەواوبوو</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 🔥 Streak
    st.markdown('<div class="sb-section-label">زنجیرەیێ خوێندنێ</div>', unsafe_allow_html=True)
    streak_val = st.session_state.streak
    streak_msg = (
        "دەستپێک بکە! 💪" if streak_val == 0 else
        "ئامادەیی! 🌱"    if streak_val < 3 else
        "بەردەوام بە! 🔥"  if streak_val < 7 else
        "تو قەهرەمانێ! 🏆"
    )
    st.markdown(f"""
    <div class="streak-card">
        <div class="streak-flame">🔥</div>
        <div>
            <div class="streak-num">{streak_val} <span style="font-size:13px;font-weight:400;color:{text_muted};">رۆژ</span></div>
            <div class="streak-label">{streak_msg}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 🎯 Daily goal
    st.markdown('<div class="sb-section-label">ئامانجێ ئەمڕۆ</div>', unsafe_allow_html=True)
    goal_fill_color = "#4CAF50" if daily_pct < 100 else "#2196F3"
    st.markdown(f"""
    <div class="goal-bar-wrap">
        <div class="goal-bar-header">
            <span class="goal-bar-title">🎯 ئارمانجێن ئەڤروکە</span>
            <span>{daily_done_min} / {daily_goal_min} خولەک — {daily_pct}%</span>
        </div>
        <div class="goal-bar-track">
            <div class="goal-bar-fill" style="width:{daily_pct}%;background:{goal_fill_color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Last subject
    st.markdown('<div class="sb-section-label">دوماهيك دەرس</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding:2px 0 8px 0;"><span class="subject-tag">📖 {st.session_state.last_subject}</span></div>', unsafe_allow_html=True)

    # Recent activity
    st.markdown('<div class="sb-section-label">دوماهيك چالاکی</div>', unsafe_allow_html=True)
    history = st.session_state.study_history[-4:][::-1]
    if history:
        items_html = "".join([f'<div class="activity-item"><div class="act-dot"></div><span>{e}</span></div>' for e in history])
        st.markdown(f'<div class="activity-list">{items_html}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="activity-list"><div class="activity-empty">هێشتا چالاکی نینە</div></div>', unsafe_allow_html=True)

    # Settings
    st.markdown('<div class="sb-section-label">ڕێکخستن</div>', unsafe_allow_html=True)
    st.markdown('<div class="settings-box">', unsafe_allow_html=True)

    goal_mins = st.slider("🎯 ئارمانجێن ئەڤروکە (خولەک)", 30, 480, st.session_state.daily_goal_seconds // 60, step=15)
    if goal_mins * 60 != st.session_state.daily_goal_seconds:
        st.session_state.daily_goal_seconds = goal_mins * 60
        save_data()
        st.rerun()

    st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)
    dark_col, toggle_col = st.columns([3, 1])
    with dark_col:
        st.markdown('<div style="font-size:13px;padding-top:6px;">🌙 دەم شەڤ</div>', unsafe_allow_html=True)
    with toggle_col:
        dark_btn = st.checkbox("", value=st.session_state.dark_mode, label_visibility="collapsed")
    if dark_btn != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_btn
        save_data()
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

    if st.button("🧹 ئاماران پاک بکە", use_container_width=True):
        for k, v in [("total_study_seconds",0),("completed_sessions",0),("last_subject","—"),
                     ("study_history",[]),("streak",0),("daily_seconds",0),("last_study_date","")]:
            st.session_state[k] = v
        save_data()
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
st.title("📚 Rekxare Dami | بو قوتابیان و خوێندەکاران")

for key, default in [("timer_running",False),("end_time",None),("total_seconds",0),
                     ("paused",False),("remaining_at_pause",0)]:
    if key not in st.session_state:
        st.session_state[key] = default

nav = st.text_input("ناڤێ خوە بنڤیسە:", "قوتابی")
if nav:
    st.write(f"بخێر هاتێ {nav}! 🌟")

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
    "Push through — the results are worth it! 🌟", "Champions are made in moments like this! 🥇",
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
    dash_length = progress * 100.0
    glow = f"filter: drop-shadow(0 0 8px {color}99);" if progress > 0 else ""
    st.markdown(f"""
    <div class="timer-card">
        <div style="display:flex;justify-content:center;">
            <svg width="260" height="260" viewBox="0 0 36 36" style="{glow}">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{timer_track}" stroke-width="2.5"/>
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{color}" stroke-width="2.5"
                      stroke-linecap="round" stroke-dasharray="{dash_length:.2f}, 200"/>
                <text x="18" y="17.5" text-anchor="middle" fill="{timer_text}"
                      font-size="6.5" font-weight="700">{mins_val:02d}:{secs_val:02d}</text>
                <text x="18" y="22.5" text-anchor="middle" fill="{timer_text}88"
                      font-size="2.8">دەقیقە : چرکە</text>
            </svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.timer_running and st.session_state.end_time:
    remaining = st.session_state.end_time - time.time()
    if remaining > 0:
        mins_val, secs_val = divmod(int(remaining), 60)
        progress = min(1.0, 1.0 - (remaining / st.session_state.total_seconds))
        render_circle(mins_val, secs_val, progress, arc_color)
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
        now     = datetime.now().strftime("%H:%M")
        minutes = st.session_state.total_seconds // 60
        st.session_state.study_history.append(f"{now} - {subject_name} ({minutes} خ)")
        save_data()

        components.html("""
        <script>
            (function() {
                var AudioContext = window.AudioContext || window.webkitAudioContext;
                var ctx = new AudioContext();
                function playNote(freq, startDelay, duration) {
                    var osc = ctx.createOscillator();
                    var gain = ctx.createGain();
                    osc.connect(gain);
                    gain.connect(ctx.destination);
                    osc.type = 'sine';
                    osc.frequency.value = freq;
                    var t = ctx.currentTime + startDelay;
                    gain.gain.setValueAtTime(0, t);
                    gain.gain.linearRampToValueAtTime(0.25, t + 0.02);
                    gain.gain.exponentialRampToValueAtTime(0.001, t + duration);
                    osc.start(t);
                    osc.stop(t + duration);
                }
                playNote(659, 0.0, 1.2);
                playNote(830, 0.22, 1.2);
                playNote(988, 0.44, 1.4);
            })();
        </script>
        """, height=0)

        st.balloons()
        st.success("دەمێ تە ب دوماهیک هات! سەرکەفتی بێ 🎉")

elif st.session_state.paused and st.session_state.remaining_at_pause > 0:
    mins_val, secs_val = divmod(int(st.session_state.remaining_at_pause), 60)
    progress = min(1.0, 1.0 - (st.session_state.remaining_at_pause / st.session_state.total_seconds))
    render_circle(mins_val, secs_val, progress, "#FFA500")
    st.warning(f"⏸️ دەم هاتە راوەستاندن. {deqe} دەقیقان بۆ {ders}")

else:
    render_circle(deqe, 0, 0.0, arc_color)
    if st.session_state.total_seconds > 0:
        st.info("🔄 دەم هاتە راوەستاندن. دووبارە دەست پێ بکە.")
