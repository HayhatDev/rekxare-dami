import streamlit as st
from datetime import datetime
import json
import os

# --- Load translations ---
with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

if "lang" not in st.session_state:
    st.session_state.lang = "badini"

def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

# --- Days of the week ---
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
                    "wed": "📖 الأربعاء", "thu": "📖 الخميس", "fri": "🕌 الجمعة", "sat": "🎉 السبت"
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

st.set_page_config(page_title=t("schedule_title"), page_icon="📅")

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "schedule" not in st.session_state:
    loaded = load_schedule()
    if loaded:
        st.session_state.schedule = loaded
    else:
        st.session_state.schedule = {
            "sun": [], "mon": [], "tue": [], "wed": [],
            "thu": [], "fri": [], "sat": [],
        }

for day in ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]:
    if f"{day}_reset" not in st.session_state:
        st.session_state[f"{day}_reset"] = 0

today_map = {6: "sun", 0: "mon", 1: "tue", 2: "wed", 3: "thu", 4: "fri", 5: "sat"}
today_key = today_map[datetime.now().weekday()]

st.markdown("""
<style>
    .stButton > button { border-radius: 10px !important; font-weight: 600 !important; transition: opacity 0.2s ease !important; }
    .stButton > button:hover:not(:disabled) { opacity: 0.85 !important; }
    .stTextInput > div > div > input { border-radius: 8px !important; }
    div[data-testid="metric-container"] { background: rgba(76,175,80,0.08); border-radius: 10px; padding: 6px 10px; }
    .today-badge { display: inline-block; background: #4CAF50; color: white; font-size: 12px; font-weight: 700; padding: 2px 10px; border-radius: 20px; margin-bottom: 8px; }
    .progress-bar-bg { background: #e8eaf0; border-radius: 10px; height: 8px; margin: 6px 0 12px 0; overflow: hidden; }
    .progress-bar-fill { height: 8px; border-radius: 10px; background: #4CAF50; transition: width 0.4s ease; }
</style>
""", unsafe_allow_html=True)

if st.session_state.dark_mode:
    st.markdown("""
    <style>
        .stApp { background-color: #1a1a2e !important; }
        [data-testid="stSidebar"] { background-color: #16213e !important; }
        .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label { color: #e0e0e0 !important; }
        .stTextInput input, .stSelectbox select, .stTimeInput input { background-color: #2d2d44 !important; color: #ffffff !important; border: 1px solid #444 !important; }
        .stButton button { background-color: #2d2d44 !important; color: #e0e0e0 !important; border: 1px solid #555 !important; }
        input[disabled] { text-decoration: line-through; color: #666 !important; background-color: #2d2d44 !important; }
        .progress-bar-bg { background: #2d2d44 !important; }
        div[data-testid="metric-container"] { background: rgba(76,175,80,0.12) !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        input[disabled] { text-decoration: line-through; color: #aaa !important; }
    </style>
    """, unsafe_allow_html=True)

st.title(t("schedule_title"))

def get_tab_label(day_key):
    day_name = get_day_name(day_key)
    tasks = st.session_state.schedule.get(day_key, [])
    if not tasks:
        return day_name
    done = sum(1 for t in tasks if t.get("done", False))
    total = len(tasks)
    marker = " ✅" if done == total and total > 0 else f" {done}/{total}"
    today_marker = " 🔵" if day_key == today_key else ""
    return f"{day_name}{today_marker}{marker}"

tab_labels = [get_tab_label(dk) for dk, _, _ in DAYS]
tab_keys = [dk for dk, _, _ in DAYS]
tabs = st.tabs(tab_labels)

for tab, (day_key, _, _) in zip(tabs, DAYS):
    with tab:
        schedule = st.session_state.schedule[day_key]

        if not schedule:
            schedule.append({"start": "07:00", "end": "08:00", "task": "", "done": False})

        if day_key == today_key:
            st.markdown(f'<span class="today-badge">{t("today_badge")}</span>', unsafe_allow_html=True)

        total_tasks = len(schedule)
        done_tasks = sum(1 for t in schedule if t.get("done", False))
        if total_tasks > 0:
            pct = int((done_tasks / total_tasks) * 100)
            bar_color = "#2196F3" if pct == 100 else "#4CAF50"
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; font-size:13px; opacity:0.7; margin-bottom:2px;">
                <span>{t("tasks_completed")}</span>
                <span>{done_tasks}/{total_tasks} — {pct}%</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width:{pct}%; background:{bar_color};"></div>
            </div>
            """, unsafe_allow_html=True)

        hcol1, hcol2, hcol3, hcol4 = st.columns([2, 1, 5, 1])
        with hcol1:
            st.caption("🕐")
        with hcol2:
            st.caption("✅")
        with hcol3:
            st.caption("📝")
        with hcol4:
            st.caption("🗑️")

        for i, entry in enumerate(schedule):
            col_time, col_done, col_task, col_delete = st.columns([2, 1, 5, 1])

            with col_time:
                start_time = st.time_input("",
                    value=datetime.strptime(entry["start"], "%H:%M").time() if entry["start"] else datetime.min.time(),
                    key=f"{day_key}_start_{i}_{st.session_state[f'{day_key}_reset']}",
                    label_visibility="collapsed")
                end_time = st.time_input("",
                    value=datetime.strptime(entry["end"], "%H:%M").time() if entry["end"] else datetime.min.time(),
                    key=f"{day_key}_end_{i}_{st.session_state[f'{day_key}_reset']}",
                    label_visibility="collapsed")

            with col_done:
                done = st.checkbox("✅", value=entry["done"],
                    key=f"{day_key}_done_{i}_{st.session_state[f'{day_key}_reset']}",
                    label_visibility="collapsed")

            with col_task:
                task_text = st.text_input("", value=entry["task"],
                    key=f"{day_key}_task_{i}_{st.session_state[f'{day_key}_reset']}",
                    disabled=done, label_visibility="collapsed",
                    placeholder=t("activity_placeholder"))

            with col_delete:
                st.write("")
                delete_btn = st.button("🗑️", key=f"{day_key}_del_{i}_{st.session_state[f'{day_key}_reset']}")

            if entry["done"] != done:
                entry["done"] = done
                save_schedule()
                st.rerun()

            entry["task"] = task_text
            entry["start"] = start_time.strftime("%H:%M")
            entry["end"] = end_time.strftime("%H:%M")

            if delete_btn:
                schedule.pop(i)
                st.session_state[f"{day_key}_reset"] += 1
                st.session_state.schedule[day_key] = schedule
                save_schedule()
                st.rerun()

        st.divider()
        if st.button(t("add_task"),
            key=f"{day_key}_add_{st.session_state[f'{day_key}_reset']}",
            use_container_width=True):
            schedule.append({"start": "08:00", "end": "09:00", "task": "", "done": False})
            st.session_state.schedule[day_key] = schedule
            save_schedule()
            st.rerun()
