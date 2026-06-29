import streamlit as st
import json
import os
import hashlib
import base64
import streamlit.components.v1 as components
from datetime import datetime

# ══════════════════════════════════════════════════════════
#  TRANSLATIONS
# ══════════════════════════════════════════════════════════
with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

if "lang" not in st.session_state:
    st.session_state.lang = "badini"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text


def get_preferences_file():
    email = st.user.email if st.user.is_logged_in else st.session_state.get("user_email", "default")
    return f"preferences_{hashlib.md5(email.encode()).hexdigest()[:8]}.json"


def save_preferences():
    with open(get_preferences_file(), "w", encoding="utf-8") as f:
        json.dump({
            "dark_mode": st.session_state.get("dark_mode", True),
            "lang":      st.session_state.get("lang", "badini"),
        }, f, ensure_ascii=False, indent=2)


def load_preferences():
    fn = get_preferences_file()
    if os.path.exists(fn):
        try:
            with open(fn, "r", encoding="utf-8") as f:
                d = json.load(f)
            st.session_state.dark_mode = d.get("dark_mode", True)
            st.session_state.lang      = d.get("lang", "badini")
            return True
        except Exception:
            pass
    return False


# ══════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Rekxare Dami",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<link rel="manifest" href="/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#1a1a2e">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js').catch(function(){});
  }
</script>
""", unsafe_allow_html=True)

if st.user.is_logged_in:
    if "user_email" not in st.session_state or not st.session_state.user_email:
        st.session_state.user_email = st.user.email
        st.session_state.data_key   = hashlib.md5(st.user.email.encode()).hexdigest()[:8]
        st.session_state.logged_in  = True
    load_preferences()

# ══════════════════════════════════════════════════════════
#  LOGIN GATE
# ══════════════════════════════════════════════════════════
if not st.user.is_logged_in:
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*,*::before,*::after{{box-sizing:border-box;}}
html,body,.stApp,[data-testid="stAppViewContainer"],
section[data-testid="stMain"],.main,.main .block-container{{
    background:linear-gradient(135deg,#0f0c29,#1a1a2e,#16213e)!important;
    font-family:'Inter',system-ui,sans-serif!important;
}}
header[data-testid="stHeader"]{{height:0!important;overflow:hidden!important;}}
[data-testid="stSidebar"],[data-testid="stSidebarCollapsedControl"],
[data-testid="stStatusWidget"],[data-testid="stToolbar"],
[data-testid="stDecoration"],#MainMenu,footer{{display:none!important;}}
.main .block-container{{
    padding-top:max(20px,calc(50vh - 280px))!important;
    padding-bottom:40px!important;padding-left:20px!important;
    padding-right:20px!important;max-width:480px!important;
}}
.lw{{width:100%;display:flex;flex-direction:column;align-items:center;}}
.ll{{font-size:72px;line-height:1;margin-bottom:12px;animation:lfloat 3s ease-in-out infinite,lglow 3s ease-in-out infinite;}}
@keyframes lfloat{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-10px);}}}}
@keyframes lglow{{
  0%,100%{{filter:drop-shadow(0 4px 16px rgba(76,175,80,.4));}}
  50%{{filter:drop-shadow(0 4px 28px rgba(76,175,80,.85));}}
}}
.lt{{font-size:32px;font-weight:900;letter-spacing:-.8px;color:#fff;text-align:center;margin-bottom:4px;}}
.ls{{font-size:14px;color:rgba(255,255,255,.55);text-align:center;margin-bottom:24px;font-weight:500;}}
.lb{{display:inline-flex;align-items:center;gap:6px;background:rgba(76,175,80,.15);
    border:1px solid rgba(76,175,80,.25);color:#81c784;border-radius:20px;
    padding:5px 14px;font-size:11px;font-weight:700;letter-spacing:.5px;margin-bottom:24px;}}
.lc{{background:rgba(0,0,0,.5);border:1.5px solid rgba(255,255,255,.13);border-radius:28px;
    padding:32px 28px 28px;width:100%;backdrop-filter:blur(12px);box-shadow:0 8px 40px rgba(0,0,0,.40);}}
.stButton>button{{background:linear-gradient(135deg,#388e3c,#4caf50)!important;
    color:#fff!important;border:none!important;border-radius:40px!important;
    font-weight:700!important;font-size:14px!important;min-height:44px!important;
    box-shadow:0 2px 8px rgba(76,175,80,.3)!important;transition:all .18s ease!important;width:100%!important;}}
.stButton>button:hover{{transform:translateY(-2px)!important;box-shadow:0 6px 16px rgba(76,175,80,.45)!important;}}
.lc .stButton>button{{font-size:16px!important;min-height:52px!important;}}
.dv{{display:flex;align-items:center;gap:12px;margin:24px 0 20px;color:rgba(255,255,255,.35);font-size:12px;font-weight:600;}}
.dv::before,.dv::after{{content:"";flex:1;height:1px;background:rgba(255,255,255,.15);}}
.lf{{font-size:12px;color:rgba(255,255,255,.30);text-align:center;margin-top:24px;}}
</style>
<div class="lw">
  <div class="ll">📚</div>
  <div class="lt">Rekxare Dami</div>
  <div class="ls">{t('login_sub')}</div>
  <div class="lb">✨ {t('login_badge')}</div>
  <div class="lc">
""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("بادينى", key="lang_badini_login", use_container_width=True):
            st.session_state.lang = "badini"; st.rerun()
    with c2:
        if st.button("English", key="lang_en_login", use_container_width=True):
            st.session_state.lang = "english"; st.rerun()
    with c3:
        if st.button("العربية", key="lang_ar_login", use_container_width=True):
            st.session_state.lang = "arabic"; st.rerun()

    st.markdown(f'<div class="dv">{t("login_divider")}</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.button("🔐 Google", on_click=st.login, use_container_width=True)
    st.markdown(f'<div class="lf">{t("login_footer")}</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════
#  QUERY PARAM HANDLERS
# ══════════════════════════════════════════════════════════
if "dark_mode" in st.query_params:
    st.session_state.dark_mode = not st.session_state.get("dark_mode", True)
    save_preferences()
    st.query_params.clear()
    st.rerun()

if st.query_params.get("lang") == "cycle":
    order = ["badini", "english", "arabic"]
    cur = st.session_state.get("lang", "badini")
    st.session_state.lang = order[(order.index(cur) + 1) % 3] if cur in order else "badini"
    save_preferences()
    st.query_params.clear()
    st.rerun()

# ══════════════════════════════════════════════════════════
#  NAVIGATION
# ══════════════════════════════════════════════════════════
pg = st.navigation(
    [
        st.Page("Home.py",              title="Rekxare Dami · " + t("nav_timer"),    icon="⏱️", default=True),
        st.Page("pages/01_Schedule.py", title="Rekxare Dami · " + t("nav_schedule"), icon="📅", url_path="schedule"),
        st.Page("pages/02_About.py",    title="Rekxare Dami · " + t("nav_about"),    icon="✨",  url_path="about"),
    ],
    position="hidden",
)

_upath = getattr(pg, "url_path", "") or ""
if _upath == "schedule":
    _active = "schedule"
elif _upath == "about":
    _active = "about"
else:
    _active = "home"

st.session_state.current_page = _active


# ══════════════════════════════════════════════════════════
#  SIDEBAR  (must run before render_nav so the DOM exists)
# ══════════════════════════════════════════════════════════
def render_sidebar(active: str = "home"):
    is_dark = st.session_state.get("dark_mode", True)
    lang    = st.session_state.get("lang", "badini")

    # ── Palette ──────────────────────────────────────────
    if is_dark:
        SB_BG       = "#0e0c24"
        PROF_BG     = "rgba(255,255,255,0.03)"
        CARD_BG     = "rgba(255,255,255,0.055)"
        CARD_BDR    = "rgba(255,255,255,0.09)"
        ACT_BG      = "rgba(76,175,80,0.20)"
        ACT_C       = "#7ec87f"
        MUTED       = "rgba(255,255,255,0.42)"
        TXT         = "#e8e8f0"
        DIVIDER     = "rgba(255,255,255,0.07)"
        STAT_BG     = "rgba(76,175,80,0.10)"
        STAT_BDR    = "rgba(76,175,80,0.22)"
        GOAL_TRACK  = "rgba(76,175,80,0.14)"
        BTN_BG      = "rgba(255,255,255,0.06)"
        BTN_BDR     = "rgba(255,255,255,0.11)"
        NAV_HOV     = "rgba(255,255,255,0.06)"
        NAV_BDR_HOV = "rgba(255,255,255,0.10)"
        SIGN_BG     = "rgba(239,83,80,0.10)"
        SIGN_BDR    = "rgba(239,83,80,0.24)"
        SIGN_C      = "#ef9a9a"
        SCHED_BG    = "rgba(33,150,243,0.10)"
        SCHED_BDR   = "rgba(33,150,243,0.22)"
        SCHED_C     = "#64b5f6"
        ABOUT_BG    = "rgba(171,71,188,0.10)"
        ABOUT_BDR   = "rgba(171,71,188,0.22)"
        RING_EMPTY  = "rgba(76,175,80,0.18)"
        RING_FILL   = "#4caf50"
    else:
        SB_BG       = "#f4f6fb"
        PROF_BG     = "rgba(0,0,0,0.03)"
        CARD_BG     = "#ffffff"
        CARD_BDR    = "#dde4f0"
        ACT_BG      = "rgba(46,125,50,0.12)"
        ACT_C       = "#2e7d32"
        MUTED       = "#6b7280"
        TXT         = "#1a1a2e"
        DIVIDER     = "#e2e8f5"
        STAT_BG     = "rgba(76,175,80,0.07)"
        STAT_BDR    = "rgba(76,175,80,0.18)"
        GOAL_TRACK  = "rgba(76,175,80,0.12)"
        BTN_BG      = "#edf0f7"
        BTN_BDR     = "#c8d4e8"
        NAV_HOV     = "rgba(0,0,0,0.05)"
        NAV_BDR_HOV = "#dde4f0"
        SIGN_BG     = "#ffebee"
        SIGN_BDR    = "#ef9a9a"
        SIGN_C      = "#c62828"
        SCHED_BG    = "rgba(33,150,243,0.07)"
        SCHED_BDR   = "rgba(33,150,243,0.18)"
        SCHED_C     = "#1565c0"
        ABOUT_BG    = "rgba(171,71,188,0.07)"
        ABOUT_BDR   = "rgba(171,71,188,0.18)"
        RING_EMPTY  = "rgba(76,175,80,0.15)"
        RING_FILL   = "#388e3c"

    # ── User info ────────────────────────────────────────
    if st.user.is_logged_in:
        user_name  = (st.user.name or st.user.email or t("student"))[:24]
        user_email = st.user.email or ""
    else:
        user_name  = t("student")
        user_email = ""
    initials = next((c for c in user_name if c.isalpha()), "S").upper()

    # ── Study stats (safe defaults for first load) ────────
    total_s      = st.session_state.get("total_study_seconds", 0)
    sessions     = st.session_state.get("completed_sessions", 0)
    streak       = st.session_state.get("streak", 0)
    daily_s      = st.session_state.get("daily_seconds", 0)
    daily_goal_s = st.session_state.get("daily_goal_seconds", 7200)
    daily_pct    = min(100, int(daily_s / max(1, daily_goal_s) * 100))
    total_h      = total_s // 3600
    total_m      = (total_s % 3600) // 60
    daily_min    = daily_s // 60
    goal_min     = daily_goal_s // 60

    if total_h > 0:
        time_str = f"{total_h}h {total_m}m"
    elif total_m > 0:
        time_str = f"{total_m}m"
    else:
        time_str = "—"

    # ── Schedule stats ────────────────────────────────────
    schedule       = st.session_state.get("schedule", {})
    today_map      = {6:"sun",0:"mon",1:"tue",2:"wed",3:"thu",4:"fri",5:"sat"}
    today_key_sb   = today_map[datetime.now().weekday()]
    today_entries  = [e for e in schedule.get(today_key_sb, []) if e.get("task","").strip()]
    today_done     = sum(1 for e in today_entries if e.get("done", False))
    today_total    = len(today_entries)
    sched_pct      = int(today_done / max(1, today_total) * 100) if today_total else 0
    # SVG ring math: circumference = 2π×15 ≈ 94.25
    ring_dash      = round(sched_pct * 0.9425, 1)

    # ── Toggle labels ─────────────────────────────────────
    dark_icon = "☀️" if is_dark else "🌙"
    mode_lbl  = {"badini": "روناهی" if is_dark else "شەڤ",
                 "english": "Light" if is_dark else "Dark",
                 "arabic":  "نهار"  if is_dark else "ليل"}.get(lang, "Light" if is_dark else "Dark")
    toggle_lbl = f"{dark_icon} {mode_lbl}"

    # ── Page-specific card HTML ──────────────────────────
    if active == "home":
        page_card = f"""
<div class="sb-sec-label">📊 {t('sidebar_title')}</div>
<div class="sb-stats-row">
  <div class="sb-stat">
    <div class="sb-stat-val">{time_str}</div>
    <div class="sb-stat-lbl">⏱️ {t('hours_unit')}</div>
  </div>
  <div class="sb-stat">
    <div class="sb-stat-val">{sessions}</div>
    <div class="sb-stat-lbl">✅ {t('stat_sessions')}</div>
  </div>
  <div class="sb-stat">
    <div class="sb-stat-val">{streak}</div>
    <div class="sb-stat-lbl">🔥 {t('streak_days')}</div>
  </div>
</div>
<div class="sb-goal-wrap">
  <div class="sb-goal-hdr">
    <span class="sb-goal-lbl">🎯 {t('daily_goal')}</span>
    <span class="sb-goal-pct" style="color:{ACT_C}!important">{daily_pct}%</span>
  </div>
  <div class="sb-track">
    <div class="sb-fill" style="width:{daily_pct}%;background:linear-gradient(90deg,#388e3c,#81c784)"></div>
  </div>
  <div class="sb-goal-sub">{daily_min}m / {goal_min}m</div>
</div>"""

    elif active == "schedule":
        task_label = t("week_tasks")
        page_card = f"""
<div class="sb-sec-label">📅 {t('nav_schedule')}</div>
<div class="sb-sched-card" style="background:{SCHED_BG};border-color:{SCHED_BDR}">
  <div class="sb-sched-row">
    <div class="sb-sched-left">
      <div class="sb-sched-count" style="color:{SCHED_C}!important">{today_done}<span class="sb-sched-of">/{today_total}</span></div>
      <div class="sb-sched-lbl">{task_label} {t('today_badge')}</div>
    </div>
    <svg class="sb-ring-svg" viewBox="0 0 36 36" width="52" height="52">
      <circle cx="18" cy="18" r="15" fill="none" stroke="{RING_EMPTY}" stroke-width="3.5"/>
      <circle cx="18" cy="18" r="15" fill="none" stroke="{RING_FILL}" stroke-width="3.5"
        stroke-dasharray="{ring_dash} 94.25" stroke-dashoffset="23.5"
        stroke-linecap="round"/>
      <text x="18" y="21.5" text-anchor="middle"
        font-size="8.5" font-weight="800" fill="{RING_FILL}">{sched_pct}%</text>
    </svg>
  </div>
  <div class="sb-track" style="margin-top:10px">
    <div class="sb-fill" style="width:{sched_pct}%;background:linear-gradient(90deg,#1565c0,#64b5f6)"></div>
  </div>
</div>"""

    else:  # about
        pages_lbl = t("stat_pages")
        langs_lbl = t("stat_languages")
        page_card = f"""
<div class="sb-sec-label">✨ {t('nav_about')}</div>
<div class="sb-about-card" style="background:{ABOUT_BG};border-color:{ABOUT_BDR}">
  <div class="sb-about-icon">📚</div>
  <div>
    <div class="sb-about-name" style="color:{TXT}!important">Rekxare Dami</div>
    <div class="sb-about-meta" style="color:{MUTED}!important">v1.0 · 3 {pages_lbl} · 3 {langs_lbl}</div>
  </div>
</div>
<div class="sb-made" style="color:{MUTED}!important">{t('made_with')}</div>"""

    # ── Streak badge visibility ───────────────────────────
    streak_vis = "flex" if streak > 0 else "none"

    with st.sidebar:
        # ── Master CSS + Profile HTML ─────────────────────
        st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* ── Sidebar reset ── */
section[data-testid="stSidebar"] {{
    font-family:'Inter',system-ui,sans-serif!important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    padding:0!important;
}}
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
    gap:0!important;padding:0!important;
}}

/* ── Keyframes ── */
@keyframes sbDown {{
    from {{ transform:translateY(-10px);opacity:0; }}
    to   {{ transform:translateY(0);    opacity:1; }}
}}
@keyframes sbUp {{
    from {{ transform:translateY(8px);opacity:0; }}
    to   {{ transform:translateY(0);   opacity:1; }}
}}
@keyframes avatarPulse {{
    0%,100% {{ box-shadow:0 4px 14px rgba(76,175,80,.35); }}
    50%      {{ box-shadow:0 4px 22px rgba(76,175,80,.65); }}
}}
@keyframes floatIcon {{
    0%,100% {{ transform:translateY(0); }}
    50%      {{ transform:translateY(-5px); }}
}}

/* ── Profile header ── */
.sb-profile {{
    padding:18px 14px 14px;
    display:flex;align-items:center;gap:11px;
    background:{PROF_BG};
    border-bottom:1px solid {DIVIDER};
    animation:sbDown .38s cubic-bezier(0.16,1,0.3,1) both;
}}
.sb-avatar {{
    width:46px;height:46px;border-radius:14px;flex-shrink:0;
    background:linear-gradient(135deg,#2e7d32,#66bb6a);
    display:flex;align-items:center;justify-content:center;
    font-size:20px;font-weight:900;color:#fff!important;
    animation:avatarPulse 3s ease-in-out infinite;
    letter-spacing:0;
}}
.sb-prof-info {{ min-width:0;flex:1; }}
.sb-prof-name {{
    font-size:14px;font-weight:800;
    color:{TXT}!important;line-height:1.25;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}}
.sb-prof-email {{
    font-size:10.5px;color:{MUTED}!important;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
    margin-top:2px;
}}
.sb-streak-badge {{
    flex-shrink:0;margin-left:2px;
    display:{streak_vis};align-items:center;gap:3px;
    background:rgba(255,152,0,0.14);
    border:1px solid rgba(255,152,0,0.28);
    border-radius:10px;padding:4px 7px;
    font-size:11.5px;font-weight:800;
    color:#ffb74d!important;white-space:nowrap;
    animation:sbDown .38s .06s cubic-bezier(0.16,1,0.3,1) both;
}}

/* ── Section label ── */
.sb-sec-label {{
    font-size:10px;font-weight:800;letter-spacing:1.3px;
    text-transform:uppercase;color:{MUTED}!important;
    padding:14px 14px 6px;
    animation:sbUp .38s cubic-bezier(0.16,1,0.3,1) both;
}}

/* ── Stats row (Home) ── */
.sb-stats-row {{
    display:grid;grid-template-columns:repeat(3,1fr);
    gap:7px;padding:0 10px 10px;
    animation:sbUp .38s .05s cubic-bezier(0.16,1,0.3,1) both;
}}
.sb-stat {{
    background:{STAT_BG};border:1px solid {STAT_BDR};
    border-radius:12px;padding:10px 6px;text-align:center;
    transition:transform .15s ease;
}}
.sb-stat:hover {{ transform:translateY(-2px); }}
.sb-stat-val {{
    font-size:15px;font-weight:900;line-height:1.1;
    color:{ACT_C}!important;
}}
.sb-stat-lbl {{
    font-size:9px;font-weight:700;color:{MUTED}!important;
    text-transform:uppercase;letter-spacing:.4px;margin-top:3px;
}}

/* ── Daily goal bar (Home) ── */
.sb-goal-wrap {{
    padding:0 10px 12px;
    animation:sbUp .38s .09s cubic-bezier(0.16,1,0.3,1) both;
}}
.sb-goal-hdr {{
    display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;
}}
.sb-goal-lbl {{ font-size:11px;font-weight:700;color:{TXT}!important; }}
.sb-goal-pct {{ font-size:12px;font-weight:800; }}
.sb-track {{
    height:6px;background:{GOAL_TRACK};
    border-radius:6px;overflow:hidden;
}}
.sb-fill {{
    height:100%;border-radius:6px;
    transition:width .7s cubic-bezier(0.34,1.56,0.64,1);
}}
.sb-goal-sub {{
    font-size:10px;font-weight:600;color:{MUTED}!important;
    margin-top:4px;text-align:right;
}}

/* ── Schedule card ── */
.sb-sched-card {{
    margin:0 10px 12px;border:1px solid;
    border-radius:14px;padding:12px 14px;
    animation:sbUp .38s .05s cubic-bezier(0.16,1,0.3,1) both;
}}
.sb-sched-row {{ display:flex;align-items:center;justify-content:space-between; }}
.sb-sched-count {{
    font-size:26px;font-weight:900;line-height:1;
}}
.sb-sched-of {{
    font-size:16px;font-weight:600;color:{MUTED}!important;
}}
.sb-sched-lbl {{
    font-size:10px;font-weight:700;color:{MUTED}!important;
    text-transform:uppercase;letter-spacing:.5px;margin-top:3px;
}}
.sb-ring-svg {{ flex-shrink:0; }}

/* ── About card ── */
.sb-about-card {{
    margin:0 10px 8px;border:1px solid;
    border-radius:14px;padding:12px 14px;
    display:flex;align-items:center;gap:12px;
    animation:sbUp .38s .05s cubic-bezier(0.16,1,0.3,1) both;
}}
.sb-about-icon {{
    font-size:28px;
    animation:floatIcon 3s ease-in-out infinite;
}}
.sb-about-name {{ font-size:14px;font-weight:800; }}
.sb-about-meta {{ font-size:10px;font-weight:600;margin-top:2px; }}
.sb-made {{
    font-size:10.5px;font-weight:600;text-align:center;
    padding:0 14px 12px;
    animation:sbUp .38s .08s cubic-bezier(0.16,1,0.3,1) both;
}}

/* ── Divider ── */
.sb-hr {{
    height:1px;background:{DIVIDER};
    margin:2px 10px 6px;
}}

/* ── Navigation: override Streamlit page_link ── */
section[data-testid="stSidebar"] [data-testid="stPageLink"] {{
    margin:0 6px!important;
}}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a {{
    display:flex!important;align-items:center!important;
    gap:9px!important;
    padding:9px 12px!important;
    border-radius:11px!important;
    font-size:13.5px!important;font-weight:600!important;
    color:{MUTED}!important;
    text-decoration:none!important;
    border:1px solid transparent!important;
    transition:background .17s ease,color .17s ease,
               padding-left .17s ease,border-color .17s ease!important;
    margin-bottom:2px!important;
}}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {{
    background:{NAV_HOV}!important;
    color:{TXT}!important;
    padding-left:16px!important;
    border-color:{NAV_BDR_HOV}!important;
}}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {{
    background:{ACT_BG}!important;
    color:{ACT_C}!important;font-weight:700!important;
    border-color:rgba(76,175,80,0.28)!important;
    box-shadow:0 2px 12px rgba(76,175,80,0.13)!important;
    padding-left:14px!important;
}}

/* ── All sidebar Streamlit buttons ── */
section[data-testid="stSidebar"] .stButton>button {{
    font-family:'Inter',system-ui,sans-serif!important;
    border-radius:10px!important;
    font-size:12.5px!important;font-weight:700!important;
    min-height:34px!important;
    padding:4px 8px!important;
    border:1.5px solid {BTN_BDR}!important;
    background:{BTN_BG}!important;
    color:{TXT}!important;
    transition:all .16s ease!important;
    width:100%!important;
}}
section[data-testid="stSidebar"] .stButton>button:hover {{
    transform:translateY(-1px)!important;
    box-shadow:0 3px 10px rgba(0,0,0,0.12)!important;
    border-color:rgba(76,175,80,0.35)!important;
    color:{ACT_C}!important;
}}
/* Primary (active lang) */
section[data-testid="stSidebar"] .stButton>button[kind="primaryFormSubmit"],
section[data-testid="stSidebar"] .stButton>button[kind="primary"] {{
    background:{ACT_BG}!important;
    border-color:rgba(76,175,80,0.38)!important;
    color:{ACT_C}!important;
    box-shadow:0 0 0 2px rgba(76,175,80,0.12)!important;
}}
/* Sign-out button */
section[data-testid="stSidebar"] [data-testid="sb_logout_btn"]>button {{
    background:{SIGN_BG}!important;
    border-color:{SIGN_BDR}!important;
    color:{SIGN_C}!important;
}}
section[data-testid="stSidebar"] [data-testid="sb_logout_btn"]>button:hover {{
    background:rgba(239,83,80,0.18)!important;
    color:{SIGN_C}!important;
}}

/* ── Caption text ── */
section[data-testid="stSidebar"] .stCaption p {{
    font-size:9.5px!important;font-weight:800!important;
    letter-spacing:1.1px!important;text-transform:uppercase!important;
    color:{MUTED}!important;padding:10px 4px 2px!important;margin:0!important;
}}

/* ── Dividers ── */
section[data-testid="stSidebar"] [data-testid="stDivider"] {{
    margin:4px 0!important;border-color:{DIVIDER}!important;
}}

/* ── Columns: tighten gap ── */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {{
    gap:5px!important;padding:0 10px!important;
}}

/* ── Scroll padding ── */
section[data-testid="stSidebar"] > div:first-child > div:first-child {{
    padding-bottom:24px!important;
}}
</style>

<!-- ── Profile header ── -->
<div class="sb-profile">
  <div class="sb-avatar">{initials}</div>
  <div class="sb-prof-info">
    <div class="sb-prof-name">{user_name}</div>
    <div class="sb-prof-email">{user_email or "—"}</div>
  </div>
  <div class="sb-streak-badge">🔥&nbsp;{streak}</div>
</div>

<!-- ── Page-specific content ── -->
{page_card}

<div class="sb-hr"></div>
""", unsafe_allow_html=True)

        # ── Navigation ────────────────────────────────────
        st.caption("📍 MENU")
        st.page_link("Home.py",              label=f"⏱️  {t('nav_timer')}")
        st.page_link("pages/01_Schedule.py", label=f"📅  {t('nav_schedule')}")
        st.page_link("pages/02_About.py",    label=f"✨  {t('nav_about')}")

        st.markdown('<div class="sb-hr" style="margin-top:6px"></div>', unsafe_allow_html=True)

        # ── Settings ──────────────────────────────────────
        st.caption(f"⚙️ {t('settings')}")

        # Language pills — active one gets "primary" type
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("بادینی", type="primary" if lang == "badini" else "secondary",
                         key="sb_ba", use_container_width=True):
                st.session_state.lang = "badini"
                save_preferences(); st.rerun()
        with c2:
            if st.button("English", type="primary" if lang == "english" else "secondary",
                         key="sb_en", use_container_width=True):
                st.session_state.lang = "english"
                save_preferences(); st.rerun()
        with c3:
            if st.button("عربية", type="primary" if lang == "arabic" else "secondary",
                         key="sb_ar", use_container_width=True):
                st.session_state.lang = "arabic"
                save_preferences(); st.rerun()

        # Dark / Light toggle
        if st.button(toggle_lbl, key="sb_dark_btn", use_container_width=True):
            st.session_state.dark_mode = not is_dark
            save_preferences(); st.rerun()

        st.markdown('<div class="sb-hr" style="margin-top:8px"></div>', unsafe_allow_html=True)

        # ── Sign out ──────────────────────────────────────
        st.button("🔓 " + t("logout"), key="sb_logout_btn",
                  use_container_width=True, on_click=st.logout)


render_sidebar(_active)


# ══════════════════════════════════════════════════════════
#  CUSTOM NAV BAR
# ══════════════════════════════════════════════════════════
def render_nav(active: str):
    is_dark   = st.session_state.get("dark_mode", True)
    lang      = st.session_state.get("lang", "badini")
    dark_icon = "☀️" if is_dark else "🌙"
    lang_abbr = {"badini": "BA", "english": "EN", "arabic": "AR"}.get(lang, "EN")
    user_name = t("student")
    if st.user.is_logged_in:
        user_name = (st.user.name or st.user.email or t("student"))[:20]

    try:
        with open("logo.png", "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="rd-logo" alt="logo">'
    except FileNotFoundError:
        logo_html = '<span class="rd-logo-emoji">📚</span>'

    if is_dark:
        NAV_BG   = "rgba(13,11,36,0.96)"
        NAV_BDR  = "rgba(255,255,255,0.08)"
        NAV_SH   = "0 4px 32px rgba(0,0,0,0.60),0 1px 0 rgba(255,255,255,0.04)"
        TXT      = "#ececec"
        MUTED    = "rgba(255,255,255,0.42)"
        ACT_BG   = "rgba(76,175,80,0.18)"
        ACT_C    = "#7ec87f"
        HOV_BG   = "rgba(255,255,255,0.07)"
        PILL_BG  = "rgba(255,255,255,0.06)"
        PILL_BDR = "rgba(255,255,255,0.10)"
        HAM_BG   = "rgba(76,175,80,0.14)"
        HAM_BDR  = "rgba(76,175,80,0.40)"
        HAM_C    = "#7ec87f"
        BTN_BG   = "rgba(255,255,255,0.06)"
        BTN_BDR  = "rgba(255,255,255,0.10)"
        BTN_HOV  = "rgba(76,175,80,0.20)"
    else:
        NAV_BG   = "rgba(255,255,255,0.97)"
        NAV_BDR  = "rgba(0,0,0,0.08)"
        NAV_SH   = "0 4px 24px rgba(0,0,0,0.12),0 1px 0 rgba(0,0,0,0.04)"
        TXT      = "#18182a"
        MUTED    = "rgba(0,0,0,0.44)"
        ACT_BG   = "rgba(46,125,50,0.12)"
        ACT_C    = "#2e7d32"
        HOV_BG   = "rgba(0,0,0,0.05)"
        PILL_BG  = "rgba(0,0,0,0.05)"
        PILL_BDR = "rgba(0,0,0,0.09)"
        HAM_BG   = "rgba(46,125,50,0.11)"
        HAM_BDR  = "rgba(46,125,50,0.32)"
        HAM_C    = "#2e7d32"
        BTN_BG   = "rgba(0,0,0,0.05)"
        BTN_BDR  = "rgba(0,0,0,0.09)"
        BTN_HOV  = "rgba(76,175,80,0.12)"

    ha = " nav-active" if active == "home"     else ""
    sa = " nav-active" if active == "schedule" else ""
    aa = " nav-active" if active == "about"    else ""
    nt, ns, na = t("nav_timer"), t("nav_schedule"), t("nav_about")

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

header[data-testid="stHeader"] {{
    height:0!important;min-height:0!important;
    overflow:visible!important;background:transparent!important;
    box-shadow:none!important;border:none!important;padding:0!important;
}}
[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"],#MainMenu,footer{{display:none!important;}}

[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapse"],
[data-testid="stSidebarCollapseButton"] {{
    position:fixed!important;top:-9999px!important;left:-9999px!important;
    width:1px!important;height:1px!important;
    opacity:0!important;pointer-events:auto!important;overflow:hidden!important;
}}

#rd-ham {{
    position:fixed!important;top:8px!important;left:10px!important;
    z-index:2200000!important;width:36px!important;height:36px!important;
    background:{HAM_BG}!important;border:1.5px solid {HAM_BDR}!important;
    border-radius:10px!important;cursor:pointer!important;
    display:flex!important;align-items:center!important;justify-content:center!important;
    box-shadow:0 2px 12px rgba(0,0,0,.22)!important;
    transition:background .18s,border-color .18s,box-shadow .18s,transform .14s!important;
    outline:none!important;-webkit-tap-highlight-color:transparent!important;
    padding:0!important;margin:0!important;
}}
#rd-ham:hover {{
    background:rgba(76,175,80,.28)!important;border-color:rgba(76,175,80,.65)!important;
    box-shadow:0 0 16px rgba(76,175,80,.38)!important;transform:scale(1.07)!important;
}}
#rd-ham:active{{transform:scale(0.91)!important;}}
#rd-ham svg{{pointer-events:none;}}

.rd-nav {{
    position:fixed;top:0;left:0;right:0;height:52px;
    display:flex;align-items:center;justify-content:space-between;
    padding:0 12px 0 56px;
    background:{NAV_BG};border-bottom:1px solid {NAV_BDR};box-shadow:{NAV_SH};
    backdrop-filter:blur(28px) saturate(1.6);-webkit-backdrop-filter:blur(28px) saturate(1.6);
    z-index:1500000;font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;
    box-sizing:border-box;animation:rdSlideDown .48s cubic-bezier(0.16,1,0.3,1) both;
}}
@keyframes rdSlideDown {{
    from{{transform:translateY(-100%);opacity:0;}}
    to  {{transform:translateY(0);    opacity:1;}}
}}
.rd-brand {{
    display:flex;align-items:center;gap:7px;flex-shrink:0;
    text-decoration:none!important;cursor:pointer;
    padding:4px 6px;border-radius:8px;transition:background .18s;
}}
.rd-brand:hover{{background:{HOV_BG};}}
.rd-logo,.rd-logo-emoji {{
    width:24px;height:24px;border-radius:6px;font-size:22px;
    filter:drop-shadow(0 0 4px rgba(76,175,80,.35));
    transition:transform .28s cubic-bezier(0.34,1.56,0.64,1),filter .25s;
}}
.rd-brand:hover .rd-logo,.rd-brand:hover .rd-logo-emoji {{
    transform:translateY(-3px) scale(1.12);
    filter:drop-shadow(0 0 10px rgba(76,175,80,.80));
}}
.rd-name {{
    font-size:14px;font-weight:800;letter-spacing:-0.3px;color:{TXT};transition:color .22s;
}}
.rd-brand:hover .rd-name{{color:{ACT_C};}}
.rd-dot {{
    width:7px;height:7px;border-radius:50%;flex-shrink:0;
    background:#4caf50;box-shadow:0 0 5px 1px rgba(76,175,80,.55);
    animation:dotBreath 2.4s ease-in-out infinite;
}}
@keyframes dotBreath {{
    0%,100%{{transform:scale(1);   box-shadow:0 0 4px 1px rgba(76,175,80,.50);opacity:.9;}}
    40%     {{transform:scale(1.8); box-shadow:0 0 12px 5px rgba(76,175,80,.80),0 0 20px 7px rgba(76,175,80,.25);opacity:1;}}
    70%     {{transform:scale(0.55);box-shadow:0 0 2px 0 rgba(76,175,80,.25);opacity:.65;}}
}}
.rd-links {{
    display:flex;align-items:center;gap:2px;
    position:absolute;left:50%;transform:translateX(-50%);
}}
.rd-link {{
    font-size:13px;font-weight:500;color:{MUTED}!important;
    padding:6px 12px;border-radius:9px;cursor:pointer;white-space:nowrap;
    text-decoration:none!important;position:relative;
    transition:background .17s,color .17s,box-shadow .17s;
}}
.rd-link::after {{
    content:'';position:absolute;bottom:4px;left:50%;transform:translateX(-50%);
    width:0;height:2px;background:{ACT_C};border-radius:1px;
    transition:width .22s cubic-bezier(0.25,1,0.5,1);
}}
.rd-link:hover{{background:{HOV_BG}!important;color:{TXT}!important;}}
.rd-link:hover::after{{width:50%;}}
.rd-link.nav-active{{
    background:{ACT_BG}!important;color:{ACT_C}!important;font-weight:700!important;
    box-shadow:0 0 14px rgba(76,175,80,.18),inset 0 0 10px rgba(76,175,80,.07);
}}
.rd-link.nav-active::after{{width:58%;}}
.rd-link:nth-child(1){{animation:rdFadeUp .44s .08s cubic-bezier(0.16,1,0.3,1) both;}}
.rd-link:nth-child(2){{animation:rdFadeUp .44s .15s cubic-bezier(0.16,1,0.3,1) both;}}
.rd-link:nth-child(3){{animation:rdFadeUp .44s .22s cubic-bezier(0.16,1,0.3,1) both;}}
@keyframes rdFadeUp {{
    from{{transform:translateY(7px);opacity:0;}}
    to  {{transform:translateY(0);  opacity:1;}}
}}
.rd-right {{
    display:flex;align-items:center;gap:4px;flex-shrink:0;
    animation:rdFadeUp .44s .28s cubic-bezier(0.16,1,0.3,1) both;
}}
.rd-user {{
    font-size:11px;font-weight:600;color:{MUTED}!important;
    background:{PILL_BG};border:1px solid {PILL_BDR};
    padding:3px 9px;border-radius:20px;
    max-width:100px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
}}
.rd-btn {{
    display:inline-flex;align-items:center;justify-content:center;
    font-size:13px;cursor:pointer;background:{BTN_BG};border:1px solid {BTN_BDR};
    color:{MUTED}!important;padding:4px 9px;border-radius:8px;
    transition:background .17s,color .17s,box-shadow .17s,transform .12s,border-color .17s;
    text-decoration:none!important;white-space:nowrap;min-height:28px;line-height:1;font-family:inherit;
}}
.rd-btn:hover {{
    background:{BTN_HOV}!important;color:{ACT_C}!important;
    border-color:rgba(76,175,80,.38)!important;
    box-shadow:0 0 10px rgba(76,175,80,.20)!important;transform:translateY(-1px);
}}
.rd-btn:active{{transform:scale(0.93);}}
.main .block-container,
section[data-testid="stMain"] .block-container{{padding-top:68px!important;}}
@media(max-width:600px){{
    .rd-nav{{padding:0 8px 0 56px!important;height:48px;}}
    .rd-name,.rd-dot,.rd-user{{display:none!important;}}
    .rd-link{{font-size:11px!important;padding:5px 7px!important;}}
    .rd-btn{{font-size:11px!important;padding:3px 7px!important;}}
}}
@media(max-width:380px){{
    .rd-link{{font-size:10px!important;padding:4px 5px!important;}}
    .rd-right{{gap:2px;}}
}}
</style>

<button id="rd-ham" aria-label="Toggle sidebar" title="Open menu">
  <svg width="18" height="18" viewBox="0 0 18 18" fill="{HAM_C}" xmlns="http://www.w3.org/2000/svg">
    <rect y="3"  width="18" height="2" rx="1"/>
    <rect y="8"  width="13" height="2" rx="1"/>
    <rect y="13" width="18" height="2" rx="1"/>
  </svg>
</button>

<div class="rd-nav">
  <a class="rd-brand" href="/" target="_self">
    {logo_html}
    <span class="rd-name">Rekxare Dami</span>
    <span class="rd-dot"></span>
  </a>
  <div class="rd-links">
    <a class="rd-link{ha}" href="/"         target="_self">⏱️ {nt}</a>
    <a class="rd-link{sa}" href="/schedule" target="_self">📅 {ns}</a>
    <a class="rd-link{aa}" href="/about"    target="_self">✨ {na}</a>
  </div>
  <div class="rd-right">
    <span class="rd-user">👤 {user_name}</span>
    <a class="rd-btn" href="?dark_mode=1" target="_self" title="Toggle dark/light">{dark_icon}</a>
    <a class="rd-btn" href="?lang=cycle"  target="_self" title="Cycle language">{lang_abbr}</a>
  </div>
</div>
""", unsafe_allow_html=True)


render_nav(_active)


# ══════════════════════════════════════════════════════════
#  SIDEBAR TOGGLE — iframe JS (bypasses main-page CSP)
# ══════════════════════════════════════════════════════════
components.html("""
<script>
(function() {
  var LS  = 'rdSB';
  var p   = window.parent.document;

  function getSB()    { return p.querySelector('section[data-testid="stSidebar"]'); }
  function wantOpen() { try { return window.parent.localStorage.getItem(LS)==='1'; } catch(e){return false;} }
  function setWant(v) { try { window.parent.localStorage.setItem(LS, v?'1':'0'); } catch(e){} }

  function openSB() {
    setWant(true);
    p.body.classList.add('rd-sb-open');
    var sb = getSB();
    if (sb) {
      sb.style.setProperty('transform',  'translateX(0)', 'important');
      sb.style.setProperty('visibility', 'visible',       'important');
      sb.style.setProperty('display',    'flex',          'important');
      sb.style.setProperty('min-width',  '244px',         'important');
    }
  }
  function closeSB() {
    setWant(false);
    p.body.classList.remove('rd-sb-open');
    var sb = getSB();
    if (sb) {
      sb.style.removeProperty('transform');
      sb.style.removeProperty('visibility');
      sb.style.removeProperty('display');
      sb.style.removeProperty('min-width');
    }
  }
  function isOpen() {
    var sb = getSB(); if (!sb) return false;
    var r = sb.getBoundingClientRect();
    return r.left > -50 && r.width > 50;
  }

  function wireHam() {
    var h = p.getElementById('rd-ham');
    if (!h) { setTimeout(wireHam, 120); return; }
    if (h.__rdWired) return;
    h.__rdWired = true;
    h.addEventListener('click', function(){ isOpen() ? closeSB() : openSB(); });
  }

  /* Re-apply open state after Streamlit reruns rebuild the DOM */
  setInterval(function(){
    if (!wantOpen()) return;
    if (!isOpen()) { openSB(); }
  }, 300);

  if (wantOpen()) openSB();
  wireHam();
  setTimeout(wireHam, 300);
  setTimeout(wireHam, 800);
})();
</script>
""", height=0)


# ══════════════════════════════════════════════════════════
#  RUN PAGE
# ══════════════════════════════════════════════════════════
pg.run()
