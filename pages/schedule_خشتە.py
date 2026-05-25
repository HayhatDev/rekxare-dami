import streamlit as st
from datetime import datetime, time as dtime
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

DAY_EMOJIS = {
    "sun": "☀️", "mon": "📖", "tue": "📖",
    "wed": "📖", "thu": "📖", "fri": "🕌", "sat": "🎉"
}

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
                emoji = DAY_EMOJIS.get(day_key, "📖")
                return f"{emoji} {eng_name}"
    return day_key

def get_time_label():
    if st.session_state.lang == "badini":
        return "دەستپێک", "دووماهی"
    elif st.session_state.lang == "arabic":
        return "بداية", "نهاية"
    else:
        return "Start", "End"

def get_column_labels():
    if st.session_state.lang == "badini":
        return "کات", "چالاکی"
    elif st.session_state.lang == "arabic":
        return "الوقت", "المهمة"
    else:
        return "Time", "Task"

def get_duration_label():
    if st.session_state.lang == "badini":
        return "ماوە"
    elif st.session_state.lang == "arabic":
        return "المدة"
    else:
        return "Duration"

def format_duration(start_str, end_str):
    try:
        s = datetime.strptime(start_str, "%H:%M")
        e = datetime.strptime(end_str, "%H:%M")
        diff = int((e - s).total_seconds() // 60)
        if diff <= 0:
            return ""
        if diff < 60:
            return f"{diff}m"
        h, m = divmod(diff, 60)
        return f"{h}h {m}m" if m else f"{h}h"
    except Exception:
        return ""

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
    APP_BG        = "#1a1a2e"
    SB_BG         = "#16213e"
    INPUT_BG      = "#252542"
    CARD_BG       = "rgba(255,255,255,0.06)"
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
    DONE_BG       = "rgba(76,175,80,0.08)"
    OVERVIEW_BG   = "rgba(255,255,255,0.04)"
    OVERVIEW_BDR  = "rgba(255,255,255,0.09)"
    DURATION_COLOR= "#8a8fa8"
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
    DONE_BG       = "rgba(76,175,80,0.06)"
    OVERVIEW_BG   = "#ffffff"
    OVERVIEW_BDR  = "#dde3ed"
    DURATION_COLOR= "#9ca3af"

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
.stTextInput input:disabled {{
    text-decoration: line-through !important;
    opacity: 0.55 !important;
}}

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

.add-task-anchor .stButton > button {{
    background: linear-gradient(135deg,#43a047,#66bb6a) !important;
    color: #fff !important;
    border-color: #388e3c !important;
    font-size: 14px !important;
    padding: 10px !important;
}}

.mark-all-anchor .stButton > button {{
    background: linear-gradient(135deg,#1565c0,#1e88e5) !important;
    color: #fff !important;
    border-color: #0d47a1 !important;
    font-size: 13px !important;
    padding: 8px !important;
}}

.today-badge {{
    display: inline-flex; align-items: center; gap: 5px;
    background: {TODAY_BG}; color: {TODAY_COLOR} !important;
    border: 1px solid {TODAY_COLOR}44;
    font-size: 12px; font-weight: 700;
    padding: 4px 12px; border-radius: 20px; margin-bottom: 12px;
}}

.prog-wrap      {{ margin-bottom: 16px; }}
.prog-header    {{
    display: flex; justify-content: space-between; align-items: center;
    font-size: 12px; margin-bottom: 6px;
}}
.prog-label     {{ font-weight: 600; color: {TEXT_PRIMARY} !important; }}
.prog-pct       {{ color: {TEXT_MUTED} !important; }}
.prog-track     {{
    background: {PROG_TRACK};
    border-radius: 99px;
    height: 8px;
    overflow: hidden;
    position: relative;
}}
.prog-fill      {{
    height: 8px;
    border-radius: 99px;
    transition: width 0.4s ease;
    min-width: 0;
}}

.all-done-banner {{
    background: rgba(76,175,80,0.12);
    border: 1px solid rgba(76,175,80,0.35);
    border-radius: 12px;
    padding: 12px 16px;
    text-align: center;
    font-size: 14px;
    font-weight: 700;
    color: #4CAF50 !important;
    margin-bottom: 12px;
}}

.duration-badge {{
    font-size: 11px;
    color: {DURATION_COLOR} !important;
    background: transparent;
    padding: 2px 0;
    display: block;
    text-align: center;
    margin-top: 2px;
}}

.week-overview {{
    background: {OVERVIEW_BG};
    border: 1px solid {OVERVIEW_BDR};
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 20px;
}}
.week-overview-title {{
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: {TEXT_MUTED} !important;
    margin-bottom: 12px;
}}
.week-grid {{
    display: flex;
    gap: 6px;
    justify-content: space-between;
}}
.week-day {{
    flex: 1;
    text-align: center;
}}
.week-day-label {{
    font-size: 10px;
    font-weight: 700;
    color: {TEXT_MUTED} !important;
    margin-bottom: 5px;
    display: block;
}}
.week-day-mini-track {{
    background: {PROG_TRACK};
    border-radius: 99px;
    height: 5px;
    overflow: hidden;
    margin-bottom: 4px;
}}
.week-day-mini-fill {{
    height: 5px;
    border-radius: 99px;
}}
.week-day-count {{
    font-size: 10px;
    color: {TEXT_MUTED} !important;
}}
.week-today-dot {{
    display: inline-block;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #4CAF50;
    margin-bottom: 3px;
}}

hr {{ border-color: {DIVIDER} !important; margin: 16px 0 !important; }}

[data-testid="stTabs"] [data-baseweb="tab"] {{
    font-size: 12px !important;
    font-weight: 600 !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 8px 10px !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    color: #4CAF50 !important;
    border-bottom-color: #4CAF50 !important;
}}

@media (max-width: 640px) {{
    .stTimeInput input {{ font-size: 12px !important; }}
    .stTextInput input {{ font-size: 12px !important; }}
    .week-grid {{ gap: 3px; }}
}}
</style>
""", unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding:8px 0 16px;">
    <div style="font-size:26px;font-weight:900;letter-spacing:-0.5px;">📅 {t("schedule_title")}</div>
</div>
""", unsafe_allow_html=True)

# ── Dark mode toggle (top right) ──────────────────────────────────────────────
dm_col1, dm_col2 = st.columns([8, 1])
with dm_col2:
    dark_toggle = st.checkbox("🌙", value=is_dark,
                               key="dm_toggle_sched",
                               help="Dark mode" if st.session_state.lang == "english" else "")
    if dark_toggle != is_dark:
        st.session_state.dark_mode = dark_toggle
        save_schedule()
        st.rerun()

# ── Week overview (native Streamlit — avoids HTML rendering issues) ───────────
st.markdown(f"""
<div style="
    background:{OVERVIEW_BG};
    border:1px solid {OVERVIEW_BDR};
    border-radius:16px;
    padding:14px 16px 10px;
    margin-bottom:20px;
">
<div style="font-size:11px;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;color:{TEXT_MUTED};margin-bottom:10px;">
    📊 Weekly Progress
</div>
</div>
""", unsafe_allow_html=True)

week_cols = st.columns(7)
for col, (dk, _, eng) in zip(week_cols, DAYS):
    tasks  = st.session_state.schedule.get(dk, [])
    total  = len(tasks)
    done   = sum(1 for tk in tasks if tk.get("done", False))
    pct    = done / total if total > 0 else 0
    is_today = dk == today_key
    short  = eng[:3].upper()
    dot    = "🟢" if is_today else ""
    count  = f"{done}/{total}" if total else "—"
    with col:
        if dot:
            st.markdown(f"<div style='text-align:center;font-size:8px;margin-bottom:1px;'>{dot}</div>",
                        unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;font-size:10px;font-weight:700;color:{TEXT_MUTED};'>{short}</div>",
                    unsafe_allow_html=True)
        st.progress(pct)
        st.markdown(f"<div style='text-align:center;font-size:10px;color:{TEXT_MUTED};margin-top:-8px;'>{count}</div>",
                    unsafe_allow_html=True)

# ── Labels ────────────────────────────────────────────────────────────────────
time_start_label, time_end_label = get_time_label()
col_time_label, col_task_label = get_column_labels()
dur_label = get_duration_label()

def get_tab_label(day_key):
    day_name = get_day_name(day_key)
    tasks    = st.session_state.schedule.get(day_key, [])
    if not tasks:
        return day_name
    done  = sum(1 for tk in tasks if tk.get("done", False))
    total = len(tasks)
    badge = " ✅" if done == total and total > 0 else f" {done}/{total}"
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

        # ── Progress bar placeholder — filled AFTER widget processing ─────────
        # This is the fix: st.empty() lets us write the bar AFTER we know the
        # real current-run done state, not the stale pre-widget-render state.
        prog_placeholder = st.empty()

        h1, h2, h3, h4 = st.columns([2.8, 0.7, 4.8, 0.7])
        with h1: st.caption("🕐 " + col_time_label)
        with h2: st.caption("✅")
        with h3: st.caption("📝 " + col_task_label)
        with h4: st.caption("")

        changed = False
        current_done_states = []

        for i, entry in enumerate(schedule):
            c_time, c_done, c_task, c_del = st.columns([2.8, 0.7, 4.8, 0.7])

            with c_time:
                try:
                    start_val = datetime.strptime(entry["start"], "%H:%M").time()
                except Exception:
                    start_val = dtime(7, 0)
                try:
                    end_val = datetime.strptime(entry["end"], "%H:%M").time()
                except Exception:
                    end_val = dtime(8, 0)

                start_time = st.time_input(
                    time_start_label,
                    value=start_val,
                    key=f"{day_key}_start_{i}_{st.session_state[f'{day_key}_reset']}",
                    label_visibility="collapsed"
                )
                end_time = st.time_input(
                    time_end_label,
                    value=end_val,
                    key=f"{day_key}_end_{i}_{st.session_state[f'{day_key}_reset']}",
                    label_visibility="collapsed"
                )
                dur = format_duration(
                    start_time.strftime("%H:%M"),
                    end_time.strftime("%H:%M")
                )
                if dur:
                    st.markdown(f'<span class="duration-badge">⏱ {dur}</span>', unsafe_allow_html=True)

            with c_done:
                st.markdown('<div style="padding-top:6px;">', unsafe_allow_html=True)
                done = st.checkbox(
                    "",
                    value=entry.get("done", False),
                    key=f"{day_key}_done_{i}_{st.session_state[f'{day_key}_reset']}",
                    label_visibility="collapsed"
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with c_task:
                task_text = st.text_input(
                    "",
                    value=entry["task"],
                    key=f"{day_key}_task_{i}_{st.session_state[f'{day_key}_reset']}",
                    disabled=done,
                    label_visibility="collapsed",
                    placeholder=t("activity_placeholder")
                )

            with c_del:
                st.write("")
                delete_btn = st.button(
                    "✕",
                    key=f"{day_key}_del_{i}_{st.session_state[f'{day_key}_reset']}"
                )

            # Track the current-run done state for progress bar
            current_done_states.append(done)

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

        # ── NOW fill the progress bar with CURRENT-RUN data ──────────────────
        total_tasks = len(schedule)
        # Use current_done_states (captured from widgets this run) for accuracy
        done_tasks = sum(1 for d in current_done_states if d)

        with prog_placeholder:
            if total_tasks > 0:
                pct = int((done_tasks / total_tasks) * 100)
                all_done = done_tasks == total_tasks
                bar_color = "#2196F3" if all_done else "#4CAF50"

                if all_done:
                    st.markdown(f"""
                    <div class="all-done-banner">
                        ✅ {done_tasks}/{total_tasks} — 100%&nbsp;&nbsp;🎉
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="prog-wrap">
                        <div class="prog-header">
                            <span class="prog-label">{t("tasks_completed")}</span>
                            <span class="prog-pct">{done_tasks}/{total_tasks} — {pct}%</span>
                        </div>
                        <div class="prog-track">
                            <div class="prog-fill" style="width:{pct}%;background:{bar_color};"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)

        # ── Action buttons row ────────────────────────────────────────────────
        btn_col1, btn_col2 = st.columns(2)

        with btn_col1:
            st.markdown('<div class="add-task-anchor">', unsafe_allow_html=True)
            if st.button(
                t("add_task"),
                key=f"{day_key}_add_{st.session_state[f'{day_key}_reset']}",
                use_container_width=True
            ):
                schedule.append({"start": "08:00", "end": "09:00", "task": "", "done": False})
                st.session_state.schedule[day_key] = schedule
                save_schedule()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with btn_col2:
            has_incomplete = any(not e.get("done", False) for e in schedule if e.get("task", "").strip())
            st.markdown('<div class="mark-all-anchor">', unsafe_allow_html=True)
            mark_lbl = {"badini": "✅ هەموو تەواو", "english": "✅ Mark All Done", "arabic": "✅ إتمام الكل"}
            if st.button(
                mark_lbl.get(st.session_state.lang, "✅ Mark All Done"),
                key=f"{day_key}_markall_{st.session_state[f'{day_key}_reset']}",
                use_container_width=True,
                disabled=not has_incomplete
            ):
                for entry in schedule:
                    entry["done"] = True
                st.session_state.schedule[day_key] = schedule
                save_schedule()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
