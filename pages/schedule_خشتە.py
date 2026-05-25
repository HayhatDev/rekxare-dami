import streamlit as st
from datetime import datetime, time as dtime
import json
import os

# ── Load translations first (pure Python — no Streamlit UI calls yet) ─────────
with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

if "lang" not in st.session_state:
    st.session_state.lang = "badini"

def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

# ── set_page_config MUST be the first Streamlit UI call ───────────────────────
st.set_page_config(
    page_title=t("schedule_title"),
    page_icon="📅",
    layout="centered"
)

# ── PWA Manifest ───────────────────────────────────────────────────────────────
st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/service-worker.js');
    }
</script>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
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
SCHEDULE_FILE = "schedule_data.json"

# ── Helpers ────────────────────────────────────────────────────────────────────
def get_day_name(day_key):
    for dk, badini_name, eng_name in DAYS:
        if dk == day_key:
            if st.session_state.lang == "badini":
                return badini_name
            elif st.session_state.lang == "arabic":
                arabic_names = {
                    "sun": "☀️ الأحد", "mon": "📖 الاثنين", "tue": "📖 الثلاثاء",
                    "wed": "📖 الأربعاء", "thu": "📖 الخميس",
                    "fri": "🕌 الجمعة", "sat": "🎉 السبت",
                }
                return arabic_names.get(day_key, eng_name)
            else:
                return f"{DAY_EMOJIS.get(day_key, '📖')} {eng_name}"
    return day_key

def get_time_label():
    if st.session_state.lang == "badini":
        return "دەستپێک", "دووماهی"
    elif st.session_state.lang == "arabic":
        return "بداية", "نهاية"
    return "Start", "End"

def get_column_labels():
    if st.session_state.lang == "badini":
        return "کات", "چالاکی"
    elif st.session_state.lang == "arabic":
        return "الوقت", "المهمة"
    return "Time", "Task"

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

def parse_time(s):
    """Return a comparable time tuple from HH:MM string, default 00:00 on error."""
    try:
        dt = datetime.strptime(s, "%H:%M")
        return (dt.hour, dt.minute)
    except Exception:
        return (0, 0)

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
        "dark_mode": st.session_state.dark_mode,
    }
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ── Session state init ─────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "schedule" not in st.session_state:
    loaded = load_schedule()
    # Ensure all 7 day keys always exist — guard against incomplete saved files
    base = {dk: [] for dk, _, _ in DAYS}
    if loaded:
        base.update(loaded)
    st.session_state.schedule = base

# Ensure all day keys exist even if loaded file was partial
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

# ── Theme ──────────────────────────────────────────────────────────────────────
if is_dark:
    APP_BG        = "#1a1a2e"
    SB_BG         = "#16213e"
    INPUT_BG      = "#252542"
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
    DURATION_COLOR= "#8a8fa8"
    EMPTY_COLOR   = "#555c72"
else:
    APP_BG        = "#e8edf5"
    SB_BG         = "#f4f7fb"
    INPUT_BG      = "#ffffff"
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
    DURATION_COLOR= "#9ca3af"
    EMPTY_COLOR   = "#9ca3af"

# ── CSS ────────────────────────────────────────────────────────────────────────
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
.stTextInput input:focus   {{ border-color: #4CAF50 !important; }}
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
.stButton > button:hover:not(:disabled) {{
    opacity: 0.78 !important;
    transform: translateY(-1px) !important;
}}
.stButton > button:disabled {{ opacity: 0.30 !important; }}

/* Delete button (4th column) */
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
}}
.sort-anchor .stButton > button {{
    background: linear-gradient(135deg,#6a1b9a,#ab47bc) !important;
    color: #fff !important;
    border-color: #4a148c !important;
    font-size: 13px !important;
}}
.clear-anchor .stButton > button {{
    background: transparent !important;
    color: #ef5350 !important;
    border-color: #ef535044 !important;
    font-size: 13px !important;
}}
.clear-anchor .stButton > button:hover {{
    background: rgba(239,83,80,0.10) !important;
    border-color: #ef5350 !important;
}}
.clear-confirm-yes .stButton > button {{
    background: linear-gradient(135deg,#c62828,#ef5350) !important;
    color: #fff !important;
    border-color: #b71c1c !important;
}}

.today-badge {{
    display: inline-flex; align-items: center; gap: 5px;
    background: {TODAY_BG}; color: {TODAY_COLOR} !important;
    border: 1px solid {TODAY_COLOR}44;
    font-size: 12px; font-weight: 700;
    padding: 4px 12px; border-radius: 20px; margin-bottom: 12px;
}}

.prog-wrap   {{ margin-bottom: 16px; }}
.prog-header {{
    display: flex; justify-content: space-between; align-items: center;
    font-size: 12px; margin-bottom: 6px;
}}
.prog-label  {{ font-weight: 600; color: {TEXT_PRIMARY} !important; }}
.prog-pct    {{ color: {TEXT_MUTED} !important; }}
.prog-track  {{
    background: {PROG_TRACK};
    border-radius: 99px; height: 8px; overflow: hidden;
}}
.prog-fill   {{
    height: 8px; border-radius: 99px; transition: width 0.4s ease;
}}

.all-done-banner {{
    background: rgba(76,175,80,0.12);
    border: 1px solid rgba(76,175,80,0.35);
    border-radius: 12px; padding: 12px 16px;
    text-align: center; font-size: 14px; font-weight: 700;
    color: #4CAF50 !important; margin-bottom: 12px;
}}

.empty-day {{
    text-align: center; padding: 32px 16px;
    color: {EMPTY_COLOR} !important;
    font-size: 13px;
}}
.empty-day-icon {{ font-size: 36px; margin-bottom: 8px; }}

.duration-badge {{
    font-size: 11px; color: {DURATION_COLOR} !important;
    background: transparent; display: block;
    text-align: center; margin-top: 2px;
}}

.danger-confirm {{
    background: rgba(239,83,80,0.10);
    border: 1px solid rgba(239,83,80,0.30);
    border-radius: 10px; padding: 10px 14px;
    font-size: 12px; font-weight: 600;
    color: #ef5350 !important; text-align: center;
    margin-bottom: 6px;
}}

hr {{ border-color: {DIVIDER} !important; margin: 16px 0 !important; }}

[data-testid="stTabs"] [data-baseweb="tab"] {{
    font-size: 12px !important; font-weight: 600 !important;
    border-radius: 8px 8px 0 0 !important; padding: 8px 10px !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    color: #4CAF50 !important;
    border-bottom-color: #4CAF50 !important;
}}

[data-testid="stProgressBar"] p {{ display: none !important; }}

@media (max-width: 640px) {{
    .stTimeInput input {{ font-size: 12px !important; }}
    .stTextInput input {{ font-size: 12px !important; }}
}}
</style>
""", unsafe_allow_html=True)

# ── Page header ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding:8px 0 16px;">
    <div style="font-size:26px;font-weight:900;letter-spacing:-0.5px;">📅 {t("schedule_title")}</div>
</div>
""", unsafe_allow_html=True)

# ── Dark mode toggle ───────────────────────────────────────────────────────────
dm_col1, dm_col2 = st.columns([8, 1])
with dm_col2:
    dark_toggle = st.checkbox(
        "🌙", value=is_dark, key="dm_toggle_sched",
        help="Dark mode" if st.session_state.lang == "english" else ""
    )
    if dark_toggle != is_dark:
        st.session_state.dark_mode = dark_toggle
        save_schedule()
        st.rerun()

# ── Week overview — single HTML block so it renders inside the card ────────────
week_cells = ""
for dk, _, eng in DAYS:
    tasks    = st.session_state.schedule.get(dk, [])
    total    = len(tasks)
    done     = sum(1 for tk in tasks if tk.get("done", False))
    pct      = (done / total * 100) if total > 0 else 0
    short    = eng[:3].upper()
    is_today_d = dk == today_key
    bar_col  = "#2196F3" if is_today_d else "#4CAF50"
    dot_html = (
        f'<div style="width:6px;height:6px;border-radius:50%;background:#4CAF50;'
        f'margin:0 auto 4px;"></div>'
        if is_today_d else
        '<div style="height:10px;"></div>'
    )
    count = f"{done}/{total}" if total else "—"
    week_cells += f"""
    <div style="flex:1;text-align:center;">
        {dot_html}
        <div style="font-size:10px;font-weight:700;color:{TEXT_MUTED};margin-bottom:5px;">{short}</div>
        <div style="background:{PROG_TRACK};border-radius:99px;height:5px;overflow:hidden;margin-bottom:4px;">
            <div style="width:{pct:.1f}%;height:5px;border-radius:99px;background:{bar_col};"></div>
        </div>
        <div style="font-size:10px;color:{TEXT_MUTED};">{count}</div>
    </div>
    """

st.markdown(f"""
<div style="background:{OVERVIEW_BG};border:1px solid {OVERVIEW_BDR};
            border-radius:16px;padding:14px 16px;margin-bottom:20px;">
    <div style="font-size:11px;font-weight:700;letter-spacing:0.8px;
                text-transform:uppercase;color:{TEXT_MUTED};margin-bottom:12px;">
        📊 Weekly Progress
    </div>
    <div style="display:flex;gap:6px;justify-content:space-between;">
        {week_cells}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Label helpers ──────────────────────────────────────────────────────────────
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
    today_dot = " 🔵" if day_key == today_key else ""
    return f"{day_name}{today_dot}{badge}"

tab_labels = [get_tab_label(dk) for dk, _, _ in DAYS]
tabs = st.tabs(tab_labels)

# ── Per-day tab ────────────────────────────────────────────────────────────────
for tab, (day_key, _, _) in zip(tabs, DAYS):
    with tab:
        schedule = st.session_state.schedule[day_key]

        # Today badge
        if day_key == today_key:
            st.markdown(
                f'<div class="today-badge">🔵 {t("today_badge")}</div>',
                unsafe_allow_html=True
            )

        # Clear-day confirmation flow
        if st.session_state[f"{day_key}_clear_confirm"]:
            st.markdown('<div class="danger-confirm">⚠️ Clear all tasks for this day?</div>',
                        unsafe_allow_html=True)
            cc1, cc2 = st.columns(2)
            with cc1:
                st.markdown('<div class="clear-confirm-yes">', unsafe_allow_html=True)
                if st.button("✓ Yes, clear", key=f"{day_key}_clear_yes", use_container_width=True):
                    st.session_state.schedule[day_key] = []
                    st.session_state[f"{day_key}_reset"] += 1
                    st.session_state[f"{day_key}_clear_confirm"] = False
                    save_schedule()
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with cc2:
                if st.button("✗ Cancel", key=f"{day_key}_clear_no", use_container_width=True):
                    st.session_state[f"{day_key}_clear_confirm"] = False
                    st.rerun()

        # ── Progress bar (from session state — always accurate after checkbox rerun)
        named_tasks  = [tk for tk in schedule if tk.get("task", "").strip()]
        total_tasks  = len(named_tasks)
        done_tasks   = sum(1 for tk in named_tasks if tk.get("done", False))

        if total_tasks > 0:
            pct       = int((done_tasks / total_tasks) * 100)
            all_done  = done_tasks == total_tasks
            bar_color = "#2196F3" if all_done else "#4CAF50"
            if all_done:
                st.markdown(
                    f'<div class="all-done-banner">✅ {done_tasks}/{total_tasks} — 100%&nbsp;&nbsp;🎉</div>',
                    unsafe_allow_html=True
                )
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

        # ── Empty state ────────────────────────────────────────────────────────
        if not schedule:
            st.markdown(f"""
            <div class="empty-day">
                <div class="empty-day-icon">📭</div>
                <div>{t("no_tasks_yet") if t("no_tasks_yet") != "no_tasks_yet"
                     else "No tasks yet. Click + Add Task to get started."}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # ── Column headers ─────────────────────────────────────────────────
            h1, h2, h3, h4 = st.columns([2.8, 0.7, 4.8, 0.7])
            with h1: st.caption("🕐 " + col_time_label)
            with h2: st.caption("✅")
            with h3: st.caption("📝 " + col_task_label)
            with h4: st.caption("")

            changed      = False
            done_changed = False

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
                        st.markdown(
                            f'<span class="duration-badge">⏱ {dur}</span>',
                            unsafe_allow_html=True
                        )

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
                        value=entry.get("task", ""),
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

                # Apply widget changes to session state
                if entry.get("done", False) != done:
                    entry["done"] = done
                    changed      = True
                    done_changed = True   # checkbox flip → rerun for fresh progress bar

                if entry.get("task", "") != task_text:
                    entry["task"] = task_text
                    changed = True

                new_start = start_time.strftime("%H:%M")
                if entry.get("start") != new_start:
                    entry["start"] = new_start
                    changed = True

                new_end = end_time.strftime("%H:%M")
                if entry.get("end") != new_end:
                    entry["end"] = new_end
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
                    st.rerun()   # refresh progress bar immediately

        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

        # ── Action buttons ─────────────────────────────────────────────────────
        btn1, btn2, btn3, btn4 = st.columns(4)

        with btn1:
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

        with btn2:
            has_incomplete = any(
                not e.get("done", False)
                for e in schedule if e.get("task", "").strip()
            )
            mark_lbl = {
                "badini": "✅ هەموو",
                "english": "✅ All Done",
                "arabic": "✅ إتمام الكل",
            }
            st.markdown('<div class="mark-all-anchor">', unsafe_allow_html=True)
            if st.button(
                mark_lbl.get(st.session_state.lang, "✅ All Done"),
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

        with btn3:
            can_sort = len(schedule) > 1
            sort_lbl = {
                "badini": "🔃 ڕیزکردن",
                "english": "🔃 Sort",
                "arabic": "🔃 ترتيب",
            }
            st.markdown('<div class="sort-anchor">', unsafe_allow_html=True)
            if st.button(
                sort_lbl.get(st.session_state.lang, "🔃 Sort"),
                key=f"{day_key}_sort_{st.session_state[f'{day_key}_reset']}",
                use_container_width=True,
                disabled=not can_sort,
                help="Sort tasks by start time"
            ):
                schedule.sort(key=lambda e: parse_time(e.get("start", "00:00")))
                st.session_state.schedule[day_key] = schedule
                st.session_state[f"{day_key}_reset"] += 1
                save_schedule()
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with btn4:
            clear_lbl = {
                "badini": "🗑️ سڕینەوە",
                "english": "🗑️ Clear",
                "arabic": "🗑️ مسح",
            }
            st.markdown('<div class="clear-anchor">', unsafe_allow_html=True)
            if st.button(
                clear_lbl.get(st.session_state.lang, "🗑️ Clear"),
                key=f"{day_key}_clear_{st.session_state[f'{day_key}_reset']}",
                use_container_width=True,
                disabled=not schedule
            ):
                st.session_state[f"{day_key}_clear_confirm"] = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
