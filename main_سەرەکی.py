import streamlit as st
import time
import random
from datetime import datetime
import json
import os
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Rekxare Dami",
    page_icon="📚",
    initial_sidebar_state="expanded"
)

DATA_FILE = "study_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            st.session_state.total_study_seconds = data.get("total_seconds", 0)
            st.session_state.completed_sessions = data.get("sessions", 0)
            st.session_state.last_subject = data.get("last_subject", "—")
            st.session_state.study_history = data.get("history", [])
            st.session_state.dark_mode = data.get("dark_mode", False)

def save_data():
    data = {
        "total_seconds": st.session_state.total_study_seconds,
        "sessions": st.session_state.completed_sessions,
        "last_subject": st.session_state.last_subject,
        "history": st.session_state.study_history,
        "dark_mode": st.session_state.dark_mode
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if "data_loaded" not in st.session_state:
    load_data()
    st.session_state.data_loaded = True

if "total_study_seconds" not in st.session_state:
    st.session_state.total_study_seconds = 0
if "completed_sessions" not in st.session_state:
    st.session_state.completed_sessions = 0
if "last_subject" not in st.session_state:
    st.session_state.last_subject = "—"
if "study_history" not in st.session_state:
    st.session_state.study_history = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.markdown("""
<style>
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: opacity 0.2s ease !important;
    }
    .stButton > button:hover:not(:disabled) { opacity: 0.85 !important; }
    .stSlider > div { padding-top: 4px; }
    .stSelectbox > div > div { border-radius: 10px !important; }
    .stTextInput > div > div > input { border-radius: 10px !important; }
    div[data-testid="metric-container"] {
        background: rgba(76,175,80,0.08);
        border-radius: 10px;
        padding: 8px 12px;
    }
    .timer-card {
        border-radius: 20px;
        padding: 24px 16px 16px 16px;
        margin: 16px 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("📊 ئامارێن تە")
    st.divider()

    total_minutes = st.session_state.total_study_seconds // 60
    hours = total_minutes // 60
    mins = total_minutes % 60

    col1, col2 = st.columns(2)
    with col1:
        st.metric("⏱️ هەمی دەم", f"{hours} س {mins} خ")
    with col2:
        st.metric("✅ دانیشتن", st.session_state.completed_sessions)

    st.divider()
    st.write(f"📚 دوماهيك دەرس: **{st.session_state.last_subject}**")

    if st.session_state.study_history:
        st.write("**📋 دوماهيك چالاکی:**")
        for entry in st.session_state.study_history[-3:][::-1]:
            st.caption(entry)

    st.divider()
    st.write("🌓 ڕووکار")

    dark_btn = st.checkbox("شەڤ", value=st.session_state.dark_mode)
    if dark_btn != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_btn
        save_data()
        st.rerun()

    st.divider()
    if st.button("🧹 ئاماران پاک بکە", use_container_width=True):
        st.session_state.total_study_seconds = 0
        st.session_state.completed_sessions = 0
        st.session_state.last_subject = "—"
        st.session_state.study_history = []
        save_data()
        st.rerun()

if st.session_state.dark_mode:
    st.markdown("""
    <style>
        .stApp { background-color: #1a1a2e !important; }
        [data-testid="stSidebar"] { background-color: #16213e !important; }
        .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label { color: #e0e0e0 !important; }
        .stTextInput input, .stSelectbox select { background-color: #2d2d44 !important; color: #ffffff !important; border: 1px solid #444 !important; }
        .stButton button { background-color: #2d2d44 !important; color: #e0e0e0 !important; border: 1px solid #555 !important; }
        .timer-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); }
        div[data-testid="metric-container"] { background: rgba(76,175,80,0.12) !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .timer-card { background: rgba(76,175,80,0.05); border: 1px solid rgba(76,175,80,0.15); }
        .stButton button { background-color: #f0f2f6 !important; color: #1a1a2e !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Rekxare Dami | بو قوتابیان و خوێندەکاران")

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "end_time" not in st.session_state:
    st.session_state.end_time = None
if "total_seconds" not in st.session_state:
    st.session_state.total_seconds = 0
if "paused" not in st.session_state:
    st.session_state.paused = False
if "remaining_at_pause" not in st.session_state:
    st.session_state.remaining_at_pause = 0

nav = st.text_input("ناڤێ خوە بنڤیسە:", "قوتابی")
if nav:
    st.write(f"بخێر هاتێ {nav}! 🌟")

st.divider()

ders = st.selectbox("تو كيژ دەرسێ دخوینی؟",
    ["🧮 بیرکاری", "⚛️ فیزیا", "🧪 کیمیا", "🇬🇧 ئینگلیزی",
     "🧬 زیندەوەرزانی", "📜 مێژوو", "🌍 جوگرافیا", "💻 کۆمپیوتەر", "☪️ ئايين"])

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
    elif st.session_state.paused:
        st.button("⏸️ راوەستاندن", disabled=True, use_container_width=True)
    else:
        st.button("⏸️ راوەستاندن", disabled=True, use_container_width=True)

with col3:
    dubare = st.button("🔄 دووبارە", use_container_width=True)

hezt = ["بەردەوام بە!", "تو دێ سەرکەڤێ!", "ئەڤ چەندە باشە!", "بەرێ خوە بدە ئارمانجان!"]

if "dest_pe_bike" in locals() and dest_pe_bike:
    st.session_state.timer_running = True
    st.session_state.paused = False
    st.session_state.end_time = time.time() + total_seconds
    st.session_state.total_seconds = total_seconds
    st.rerun()

if "resume" in locals() and resume:
    st.session_state.timer_running = True
    st.session_state.paused = False
    st.session_state.end_time = time.time() + st.session_state.remaining_at_pause
    st.rerun()

if "stop_timer" in locals() and stop_timer:
    st.session_state.timer_running = False
    st.session_state.paused = True
    st.session_state.remaining_at_pause = max(0, st.session_state.end_time - time.time())
    st.rerun()

if dubare:
    st.session_state.timer_running = False
    st.session_state.paused = False
    st.session_state.end_time = None
    st.session_state.total_seconds = 0
    st.session_state.remaining_at_pause = 0
    st.rerun()

def render_circle(mins_val, secs_val, progress, color):
    dash_length = progress * 100.0
    is_dark = st.session_state.get("dark_mode", False)
    track_color = "#2d2d44" if is_dark else "#e8eaf0"
    text_color = "#ffffff" if is_dark else "#1a1a2e"
    glow = f"filter: drop-shadow(0 0 6px {color}88);" if progress > 0 else ""
    st.markdown(f"""
    <div class="timer-card">
        <div style="display: flex; justify-content: center;">
            <svg width="260" height="260" viewBox="0 0 36 36" style="{glow}">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{track_color}" stroke-width="2.5"/>
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                      fill="none" stroke="{color}" stroke-width="2.5"
                      stroke-linecap="round"
                      stroke-dasharray="{dash_length:.2f}, 200"/>
                <text x="18" y="17.5" text-anchor="middle" fill="{text_color}"
                      font-size="6.5" font-weight="700">{mins_val:02d}:{secs_val:02d}</text>
                <text x="18" y="22.5" text-anchor="middle" fill="{text_color}88"
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
        render_circle(mins_val, secs_val, progress, "#4CAF50")
        st.success(f"✅ باشە {nav}! تو دێ {deqe} دەقیقان بۆ {ders} تەرخان دکەی.")
        st.info(f"💬 {random.choice(hezt)}")
        time.sleep(1)
        st.rerun()

    else:
        st.session_state.timer_running = False
        st.session_state.paused = False
        st.session_state.total_study_seconds += st.session_state.total_seconds
        st.session_state.completed_sessions += 1
        subject_name = ders.split(" ", 1)[1] if " " in ders else ders
        st.session_state.last_subject = subject_name
        now = datetime.now().strftime("%H:%M")
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
    render_circle(deqe, 0, 0.0, "#4CAF50")
    if st.session_state.total_seconds > 0:
        st.info("🔄 دەم هاتە راوەستاندن. دووبارە دەست پێ بکە.")
