import streamlit as st
from datetime import datetime, time as dtime, date, timedelta
import json
import os

# ── Translations first
with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)


# --- PWA Manifest 
st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js');
    }
</script>
""", unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state.lang = "badini"

def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

# ── set_page_config
st.set_page_config(
    page_title=t("schedule_title"),
    page_icon="📅",
    layout="centered"
)

st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js');
    }
</script>
""", unsafe_allow_html=True)

# ── Constants 
DAYS = [
    ("sun", "☀️ ئێکشەمب", "Sunday"),
    ("mon", "📖 دووشەمب", "Monday"),
    ("tue", "📖 سێشەمب", "Tuesday"),
    ("wed", "📖 چارشەمب", "Wednesday"),
    ("thu", "📖 پێنجشەمب", "Thursday"),
    ("fri", "🕌 خودبە",   "Friday"),
    ("sat", "🎉 شەمبی",   "Saturday"),
]
DAY_EMOJIS = {
    "sun": "☀️", "mon": "📖", "tue": "📖",
    "wed": "📖", "thu": "📖", "fri": "🕌", "sat": "🎉"
}
SCHEDULE_FILE = "schedule_data.json"

# ── Helpers
def get_day_name(day_key):
    for dk, badini_name, eng_name in DAYS:
        if dk == day_key:
            if st.session_state.lang == "badini":
                return badini_name
            elif st.session_state.lang == "arabic":
                ar = {
                    "sun": "☀️ الأحد",     "mon": "📖 الاثنين",  "tue": "📖 الثلاثاء",
                    "wed": "📖 الأربعاء",   "thu": "📖 الخميس",
                    "fri": "🕌 الجمعة",    "sat": "🎉 السبت",
                }
                return ar.get(day_key, eng_name)
            else:
                return f"{DAY_EMOJIS.get(day_key, '📖')} {eng_name}"
    return day_key

def get_time_label():
    if st.session_state.lang == "badini":
        return "دەستپێک", "دووماهی"
    if st.session_state.lang == "arabic":
        return "بداية", "نهاية"
    return "Start", "End"

def get_column_labels():
    if st.session_state.lang == "badini":
        return "دەم", "چالاکی"
    if st.session_state.lang == "arabic":
        return "الوقت", "المهمة"
    return "Time", "Task"

def parse_time(s):
    try:
        dt = datetime.strptime(s, "%H:%M")
        return (dt.hour, dt.minute)
    except Exception:
        return (0, 0)

def format_duration(start_str, end_str):
    try:
        s    = datetime.strptime(start_str, "%H:%M")
        e    = datetime.strptime(end_str,   "%H:%M")
        diff = int((e - s).total_seconds() // 60)
        if diff <= 0:
            return ""
        if diff < 60:
            return f"{diff}m"
        h, m = divmod(diff, 60)
        return f"{h}h {m}m" if m else f"{h}h"
    except Exception:
        return ""

def total_day_minutes(day_entries):
    """Sum durations of all named tasks for a day."""
    total = 0
    for e in day_entries:
        if not e.get("task", "").strip():
            continue
        try:
            s = datetime.strptime(e.get("start", "00:00"), "%H:%M")
            end = datetime.strptime(e.get("end",   "00:00"), "%H:%M")
            diff = int((end - s).total_seconds() // 60)
            if diff > 0:
                total += diff
        except Exception:
            pass
    return total

def fmt_minutes(mins):
    if mins <= 0:
        return ""
    if mins < 60:
        return f"{mins}m"
    h, m = divmod(mins, 60)
    return f"{h}h {m}m" if m else f"{h}h"

def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "dark_mode" in data:
            st.session_state.dark_mode = data["dark_mode"]
        return data.get("schedule", None)
    return None

def save_schedule():
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "schedule":  st.session_state.schedule,
            "dark_mode": st.session_state.dark_mode,
        }, f, ensure_ascii=False, indent=2)

def copy_week_to_next():
    """نسخ مهام الأسبوع الحالي إلى الأسبوع القادم مع إعادة تعيين done=False."""
    today = datetime.now().weekday()
    days_until_sunday = (6 - today) % 7
    if days_until_sunday == 0:
        days_until_sunday = 7
    
    next_sunday = date.today() + timedelta(days=days_until_sunday)
    week_number = next_sunday.strftime("%Y-%W")
    
    new_schedule = {dk: [] for dk, _, _ in DAYS}
    
    for dk, _, _ in DAYS:
        for task in st.session_state.schedule.get(dk, []):
            new_task = task.copy()
            new_task["done"] = False
            new_schedule[dk].append(new_task)
    
    st.session_state.schedule = new_schedule
    st.session_state.active_day = today_key
    save_schedule()
    
# ── Session-state init
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "schedule" not in st.session_state:
    loaded = load_schedule()
    base   = {dk: [] for dk, _, _ in DAYS}
    if loaded:
        base.update(loaded)
    st.session_state.schedule = base

for dk, _, _ in DAYS:
    if dk not in st.session_state.schedule:
        st.session_state.schedule[dk] = []
    if f"{dk}_reset" not in st.session_state:
        st.session_state[f"{dk}_reset"] = 0
    if f"{dk}_clear_confirm" not in st.session_state:
        st.session_state[f"{dk}_clear_confirm"] = False

today_map = {6: "sun", 0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat"}
today_key = today_map[datetime.now().weekday()]
is_dark   = st.session_state.dark_mode

# ── Theme tokens 
if is_dark:
    APP_BG        = "#1a1a2e"
    SB_BG         = "#16213e"
    INPUT_BG      = "#252542"
    CARD_BG       = "rgba(255,255,255,0.05)"
    CARD_BORDER   = "rgba(255,255,255,0.09)"
    TEXT_PRIMARY  = "#e2e2e2"
    TEXT_MUTED    = "#8a8fa8"
    BTN_BG        = "#252542"
    BTN_COLOR     = "#e2e2e2"
    BTN_BORDER    = "#3a3a5c"
    PROG_TRACK    = "rgba(255,255,255,0.12)"
    DIVIDER       = "rgba(255,255,255,0.08)"
    TODAY_BG      = "rgba(76,175,80,0.15)"
    TODAY_COLOR   = "#81c784"
    OVERVIEW_BG   = "rgba(255,255,255,0.04)"
    OVERVIEW_BDR  = "rgba(255,255,255,0.09)"
    DURATION_CLR  = "#8a8fa8"
    EMPTY_CLR     = "#555c72"
    PILL_BG       = "rgba(76,175,80,0.15)"
    PILL_COLOR    = "#81c784"
    PILL_BORDER   = "rgba(76,175,80,0.25)"
    TASK_ROW_BG   = "rgba(255,255,255,0.03)"
    TASK_ROW_DONE = "rgba(76,175,80,0.07)"
    TOTAL_BG      = "rgba(33,150,243,0.12)"
    TOTAL_COLOR   = "#64b5f6"
    TOTAL_BDR     = "rgba(33,150,243,0.25)"
else:
    APP_BG        = "#e8edf5"
    SB_BG         = "#f4f7fb"
    INPUT_BG      = "#ffffff"
    CARD_BG       = "#ffffff"
    CARD_BORDER   = "#dde3ed"
    TEXT_PRIMARY  = "#1a1a2e"
    TEXT_MUTED    = "#6b7280"
    BTN_BG        = "#dde5f0"
    BTN_COLOR     = "#1a1a2e"
    BTN_BORDER    = "#c0cce0"
    PROG_TRACK    = "#dde3ed"
    DIVIDER       = "#dde3ed"
    TODAY_BG      = "rgba(76,175,80,0.10)"
    TODAY_COLOR   = "#2e7d32"
    OVERVIEW_BG   = "#ffffff"
    OVERVIEW_BDR  = "#dde3ed"
    DURATION_CLR  = "#9ca3af"
    EMPTY_CLR     = "#9ca3af"
    PILL_BG       = "rgba(76,175,80,0.08)"
    PILL_COLOR    = "#2e7d32"
    PILL_BORDER   = "rgba(76,175,80,0.20)"
    TASK_ROW_BG   = "#f9fafb"
    TASK_ROW_DONE = "rgba(76,175,80,0.06)"
    TOTAL_BG      = "rgba(33,150,243,0.07)"
    TOTAL_COLOR   = "#1565c0"
    TOTAL_BDR     = "rgba(33,150,243,0.18)"

# ── CSS 
st.markdown(f"""
<style>
*, *::before, *::after {{ box-sizing: border-box; }}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"],
section[data-testid="stMain"],
.main .block-container      {{ background-color: {APP_BG} !important; }}
[data-testid="stSidebar"]   {{ background-color: {SB_BG} !important; }}
.stApp *, [data-testid="stSidebar"] * {{ color: {TEXT_PRIMARY} !important; }}

.stTextInput input,
.stTimeInput input {{
    background-color: {INPUT_BG} !important;
    border: 1px solid {CARD_BORDER} !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    padding: 6px 8px !important;
}}
.stTextInput input:focus   {{ border-color: #4CAF50 !important; box-shadow: 0 0 0 2px rgba(76,175,80,0.15) !important; }}
.stTextInput input:disabled {{
    text-decoration: line-through !important;
    opacity: 0.50 !important;
}}

[data-testid="stCheckbox"] svg {{ stroke: #4CAF50 !important; }}
[data-testid="stCheckbox"]     {{ margin-top: 8px !important; }}

.stButton > button {{
    background-color: {BTN_BG} !important;
    color:            {BTN_COLOR} !important;
    border:           1px solid {BTN_BORDER} !important;
    border-radius:    10px !important;
    font-weight:      600 !important;
    font-size:        13px !important;
    transition:       all 0.18s ease !important;
    padding:          6px 8px !important;
}}
.stButton > button:hover:not(:disabled) {{
    opacity: 0.80 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.10) !important;
}}
.stButton > button:disabled {{ opacity: 0.28 !important; }}

/* Delete button — 4th column */
[data-testid="column"]:nth-child(4) .stButton > button {{
    background: transparent !important;
    color: #ef5350 !important;
    border-color: transparent !important;
    font-size: 16px !important;
    padding: 6px 8px !important;
}}
[data-testid="column"]:nth-child(4) .stButton > button:hover {{
    background: rgba(239,83,80,0.10) !important;
    border-color: #ef5350 !important;
}}

/* ── Action row buttons via anchor — zero wrapper divs ── */
.action-row-anchor {{ display: none !important; }}

.element-container:has(.action-row-anchor) + div
    [data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton > button {{
    background: linear-gradient(135deg,#43a047,#66bb6a) !important;
    color: #fff !important; border-color: #388e3c !important;
    font-size: 13px !important; padding: 9px 8px !important;
    box-shadow: 0 2px 8px rgba(67,160,71,0.30) !important;
}}
.element-container:has(.action-row-anchor) + div
    [data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton > button:not(:disabled) {{
    background: linear-gradient(135deg,#1565c0,#1e88e5) !important;
    color: #fff !important; border-color: #0d47a1 !important;
    font-size: 12px !important;
    box-shadow: 0 2px 8px rgba(21,101,192,0.25) !important;
}}
.element-container:has(.action-row-anchor) + div
    [data-testid="stHorizontalBlock"] > div:nth-child(3) .stButton > button {{
    background: linear-gradient(135deg,#43a047,#66bb6a) !important;
    color: #fff !important; border-color: #388e3c !important;
    font-size: 12px !important; padding: 9px 8px !important;
    box-shadow: 0 2px 8px rgba(67,160,71,0.30) !important;
}}
.element-container:has(.action-row-anchor) + div
    [data-testid="stHorizontalBlock"] > div:nth-child(4) .stButton > button {{
    background: transparent !important;
    color: #ef5350 !important;
    border-color: #ef535044 !important;
    font-size: 12px !important;
}}
.element-container:has(.action-row-anchor) + div
    [data-testid="stHorizontalBlock"] > div:nth-child(4) .stButton > button:hover {{
    background: rgba(239,83,80,0.10) !important;
    border-color: #ef5350 !important;
}}

/* ── Confirm row — YES button red ── */
.confirm-row-anchor {{ display: none !important; }}
.element-container:has(.confirm-row-anchor) + div
    [data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton > button {{
    background: linear-gradient(135deg,#c62828,#ef5350) !important;
    color: #fff !important; border-color: #b71c1c !important;
}}

/* ── Live time-range pill (replaces old st.caption) ── */
.time-pill {{
    display: inline-flex; align-items: center; gap: 4px;
    background: {PILL_BG};
    color: {PILL_COLOR} !important;
    border: 1px solid {PILL_BORDER};
    font-size: 11px; font-weight: 700;
    padding: 3px 8px; border-radius: 20px;
    margin-bottom: 4px; white-space: nowrap;
    font-variant-numeric: tabular-nums;
}}

/* ── Duration badge ── */
.duration-badge {{
    font-size: 10px; color: {DURATION_CLR} !important;
    display: block; text-align: center; margin-top: 3px;
    font-weight: 600;
}}

/* ── Per-day total time strip ── */
.day-total-strip {{
    display: flex; align-items: center; justify-content: space-between;
    background: {TOTAL_BG};
    border: 1px solid {TOTAL_BDR};
    border-radius: 10px; padding: 7px 12px; margin-bottom: 14px;
    font-size: 12px; font-weight: 600;
    color: {TOTAL_COLOR} !important;
}}
.day-total-strip span {{ color: {TOTAL_COLOR} !important; }}

/* ── Week overview card ── */
.week-card {{
    background: {OVERVIEW_BG};
    border: 1px solid {OVERVIEW_BDR};
    border-radius: 16px;
    padding: 14px 16px 12px;
    margin-bottom: 20px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.04);
}}
.week-card-title {{
    font-size: 11px; font-weight: 700; letter-spacing: 0.8px;
    text-transform: uppercase; color: {TEXT_MUTED} !important;
    margin-bottom: 10px;
}}

[data-testid="stProgressBar"] p {{ display: none !important; }}
[data-testid="stProgressBar"] > div {{ height: 5px !important; border-radius: 99px !important; }}

/* ── Today badge ── */
.today-badge {{
    display: inline-flex; align-items: center; gap: 6px;
    background: {TODAY_BG}; color: {TODAY_COLOR} !important;
    border: 1px solid {TODAY_COLOR}44;
    font-size: 12px; font-weight: 700;
    padding: 5px 14px; border-radius: 20px; margin-bottom: 14px;
}}
.today-badge span {{ color: {TODAY_COLOR} !important; }}

/* ── Progress bar (per-day) ── */
.prog-wrap   {{ margin-bottom: 16px; }}
.prog-header {{ display: flex; justify-content: space-between; align-items: center; font-size: 12px; margin-bottom: 6px; }}
.prog-label  {{ font-weight: 600; color: {TEXT_PRIMARY} !important; }}
.prog-pct    {{ color: {TEXT_MUTED} !important; font-variant-numeric: tabular-nums; }}
.prog-track  {{ background: {PROG_TRACK}; border-radius: 99px; height: 8px; overflow: hidden; }}
.prog-fill   {{ height: 8px; border-radius: 99px; transition: width 0.4s ease; }}

/* ── All-done banner ── */
.all-done-banner {{
    background: rgba(76,175,80,0.12);
    border: 1px solid rgba(76,175,80,0.35);
    border-radius: 12px; padding: 14px 16px; text-align: center;
    font-size: 15px; font-weight: 700;
    color: #4CAF50 !important; margin-bottom: 14px;
    letter-spacing: 0.2px;
}}

/* ── Empty state ── */
.empty-day      {{ text-align: center; padding: 36px 16px; color: {EMPTY_CLR} !important; font-size: 13px; }}
.empty-day-icon {{ font-size: 40px; margin-bottom: 10px; }}
.empty-day-hint {{ font-size: 11px; margin-top: 6px; opacity: 0.7; }}

/* ── Danger confirm ── */
.danger-confirm {{
    background: rgba(239,83,80,0.10);
    border: 1px solid rgba(239,83,80,0.30);
    border-radius: 10px; padding: 10px 14px;
    font-size: 12px; font-weight: 600;
    color: #ef5350 !important; text-align: center; margin-bottom: 8px;
}}

hr {{ border-color: {DIVIDER} !important; margin: 16px 0 !important; }}

[data-testid="stTabs"] [data-baseweb="tab"] {{
    font-size: 11px !important; font-weight: 600 !important;
    border-radius: 8px 8px 0 0 !important; padding: 7px 9px !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    color: #4CAF50 !important;
    border-bottom-color: #4CAF50 !important;
}}

/* ── Column header captions ── */
.col-header {{
    font-size: 10px; font-weight: 700; letter-spacing: 0.7px;
    text-transform: uppercase; color: {TEXT_MUTED} !important;
    padding-bottom: 4px;
}}
.col-header span {{ color: {TEXT_MUTED} !important; }}

@media (max-width: 640px) {{
    .stTimeInput input {{ font-size: 12px !important; }}
    .stTextInput input {{ font-size: 12px !important; }}
    .time-pill {{ font-size: 10px !important; padding: 2px 6px !important; }}
}}
</style>
""", unsafe_allow_html=True)

# ── Page header 
_, dm_col = st.columns([8, 1])
with dm_col:
    dark_toggle = st.checkbox(
        "🌙", value=is_dark, key="dm_toggle_sched",
        help="Dark mode" if st.session_state.lang == "english" else ""
    )
    if dark_toggle != is_dark:
        st.session_state.dark_mode = dark_toggle
        save_schedule()
        st.rerun()

st.markdown(f"""
<div style="padding:0 0 16px;">
    <div style="font-size:26px;font-weight:900;letter-spacing:-0.5px;">
        📅 {t("schedule_title")}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Week overview
_weekly_title = {
    "badini":  "📊 پێشکەفتنا حەفتیانە",
    "english": "📊 Weekly Overview",
    "arabic":  "📊 التقدم الأسبوعي",
}.get(st.session_state.lang, "📊 Weekly Overview")

st.markdown('<div class="week-card">', unsafe_allow_html=True)
st.markdown(f'<div class="week-card-title">{_weekly_title}</div>', unsafe_allow_html=True)

# ── نسخ الأسبوع 
st.divider()
copy_lbl = {
    "badini": "📋 کوپی بکە بو حەفتیا دهێت",
    "english": "📋 Copy to Next Week",
    "arabic": "📋 نسخ إلى الأسبوع القادم",
}.get(st.session_state.lang, "📋 Copy to Next Week")

if st.button(copy_lbl, use_container_width=True):
    copy_week_to_next()
    st.success({
        "badini": "✅ حەفتی هاتە کۆپیکرن!",
        "english": "✅ Week copied successfully!",
        "arabic": "✅ تم نسخ الأسبوع بنجاح!",
    }.get(st.session_state.lang, "✅ Week copied!"))
    st.rerun()
    
week_cols = st.columns(7)
for col, (dk, _, eng) in zip(week_cols, DAYS):
    tasks      = st.session_state.schedule.get(dk, [])
    named      = [tk for tk in tasks if tk.get("task", "").strip()]
    total      = len(named)
    done       = sum(1 for tk in named if tk.get("done", False))
    pct        = done / total if total > 0 else 0.0
    is_today_d = dk == today_key
    short      = eng[:3].upper()
    count      = f"{done}/{total}" if total else "—"
    day_mins   = total_day_minutes(tasks)
    time_lbl   = fmt_minutes(day_mins) if day_mins else ""
    with col:
        dot_html = (
            "<div style='text-align:center;font-size:9px;color:#4CAF50;margin-bottom:1px;'>●</div>"
            if is_today_d else
            "<div style='height:13px;'></div>"
        )
        st.markdown(dot_html, unsafe_allow_html=True)
        day_color = "#4CAF50" if is_today_d else TEXT_MUTED
        st.markdown(
            f"<div style='text-align:center;font-size:10px;font-weight:700;"
            f"color:{day_color};margin-bottom:2px;'>{short}</div>",
            unsafe_allow_html=True
        )
        st.progress(pct)
        st.markdown(
            f"<div style='text-align:center;font-size:10px;color:{TEXT_MUTED};"
            f"margin-top:-4px;line-height:1.4;'>{count}</div>",
            unsafe_allow_html=True
        )
        if time_lbl:
            st.markdown(
                f"<div style='text-align:center;font-size:9px;color:{TEXT_MUTED};"
                f"opacity:0.75;'>{time_lbl}</div>",
                unsafe_allow_html=True
            )

st.markdown('</div>', unsafe_allow_html=True)

# ── Label helpers
time_start_label, time_end_label = get_time_label()
col_time_label, col_task_label   = get_column_labels()

def get_tab_label(day_key):
    day_name = get_day_name(day_key)
    tasks    = [tk for tk in st.session_state.schedule.get(day_key, [])
                if tk.get("task", "").strip()]
    if not tasks:
        return day_name
    done  = sum(1 for tk in tasks if tk.get("done", False))
    total = len(tasks)
    badge = " ✅" if done == total else f" {done}/{total}"
    dot   = " 🔵" if day_key == today_key else ""
    return f"{day_name}{dot}{badge}"

# ── AI Scheduler 
ai_lbl = {
    "badini": "🤖 ڕێکخستنی زیرەک ب AI",
    "english": "🤖 AI Smart Scheduler",
    "arabic": "🤖 الجدولة الذكية بالذكاء الاصطناعي",
}.get(st.session_state.lang, "🤖 AI Smart Scheduler")

if "ai_input" not in st.session_state:
    st.session_state.ai_input = ""
if "ai_loading" not in st.session_state:
    st.session_state.ai_loading = False

with st.expander(ai_lbl, expanded=False):
    st.markdown({
        "badini": "ئامانجێن خوە بنڤیسە (ب زمانێ ئینگلیزی باشترین کار دکەت):",
        "english": "Describe your study goals (English works best):",
        "arabic": "اكتب أهدافك الدراسية (الإنجليزية تعمل بشكل أفضل):",
    }.get(st.session_state.lang, "Describe your study goals:"))
    
    user_goal = st.text_area(
        "Goal",
        value=st.session_state.ai_input,
        placeholder="e.g., I need to study math for 10 hours, physics for 5 hours this week. I prefer mornings.",
        label_visibility="collapsed",
        key="ai_goal_input"
    )
    st.session_state.ai_input = user_goal
    
    if st.button("🚀 " + {
        "badini": "دروست بکە",
        "english": "Generate Schedule",
        "arabic": "توليد الجدول",
    }.get(st.session_state.lang, "Generate Schedule"), use_container_width=True, disabled=st.session_state.ai_loading):
        if not user_goal.strip():
            st.error({
                "badini": "تکایە ئامانجێن خوە بنڤیسە.",
                "english": "Please enter your goals.",
                "arabic": "يرجى كتابة أهدافك.",
            }.get(st.session_state.lang, "Please enter your goals."))
        else:
            st.session_state.ai_loading = True
            st.rerun()

# تنفيذ الطلب إذا كان التحميل مفعلاً
if st.session_state.ai_loading and st.session_state.ai_input:
    import requests
    
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("🚨 Groq API key is missing. Add it to Streamlit secrets.")
        st.session_state.ai_loading = False
        st.stop()
    
    # إعداد الرسالة للذكاء الاصطناعي
    today = datetime.now().strftime("%A")
    prompt = f"""
You are a study schedule generator. The user has the following study goals for the upcoming week (starting today, {today}):

{st.session_state.ai_input}

Please create a day-by-day study schedule for the next 7 days. 
Return ONLY a valid JSON object with the following structure, and no other text before or after the JSON:
{{
  "mon": [{{"start": "HH:MM", "end": "HH:MM", "task": "Subject"}}, ...],
  "tue": [...],
  "wed": [...],
  "thu": [...],
  "fri": [...],
  "sat": [...],
  "sun": [...]
}}
Fill only the days that are relevant. Use 24-hour format for times. Distribute the study hours according to the user's preferences (e.g., mornings, afternoons). Include breaks if necessary.
"""
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        # محاولة تنظيف الرد
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()
        
        new_schedule = json.loads(content)
        
        # التحقق من أن المفاتيح صحيحة
        valid_keys = {"sun", "mon", "tue", "wed", "thu", "fri", "sat"}
        for day_key in valid_keys:
            if day_key in new_schedule and isinstance(new_schedule[day_key], list):
                st.session_state.schedule[day_key] = []
                for task in new_schedule[day_key]:
                    # تأكد من وجود الحقول المطلوبة
                    start = task.get("start", "08:00")
                    end = task.get("end", "09:00")
                    task_name = task.get("task", "Study")
                    st.session_state.schedule[day_key].append({
                        "start": start,
                        "end": end,
                        "task": task_name,
                        "done": False
                    })
        
        save_schedule()
        st.success({
            "badini": "✅ خشتە ب سەرکەفتی دروست بوو!",
            "english": "✅ Schedule generated successfully!",
            "arabic": "✅ تم إنشاء الجدول بنجاح!",
        }.get(st.session_state.lang, "✅ Schedule generated!"))
        
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Network error: {str(e)}")
    except json.JSONDecodeError:
        st.error("🚨 The AI returned an invalid format. Please try again.")
        st.code(content, language="json")
    except Exception as e:
        st.error(f"🚨 Unexpected error: {str(e)}")
    
    st.session_state.ai_loading = False
    st.session_state.ai_input = ""
    st.rerun()
    
# --- اختيار اليوم عبر Radio (يحافظ على الاختيار بعد rerun) 
if "active_day" not in st.session_state:
    st.session_state.active_day = today_key

day_labels = [get_tab_label(dk) for dk, _, _ in DAYS]
day_keys   = [dk for dk, _, _ in DAYS]

active_index = day_keys.index(st.session_state.active_day) if st.session_state.active_day in day_keys else 0

selected_label = st.radio(
    "",
    day_labels,
    index=active_index,
    horizontal=True,
    label_visibility="collapsed",
    key="schedule_day_radio"
)

selected_index = day_labels.index(selected_label)
st.session_state.active_day = day_keys[selected_index]
# ── Per-day tab 
# عرض محتوى اليوم النشط فقط
active_day_key = st.session_state.active_day
for day_key, _, _ in DAYS:
    if day_key != active_day_key:
        continue
    schedule = st.session_state.schedule[day_key]
    
    if day_key == today_key:
        named_today = [tk for tk in schedule if tk.get("task", "").strip()]
        done_today  = sum(1 for tk in named_today if tk.get("done", False))
        tot_today   = total_day_minutes(schedule)
        extras      = []
        if named_today:
            extras.append(f"{done_today}/{len(named_today)}")
        if tot_today:
            extras.append(fmt_minutes(tot_today))
        extra_str = f" · {' · '.join(extras)}" if extras else ""
        st.markdown(
            f'<div class="today-badge"><span>🔵 {t("today_badge")}</span>'
            f'<span style="font-weight:400;opacity:0.85;">{extra_str}</span></div>',
            unsafe_allow_html=True
        )

    # ── Clear-day confirmation 
    if st.session_state[f"{day_key}_clear_confirm"]:
        st.markdown(
            '<div class="danger-confirm">⚠️ '
            + {
                "badini":  "هەمی کاران ژێببە؟",
                "english": "Clear all tasks for this day?",
                "arabic":  "مسح جميع المهام لهذا اليوم؟",
              }.get(st.session_state.lang, "Clear all tasks for this day?")
            + '</div>',
            unsafe_allow_html=True
        )
        st.markdown('<div class="confirm-row-anchor"></div>', unsafe_allow_html=True)
        cc1, cc2 = st.columns(2)
        with cc1:
            if st.button(
                "✓ " + {"badini": "بەلێ، ژێببە", "english": "Yes, clear", "arabic": "نعم، امسح"}.get(
                    st.session_state.lang, "Yes"),
                key=f"{day_key}_clear_yes", use_container_width=True
            ):
                st.session_state.schedule[day_key] = []
                st.session_state[f"{day_key}_reset"] += 1
                st.session_state[f"{day_key}_clear_confirm"] = False
                save_schedule()
                st.rerun()
        with cc2:
            if st.button(
                "✗ " + {"badini": "نەخێر", "english": "Cancel", "arabic": "إلغاء"}.get(
                    st.session_state.lang, "Cancel"),
                key=f"{day_key}_clear_no", use_container_width=True
            ):
                st.session_state[f"{day_key}_clear_confirm"] = False
                st.rerun()

    # ── Progress bar
    named   = [tk for tk in schedule if tk.get("task", "").strip()]
    n_total = len(named)
    n_done  = sum(1 for tk in named if tk.get("done", False))

    if n_total > 0:
        pct       = int((n_done / n_total) * 100)
        all_done  = n_done == n_total
        bar_color = "#4CAF50" if not all_done else "#2196F3"
        if all_done:
            st.markdown(
                f'<div class="all-done-banner">🎉 {n_done}/{n_total} — 100% {t("tasks_completed")}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(f"""
            <div class="prog-wrap">
                <div class="prog-header">
                    <span class="prog-label">{t("tasks_completed")}</span>
                    <span class="prog-pct">{n_done}/{n_total} — {pct}%</span>
                </div>
                <div class="prog-track">
                    <div class="prog-fill" style="width:{pct}%;background:{bar_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Per-day total scheduled time strip 
    day_total_min = total_day_minutes(schedule)
    if day_total_min > 0:
        total_lbl = {
            "badini":  f"⏱ هەمی دەم: {fmt_minutes(day_total_min)}",
            "english": f"⏱ Total scheduled: {fmt_minutes(day_total_min)}",
            "arabic":  f"⏱ إجمالي الوقت: {fmt_minutes(day_total_min)}",
        }.get(st.session_state.lang, f"⏱ {fmt_minutes(day_total_min)}")
        done_min = sum(
            int((datetime.strptime(e.get("end", "00:00"), "%H:%M") -
                 datetime.strptime(e.get("start", "00:00"), "%H:%M")).total_seconds() // 60)
            for e in schedule
            if e.get("done") and e.get("task", "").strip()
            and int((datetime.strptime(e.get("end", "00:00"), "%H:%M") -
                     datetime.strptime(e.get("start", "00:00"), "%H:%M")).total_seconds() // 60) > 0
        )
        done_lbl = f" · ✅ {fmt_minutes(done_min)}" if done_min > 0 else ""
        st.markdown(
            f'<div class="day-total-strip"><span>{total_lbl}{done_lbl}</span></div>',
            unsafe_allow_html=True
        )

    # ── Empty state
    if not schedule:
        no_tasks_msg = {
            "badini":  "هیچ كار نينە.",
            "english": "No tasks yet.",
            "arabic":  "لا توجد مهام بعد.",
        }
        hint_msg = {
            "badini":  "زێدەکرنێ کلیک بکە بو دروستکرنا کارەکێ",
            "english": "Click + Add Task below to get started",
            "arabic":  "انقر على + إضافة مهمة أدناه للبدء",
        }
        st.markdown(f"""
        <div class="empty-day">
            <div class="empty-day-icon">📭</div>
            <div>{no_tasks_msg.get(st.session_state.lang, no_tasks_msg["english"])}</div>
            <div class="empty-day-hint">{hint_msg.get(st.session_state.lang, hint_msg["english"])}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Column headers
        h1, h2, h3, h4 = st.columns([2.8, 0.7, 4.8, 0.7])
        with h1:
            st.markdown(f'<div class="col-header"><span>🕐 {col_time_label}</span></div>', unsafe_allow_html=True)
        with h2:
            st.markdown('<div class="col-header"><span>✅</span></div>', unsafe_allow_html=True)
        with h3:
            st.markdown(f'<div class="col-header"><span>📝 {col_task_label}</span></div>', unsafe_allow_html=True)
        with h4:
            st.markdown('<div class="col-header"></div>', unsafe_allow_html=True)

        changed      = False
        done_changed = False

        for i, entry in enumerate(schedule):
            c_time, c_done, c_task, c_del = st.columns([2.8, 0.7, 4.8, 0.7])

            with c_time:
                try:
                    start_val = datetime.strptime(entry["start"], "%H:%M").time()
                except Exception:
                    start_val = datetime.strptime("07:00", "%H:%M").time()
                try:
                    end_val = datetime.strptime(entry["end"], "%H:%M").time()
                except Exception:
                    end_val = datetime.strptime("08:00", "%H:%M").time()

                _sk = f"{day_key}_start_{i}_{st.session_state[f'{day_key}_reset']}"
                _ek = f"{day_key}_end_{i}_{st.session_state[f'{day_key}_reset']}"
                _live_s = st.session_state.get(_sk, start_val)
                _live_e = st.session_state.get(_ek, end_val)
                _cap_s  = (_live_s.strftime("%H:%M") if hasattr(_live_s, "strftime")
                           else entry.get("start", "--:--"))
                _cap_e  = (_live_e.strftime("%H:%M") if hasattr(_live_e, "strftime")
                           else entry.get("end", "--:--"))

                st.markdown(
                    f'<div class="time-pill">🕐 {_cap_s} → {_cap_e}</div>',
                    unsafe_allow_html=True
                )

                start_time = st.time_input(
                    time_start_label,
                    value=start_val,
                    key=_sk,
                    label_visibility="collapsed"
                )
                end_time = st.time_input(
                    time_end_label,
                    value=end_val,
                    key=_ek,
                    label_visibility="collapsed"
                )
                dur = format_duration(
                    start_time.strftime("%H:%M"),
                    end_time.strftime("%H:%M")
                )
                if dur:
                    st.markdown(
                        f'<span class="duration-badge">⏱ {dur}</span>',
                        unsafe_allow_html=True
                    )

            with c_done:
                done = st.checkbox(
                    "", value=entry.get("done", False),
                    key=f"{day_key}_done_{i}_{st.session_state[f'{day_key}_reset']}",
                    label_visibility="collapsed"
                )

            with c_task:
                task_text = st.text_input(
                    "", value=entry.get("task", ""),
                    key=f"{day_key}_task_{i}_{st.session_state[f'{day_key}_reset']}",
                    disabled=done, label_visibility="collapsed",
                    placeholder=t("activity_placeholder")
                )

            with c_del:
                delete_btn = st.button(
                    "✕",
                    key=f"{day_key}_del_{i}_{st.session_state[f'{day_key}_reset']}"
                )

            if entry.get("done", False) != done:
                entry["done"] = done
                changed = done_changed = True

            if entry.get("task", "") != task_text:
                entry["task"] = task_text
                changed = True

            ns = start_time.strftime("%H:%M")
            if entry.get("start") != ns:
                entry["start"] = ns
                changed = True

            ne = end_time.strftime("%H:%M")
            if entry.get("end") != ne:
                entry["end"] = ne
                changed = True

            if delete_btn:
                schedule.pop(i)
                st.session_state.schedule[day_key] = schedule
                st.session_state[f"{day_key}_reset"] += 1
                save_schedule()
                st.rerun()

        if changed:
            st.session_state.schedule[day_key] = schedule
            save_schedule()
            if done_changed:
                st.rerun()

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    # ── نسخ اليوم إلى يوم آخر 
    st.divider()
    copy_day_lbl = {
        "badini": "📋 ڕۆژێ کۆپی بکە بو ڕۆژەکێ دی",
        "english": "📋 Copy Day to Another Day",
        "arabic": "📋 نسخ اليوم إلى يوم آخر",
    }.get(st.session_state.lang, "📋 Copy Day to Another Day")
    
    st.caption(copy_day_lbl)
    
    # اختيار اليوم الهدف (باستثناء اليوم النشط)
    target_days = [(dk, get_day_name(dk)) for dk, _, _ in DAYS if dk != active_day_key]
    target_day_labels = [name for _, name in target_days]
    target_day_keys   = [dk for dk, _ in target_days]
    
    if target_day_labels:
        # وضع selectbox والزر في صف واحد
        col_target, col_btn = st.columns([3, 1])
        
        with col_target:
            target_day = st.selectbox(
                "👉 " + {
                    "badini": "ڕۆژێ ئارمانج",
                    "english": "Target day",
                    "arabic": "اليوم الهدف",
                }.get(st.session_state.lang, "Target day"),
                target_day_labels,
                key=f"copy_day_target_{active_day_key}",
                label_visibility="visible"
            )
        
        with col_btn:
            # الحصول على المفتاح المختار
            selected_target_key = target_day_keys[target_day_labels.index(target_day)]
            
            copy_day_btn_lbl = {
                "badini": "📋 کۆپی بکە",
                "english": "📋 Copy",
                "arabic": "📋 نسخ",
            }.get(st.session_state.lang, "📋 Copy")
            
            # إضافة مسافة صغيرة لمحاذاة الزر مع selectbox
            st.markdown('<div style="height: 4px;"></div>', unsafe_allow_html=True)
            
            if st.button(
                copy_day_btn_lbl,
                key=f"copy_day_btn_{active_day_key}",
                use_container_width=True
            ):
                # نسخ مهام اليوم النشط إلى اليوم الهدف
                tasks_to_copy = st.session_state.schedule[active_day_key]
                st.session_state.schedule[selected_target_key] = [
                    {"start": t.get("start", "08:00"),
                     "end": t.get("end", "09:00"),
                     "task": t.get("task", ""),
                     "done": False}
                    for t in tasks_to_copy
                ]
                st.session_state[f"{selected_target_key}_reset"] += 1
                save_schedule()
                st.success({
                    "badini": f"✅ هاتە کۆپیکرن بۆ {get_day_name(selected_target_key)}!",
                    "english": f"✅ Copied to {get_day_name(selected_target_key)}!",
                    "arabic": f"✅ تم النسخ إلى {get_day_name(selected_target_key)}!",
                }.get(st.session_state.lang, "✅ Copied!"))
                st.rerun()
    # ── Action buttons 
    st.markdown('<div class="action-row-anchor"></div>', unsafe_allow_html=True)
    b1, b2, b3, b4 = st.columns(4)

    with b1:
        add_lbl = {
            "badini": "➕ زێدەکرن", "english": "➕ Add Task", "arabic": "➕ إضافة",
        }
        if st.button(
            add_lbl.get(st.session_state.lang, "➕ Add Task"),
            key=f"{day_key}_add_{st.session_state[f'{day_key}_reset']}",
            use_container_width=True
        ):
            schedule.append({"start": "08:00", "end": "09:00", "task": "", "done": False})
            st.session_state.schedule[day_key] = schedule
            save_schedule()
            st.rerun()

    with b2:
        has_incomplete = any(not e.get("done",False) for e in schedule)
        if st.button(
            {"badini":"✅ هەموو","english":"✅ All Done","arabic":"✅ إتمام الكل"}.get(st.session_state.lang,"✅ All Done"),
            key=f"{day_key}_markall_{st.session_state[f'{day_key}_reset']}",
            use_container_width=True, disabled=not has_incomplete
        ):
            for e in schedule:
                e["done"] = True
            st.session_state[f"{day_key}_reset"] += 1
            st.session_state.schedule[day_key] = schedule
            save_schedule(); st.rerun()

    with b3:
        sort_disabled = len(schedule) <= 1
        sort_lbl = {
            "badini": "🔃 ڕیزکرن", "english": "🔃 Sort", "arabic": "🔃 ترتيب",
        }.get(st.session_state.lang, "🔃 Sort")
        
        # مفتاح ديناميكي
        sort_key = f"{day_key}_sort_{st.session_state[f'{day_key}_reset']}"
        
        if st.button(
            sort_lbl,
            key=sort_key,
            use_container_width=True,
            disabled=sort_disabled,
            help="Sort tasks by start time"
        ):
            schedule.sort(key=lambda e: parse_time(e.get("start", "00:00")))
            st.session_state.schedule[day_key] = schedule
            st.session_state[f"{day_key}_reset"] += 1
            save_schedule()
            st.rerun()
            
    with b4:
        clear_lbl = {
            "badini": "🗑️ ژێبرن", "english": "🗑️ Clear", "arabic": "🗑️ مسح",
        }
        if st.button(
            clear_lbl.get(st.session_state.lang, "🗑️ Clear"),
            key=f"{day_key}_clear_{st.session_state[f'{day_key}_reset']}",
            use_container_width=True, disabled=not schedule
        ):
            st.session_state[f"{day_key}_clear_confirm"] = True
            st.rerun()
