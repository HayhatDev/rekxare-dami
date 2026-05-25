import streamlit as st
from datetime import datetime
import json
import os

# --- PWA Manifest ---
st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js');
    }
</script>
""", unsafe_allow_html=True)


with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

if "lang" not in st.session_state:
    st.session_state.lang = "badini"

def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

DAYS = [
    ("sun", "☀️ ئێکشەمب", "Sunday"),
    ("mon", "📖 دووشەمب", "Monday"),
    ("tue", "📖 سێشەمب", "Tuesday"),
    ("wed", "📖 چارشەمب", "Wednesday"),
    ("thu", "📖 پێنجشەمب", "Thursday"),
    ("fri", "🕌 خودبە", "Friday"),
    ("sat", "🎉 شەمبی", "Saturday"),
]

def get_day_name(day_key):
    for dk, badini_name, eng_name in DAYS:
        if dk == day_key:
            if st.session_state.lang == "badini":
                return badini_name
            elif st.session_state.lang == "arabic":
                arabic_names = {
                    "sun": "☀️ الأحد", "mon": "📖 الاثنين", "tue": "📖 الثلاثاء",
                    "wed": "📖 الأربعاء", "thu": "📖 الخميس",
                    "fri": "🕌 الجمعة", "sat": "🎉 السبت"
                }
                return arabic_names.get(day_key, eng_name)
            else:
                return f"📖 {eng_name}"
    return day_key

SCHEDULE_FILE = "schedule_data.json"

def load_schedule():
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "dark_mode" in data:
                st.session_state.dark_mode = data["dark_mode"]
            return data.get("schedule", None)
    return None

def save_schedule():
    data = {
        "schedule": st.session_state.schedule,
        "dark_mode": st.session_state.dark_mode
    }
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.set_page_config(
    page_title=t("schedule_title"),
    page_icon="📅",
    layout="centered"
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "schedule" not in st.session_state:
    loaded = load_schedule()
    st.session_state.schedule = loaded if loaded else {
        dk: [] for dk, _, _ in DAYS
    }

for dk, _, _ in DAYS:
    if f"{dk}_reset" not in st.session_state:
        st.session_state[f"{dk}_reset"] = 0

today_map = {6: "sun", 0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat"}
today_key = today_map[datetime.now().weekday()]
is_dark   = st.session_state.dark_mode

if is_dark:
    APP_BG       = "#1a1a2e"
    SB_BG        = "#16213e"
    CARD_BG      = "rgba(255,255,255,0.06)"
    CARD_BORDER  = "rgba(255,255,255,0.09)"
    TEXT_PRIMARY = "#e2e2e2"
    TEXT_MUTED   = "#8a8fa8"
    SECTION_LBL  = "#555c72"
    INPUT_BG     = "#252542"
    BTN_BG       = "#252542"
    BTN_COLOR    = "#e2e2e2"
    BTN_BORDER   = "#3a3a5c"
    PROG_TRACK   = "rgba(255,255,255,0.08)"
    DIVIDER      = "rgba(255,255,255,0.08)"
    TODAY_BG     = "rgba(76,175,80,0.15)"
    TODAY_COLOR  = "#81c784"
    CELEBRATE_BG = "rgba(76,175,80,0.12)"
    CELEBRATE_C  = "#81c784"
else:
    APP_BG       = "#e8edf5"
    SB_BG        = "#f4f7fb"
    CARD_BG      = "#ffffff"
    CARD_BORDER  = "#dde3ed"
    TEXT_PRIMARY = "#1a1a2e"
    TEXT_MUTED   = "#6b7280"
    SECTION_LBL  = "#9ca3af"
    INPUT_BG     = "#ffffff"
    BTN_BG       = "#dde5f0"
    BTN_COLOR    = "#1a1a2e"
    BTN_BORDER   = "#c0cce0"
    PROG_TRACK   = "#dde3ed"
    DIVIDER      = "#dde3ed"
    TODAY_BG     = "rgba(76,175,80,0.10)"
    TODAY_COLOR  = "#2e7d32"
    CELEBRATE_BG = "rgba(76,175,80,0.08)"
    CELEBRATE_C  = "#2e7d32"

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
.stTimeInput input          {{
    background-color: {INPUT_BG} !important;
    border: 1px solid {CARD_BORDER} !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    padding: 6px 8px !important;
}}
.stTextInput input:focus    {{ border-color: #4CAF50 !important; }}

[data-testid="stCheckbox"] svg {{ stroke: #4CAF50 !important; }}

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
.stButton > button:hover:not(:disabled)  {{ opacity: 0.78 !important; transform: translateY(-1px) !important; }}
.stButton > button:disabled              {{ opacity: 0.30 !important; }}

/* Delete button - 4th column */
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

/* Add task button */
.add-task-anchor .stButton > button {{
    background: linear-gradient(135deg,#43a047,#66bb6a) !important;
    color: #fff !important;
    border-color: #388e3c !important;
    font-size: 14px !important;
    padding: 10px !important;
}}

.today-badge {{
    display: inline-flex; align-items: center; gap: 5px;
    background: {TODAY_BG}; color: {TODAY_COLOR} !important;
    border: 1px solid {TODAY_COLOR}44;
    font-size: 12px; font-weight: 700;
    padding: 4px 12px; border-radius: 20px; margin-bottom: 12px;
}}

.celebrate-banner {{
    background: {CELEBRATE_BG}; color: {CELEBRATE_C} !important;
    border: 1px solid {CELEBRATE_C}44;
    border-radius: 12px; padding: 14px 18px;
    text-align: center; font-weight: 700; font-size: 15px;
    margin-bottom: 16px;
}}

.prog-wrap      {{ margin-bottom: 16px; }}
.prog-header    {{
    display: flex; justify-content: space-between; align-items: center;
    font-size: 12px; color: {TEXT_MUTED} !important; margin-bottom: 6px;
}}
.prog-label     {{ font-weight: 600; color: {TEXT_PRIMARY} !important; }}
.prog-track     {{ background: {PROG_TRACK}; border-radius: 99px; height: 7px; overflow: hidden; }}
.prog-fill      {{ height: 7px; border-radius: 99px; transition: width 0.4s ease; }}

hr {{ border-color: {DIVIDER} !important; margin: 16px 0 !important; }}

[data-testid="stTabs"] [data-baseweb="tab"] {{
    font-size: 13px !important;
    font-weight: 600 !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 8px 14px !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    color: #4CAF50 !important;
    border-bottom-color: #4CAF50 !important;
}}

@media (max-width: 640px) {{
    .stTimeInput input {{ font-size: 12px !important; }}
    .stTextInput input {{ font-size: 12px !important; }}
}}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="padding:8px 0 20px;">
    <div style="font-size:26px;font-weight:900;letter-spacing:-0.5px;">📅 {t("schedule_title")}</div>
</div>
""", unsafe_allow_html=True)

def get_tab_label(day_key):
    day_name = get_day_name(day_key)
    tasks    = st.session_state.schedule.get(day_key, [])
    if not tasks:
        return day_name
    done  = sum(1 for tk in tasks if tk.get("done", False))
    total = len(tasks)
    badge = " ✅" if done == total else f" {done}/{total}"
    today = " 🔵" if day_key == today_key else ""
    return f"{day_name}{today}{badge}"

tab_labels = [get_tab_label(dk) for dk, _, _ in DAYS]
tabs = st.tabs(tab_labels)

for tab, (day_key, _, _) in zip(tabs, DAYS):
    with tab:
        schedule = st.session_state.schedule[day_key]

        if not schedule:
            schedule.append({"start": "07:00", "end": "08:00", "task": "", "done": False})

        if day_key == today_key:
            st.markdown(f'<div class="today-badge">🔵 {t("today_badge")}</div>', unsafe_allow_html=True)

        total_tasks = len(schedule)
        done_tasks  = sum(1 for tk in schedule if tk.get("done", False))
        
        # 🎉 باقة الاحتفال عند إنجاز كل المهام
        if total_tasks > 0 and done_tasks == total_tasks:
            st.markdown(f'<div class="celebrate-banner">🎉 {t("tasks_completed")}! — هەمی ئەرکێن خوە تەواو کرن!</div>', unsafe_allow_html=True)
        
        if total_tasks > 0:
            pct       = int((done_tasks / total_tasks) * 100) if total_tasks > 0 else 0
            bar_color = "#2196F3" if pct == 100 else "#4CAF50"
            st.markdown(f"""
            <div class="prog-wrap">
                <div class="prog-header">
                    <span class="prog-label">{t("tasks_completed")}</span>
                    <span>{done_tasks}/{total_tasks} — {pct}%</span>
                </div>
                <div class="prog-track">
                    <div class="prog-fill" style="width:{pct}%;background:{bar_color};"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        h1, h2, h3, h4 = st.columns([2, 0.7, 5, 0.7])
        with h1: st.caption("🕐 " + ("کات" if st.session_state.lang == "badini" else "Time" if st.session_state.lang == "english" else "الوقت"))
        with h2: st.caption("✅")
        with h3: st.caption("📝 " + ("چالاکی" if st.session_state.lang == "badini" else "Task" if st.session_state.lang == "english" else "المهمة"))
        with h4: st.caption("")

        changed = False
        for i, entry in enumerate(schedule):
            c_time, c_done, c_task, c_del = st.columns([2, 0.7, 5, 0.7])

            with c_time:
                start_time = st.time_input(
                    entry["start"],
                    value=datetime.strptime(entry["start"], "%H:%M").time(),
                    key=f"{day_key}_start_{i}_{st.session_state[f'{day_key}_reset']}"
                )
                end_time = st.time_input(
                    entry["end"],
                    value=datetime.strptime(entry["end"], "%H:%M").time(),
                    key=f"{day_key}_end_{i}_{st.session_state[f'{day_key}_reset']}"
                )
            with c_done:
                st.markdown('<div style="padding-top:6px;">', unsafe_allow_html=True)
                done = st.checkbox("",
                    value=entry.get("done", False),
                    key=f"{day_key}_done_{i}_{st.session_state[f'{day_key}_reset']}",
                    label_visibility="collapsed")
                st.markdown('</div>', unsafe_allow_html=True)

            with c_task:
                task_text = st.text_input("",
                    value=entry["task"],
                    key=f"{day_key}_task_{i}_{st.session_state[f'{day_key}_reset']}",
                    disabled=done,
                    label_visibility="collapsed",
                    placeholder=t("activity_placeholder"))

            with c_del:
                st.write("")
                delete_btn = st.button("✕",
                    key=f"{day_key}_del_{i}_{st.session_state[f'{day_key}_reset']}")

            if entry["done"] != done:
                entry["done"] = done
                changed = True

            if entry["task"] != task_text:
                entry["task"] = task_text
                changed = True

            new_start = start_time.strftime("%H:%M")
            if entry["start"] != new_start:
                entry["start"] = new_start
                changed = True

            new_end = end_time.strftime("%H:%M")
            if entry["end"] != new_end:
                entry["end"] = new_end
                changed = True

            if delete_btn:
                schedule.pop(i)
                st.session_state[f"{day_key}_reset"] += 1
                st.session_state.schedule[day_key] = schedule
                save_schedule()
                st.rerun()

        if changed:
            save_schedule()

        st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="add-task-anchor">', unsafe_allow_html=True)
        if st.button(t("add_task"),
                     key=f"{day_key}_add_{st.session_state[f'{day_key}_reset']}",
                     use_container_width=True):
            schedule.append({"start": "08:00", "end": "09:00", "task": "", "done": False})
            st.session_state.schedule[day_key] = schedule
            save_schedule()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
