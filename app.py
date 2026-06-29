import streamlit as st
import json
import os
import hashlib
import base64
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
.ll{{font-size:72px;line-height:1;margin-bottom:12px;
    animation:lfloat 3s ease-in-out infinite,lglow 3s ease-in-out infinite;}}
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
#  SIDEBAR CONTENT
#
#  WHY THIS IS HERE:
#  When st.navigation(position="hidden") is used and nothing
#  calls st.sidebar, Streamlit does NOT render the sidebar
#  section in the DOM at all — so there is no toggle button
#  to click or style.  Adding at least one st.sidebar call
#  forces Streamlit to render the sidebar and its native
#  toggle button ([data-testid="stSidebarCollapsedControl"]).
#  That native button is then CSS-restyled to look like our
#  hamburger.  No JavaScript toggle hacks needed.
# ══════════════════════════════════════════════════════════
def render_sidebar():
    is_dark   = st.session_state.get("dark_mode", True)
    lang      = st.session_state.get("lang", "badini")
    dark_icon = "☀️" if is_dark else "🌙"
    lang_abbr = {"badini": "BA", "english": "EN", "arabic": "AR"}.get(lang, "EN")

    user_name = t("student") if not st.user.is_logged_in else (st.user.name or st.user.email or "")[:24]
    user_email = st.user.email if st.user.is_logged_in else ""

    with st.sidebar:
        # ── User card
        st.markdown(f"""
<div style="padding:12px 4px 4px;display:flex;align-items:center;gap:10px;margin-bottom:4px;">
  <div style="width:38px;height:38px;border-radius:50%;
              background:linear-gradient(135deg,#388e3c,#66bb6a);
              display:flex;align-items:center;justify-content:center;
              font-size:18px;flex-shrink:0;">👤</div>
  <div>
    <div style="font-weight:700;font-size:14px;line-height:1.3;">{user_name}</div>
    <div style="font-size:11px;opacity:0.55;word-break:break-all;">{user_email}</div>
  </div>
</div>
""", unsafe_allow_html=True)
        st.divider()

        # ── Navigation links
        st.markdown(f"**{t('nav_timer')}** · {t('nav_schedule')} · {t('nav_about')}"[:0] or "", unsafe_allow_html=False)
        st.page_link("Home.py",              label=f"⏱️  {t('nav_timer')}")
        st.page_link("pages/01_Schedule.py", label=f"📅  {t('nav_schedule')}")
        st.page_link("pages/02_About.py",    label=f"✨  {t('nav_about')}")
        st.divider()

        # ── Settings
        st.caption("⚙️ Settings")
        c1, c2 = st.columns(2)
        with c1:
            if st.button(dark_icon + " " + ("Light" if is_dark else "Dark"),
                         key="sb_dark_btn", use_container_width=True):
                st.session_state.dark_mode = not is_dark
                save_preferences()
                st.rerun()
        with c2:
            if st.button("🌐 " + lang_abbr,
                         key="sb_lang_btn", use_container_width=True):
                order = ["badini", "english", "arabic"]
                st.session_state.lang = order[(order.index(lang) + 1) % 3]
                save_preferences()
                st.rerun()

        st.divider()
        # ── Sign out
        c1, c2 = st.columns(2)
        with c2:
            st.button("🔓 Sign out", key="sb_logout_btn",
                      on_click=st.logout, use_container_width=True)


render_sidebar()


# ══════════════════════════════════════════════════════════
#  CUSTOM NAV BAR
# ══════════════════════════════════════════════════════════
def render_nav(active: str):
    is_dark   = st.session_state.get("dark_mode", True)
    lang      = st.session_state.get("lang", "badini")
    dark_icon = "☀️" if is_dark else "🌙"
    lang_abbr = {"badini": "BA", "english": "EN", "arabic": "AR"}.get(lang, "EN")

    user_name = "Student"
    if st.user.is_logged_in:
        raw = st.user.name or st.user.email or "Student"
        user_name = raw[:20]

    try:
        with open("logo.png", "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="rd-logo" alt="logo">'
    except FileNotFoundError:
        logo_html = '<span class="rd-logo-emoji">📚</span>'

    if is_dark:
        NAV_BG   = "rgba(13,11,36,0.96)"
        NAV_BDR  = "rgba(255,255,255,0.08)"
        NAV_SH   = "0 4px 32px rgba(0,0,0,0.60), 0 1px 0 rgba(255,255,255,0.04)"
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
        SB_BG    = "#0e0c24"
        SB_BDR   = "rgba(255,255,255,0.07)"
        SB_LNK   = "rgba(255,255,255,0.70)"
    else:
        NAV_BG   = "rgba(255,255,255,0.97)"
        NAV_BDR  = "rgba(0,0,0,0.08)"
        NAV_SH   = "0 4px 24px rgba(0,0,0,0.12), 0 1px 0 rgba(0,0,0,0.04)"
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
        SB_BG    = "#f4f6f8"
        SB_BDR   = "rgba(0,0,0,0.07)"
        SB_LNK   = "rgba(0,0,0,0.75)"

    ha = " nav-active" if active == "home"     else ""
    sa = " nav-active" if active == "schedule" else ""
    aa = " nav-active" if active == "about"    else ""

    nt = t("nav_timer")
    ns = t("nav_schedule")
    na = t("nav_about")

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── 1. Collapse Streamlit header strip ──────────────────────── */
header[data-testid="stHeader"] {{
    height: 0 !important; min-height: 0 !important;
    overflow: visible !important;
    background: transparent !important;
    box-shadow: none !important; border: none !important; padding: 0 !important;
}}
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], #MainMenu, footer {{ display: none !important; }}

/* ── 2. Sidebar panel styling ────────────────────────────────── */
section[data-testid="stSidebar"] {{
    background: {SB_BG} !important;
    border-right: 1px solid {SB_BDR} !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.18) !important;
}}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a {{
    color: {SB_LNK} !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 8px 12px !important;
    border-radius: 8px !important;
    display: block !important;
    text-decoration: none !important;
    transition: background .15s ease, color .15s ease !important;
    margin-bottom: 2px !important;
}}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a:hover {{
    background: {HAM_BG} !important; color: {ACT_C} !important;
}}
section[data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {{
    background: {ACT_BG} !important; color: {ACT_C} !important; font-weight: 700 !important;
}}
/* Style sidebar buttons */
section[data-testid="stSidebar"] .stButton > button {{
    background: {HAM_BG} !important; border: 1px solid {HAM_BDR} !important;
    color: {HAM_C} !important; border-radius: 8px !important;
    font-size: 12px !important; font-weight: 600 !important;
    transition: all .15s ease !important;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
    background: rgba(76,175,80,.25) !important;
    box-shadow: 0 0 10px rgba(76,175,80,.25) !important;
}}

/* ── 3. Native sidebar TOGGLE BUTTONS — restyled as hamburger ──
   KEY INSIGHT: render_sidebar() adds st.sidebar content which
   forces Streamlit to render these elements in the DOM.
   We restyle them in place — NO JS toggle needed, they always
   work because Streamlit owns their click handlers.
   ─────────────────────────────────────────────────────────── */

/* Shared hamburger appearance for all toggle variants */
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapse"],
[data-testid="stSidebarCollapseButton"] {{
    position: fixed !important;
    top: 8px !important; left: 10px !important;
    z-index: 2200000 !important;
    width: 36px !important; height: 36px !important;
    background: {HAM_BG} !important;
    border: 1.5px solid {HAM_BDR} !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important; justify-content: center !important;
    box-shadow: 0 2px 12px rgba(0,0,0,.22) !important;
    transition: background .18s ease, border-color .18s ease,
                box-shadow .18s ease, transform .14s ease !important;
    overflow: visible !important;
    padding: 0 !important; margin: 0 !important;
}}
[data-testid="stSidebarCollapsedControl"]:hover,
[data-testid="collapsedControl"]:hover,
[data-testid="stSidebarCollapse"]:hover,
[data-testid="stSidebarCollapseButton"]:hover {{
    background: rgba(76,175,80,.28) !important;
    border-color: rgba(76,175,80,.65) !important;
    box-shadow: 0 0 16px rgba(76,175,80,.38) !important;
    transform: scale(1.07) !important;
}}
[data-testid="stSidebarCollapsedControl"]:active,
[data-testid="collapsedControl"]:active,
[data-testid="stSidebarCollapse"]:active,
[data-testid="stSidebarCollapseButton"]:active {{
    transform: scale(0.91) !important;
}}
/* Inner <button> wrapper (some variants wrap in a button) */
[data-testid="stSidebarCollapsedControl"] button,
[data-testid="collapsedControl"] button,
[data-testid="stSidebarCollapse"] button,
[data-testid="stSidebarCollapseButton"] button {{
    all: unset !important;
    width: 100% !important; height: 100% !important;
    display: flex !important;
    align-items: center !important; justify-content: center !important;
    cursor: pointer !important;
}}
/* Hide Streamlit's native chevron icon */
[data-testid="stSidebarCollapsedControl"] svg,
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapse"] svg,
[data-testid="stSidebarCollapseButton"] svg {{
    display: none !important;
}}
/* Hamburger icon via ::before (works on button child or element itself) */
[data-testid="stSidebarCollapsedControl"] button::before,
[data-testid="collapsedControl"] button::before,
[data-testid="stSidebarCollapse"] button::before,
[data-testid="stSidebarCollapseButton"] button::before,
[data-testid="stSidebarCollapsedControl"]::after,
[data-testid="collapsedControl"]::after {{
    content: '' !important;
    display: block !important;
    width: 18px !important; height: 18px !important;
    background-color: {HAM_C} !important;
    -webkit-mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Crect y='3' width='18' height='2' rx='1'/%3E%3Crect y='8' width='13' height='2' rx='1'/%3E%3Crect y='13' width='18' height='2' rx='1'/%3E%3C/svg%3E") !important;
    mask-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Crect y='3' width='18' height='2' rx='1'/%3E%3Crect y='8' width='13' height='2' rx='1'/%3E%3Crect y='13' width='18' height='2' rx='1'/%3E%3C/svg%3E") !important;
    -webkit-mask-repeat: no-repeat !important; mask-repeat: no-repeat !important;
    -webkit-mask-size: contain !important; mask-size: contain !important;
    -webkit-mask-position: center !important; mask-position: center !important;
}}

/* ── 4. Nav bar ─────────────────────────────────────────────── */
.rd-nav {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 52px;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 12px 0 56px;
    background: {NAV_BG};
    border-bottom: 1px solid {NAV_BDR};
    box-shadow: {NAV_SH};
    backdrop-filter: blur(28px) saturate(1.6);
    -webkit-backdrop-filter: blur(28px) saturate(1.6);
    z-index: 1500000;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    box-sizing: border-box;
    animation: rdSlideDown 0.48s cubic-bezier(0.16,1,0.3,1) both;
}}
@keyframes rdSlideDown {{
    from {{ transform: translateY(-100%); opacity: 0; }}
    to   {{ transform: translateY(0);     opacity: 1; }}
}}

/* Brand */
.rd-brand {{
    display: flex; align-items: center; gap: 7px; flex-shrink: 0;
    text-decoration: none !important; cursor: pointer;
    padding: 4px 6px; border-radius: 8px;
    transition: background .18s ease;
}}
.rd-brand:hover {{ background: {HOV_BG}; }}
.rd-logo {{
    width: 24px; height: 24px; border-radius: 6px;
    filter: drop-shadow(0 0 4px rgba(76,175,80,.35));
    transition: transform .28s cubic-bezier(0.34,1.56,0.64,1), filter .25s ease;
}}
.rd-logo-emoji {{
    font-size: 22px;
    filter: drop-shadow(0 0 4px rgba(76,175,80,.35));
    transition: transform .28s cubic-bezier(0.34,1.56,0.64,1), filter .25s ease;
}}
.rd-brand:hover .rd-logo,
.rd-brand:hover .rd-logo-emoji {{
    transform: translateY(-3px) scale(1.12);
    filter: drop-shadow(0 0 10px rgba(76,175,80,.80));
}}
.rd-name {{
    font-size: 14px; font-weight: 800; letter-spacing: -0.3px; color: {TXT};
    transition: color .22s ease;
}}
.rd-brand:hover .rd-name {{ color: {ACT_C}; }}

/* Subtle breathing dot */
.rd-dot {{
    width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
    background: #4caf50;
    box-shadow: 0 0 5px 1px rgba(76,175,80,.50);
    animation: dotBreath 3.5s ease-in-out infinite;
}}
@keyframes dotBreath {{
    0%, 100% {{ transform: scale(1);    opacity: 0.85; box-shadow: 0 0 4px 1px rgba(76,175,80,.45); }}
    50%       {{ transform: scale(1.35); opacity: 1;    box-shadow: 0 0 8px 3px rgba(76,175,80,.60); }}
}}

/* Centered nav links */
.rd-links {{
    display: flex; align-items: center; gap: 2px;
    position: absolute; left: 50%; transform: translateX(-50%);
}}
.rd-link {{
    font-size: 13px; font-weight: 500;
    color: {MUTED} !important;
    padding: 6px 12px; border-radius: 9px;
    transition: background .17s ease, color .17s ease, box-shadow .17s ease;
    cursor: pointer; white-space: nowrap;
    text-decoration: none !important;
    position: relative;
}}
.rd-link::after {{
    content: '';
    position: absolute; bottom: 4px; left: 50%;
    transform: translateX(-50%);
    width: 0; height: 2px;
    background: {ACT_C};
    border-radius: 1px;
    transition: width .22s cubic-bezier(0.25,1,0.5,1);
}}
.rd-link:hover {{ background: {HOV_BG} !important; color: {TXT} !important; }}
.rd-link:hover::after {{ width: 50%; }}
.rd-link.nav-active {{
    background: {ACT_BG} !important; color: {ACT_C} !important;
    font-weight: 700 !important;
    box-shadow: 0 0 14px rgba(76,175,80,.18), inset 0 0 10px rgba(76,175,80,.07);
}}
.rd-link.nav-active::after {{ width: 58%; }}
.rd-link:nth-child(1) {{ animation: rdFadeUp .44s .08s cubic-bezier(0.16,1,0.3,1) both; }}
.rd-link:nth-child(2) {{ animation: rdFadeUp .44s .15s cubic-bezier(0.16,1,0.3,1) both; }}
.rd-link:nth-child(3) {{ animation: rdFadeUp .44s .22s cubic-bezier(0.16,1,0.3,1) both; }}
@keyframes rdFadeUp {{
    from {{ transform: translateY(7px); opacity: 0; }}
    to   {{ transform: translateY(0);   opacity: 1; }}
}}

/* Right controls */
.rd-right {{
    display: flex; align-items: center; gap: 4px; flex-shrink: 0;
    animation: rdFadeUp .44s .28s cubic-bezier(0.16,1,0.3,1) both;
}}
.rd-user {{
    font-size: 11px; font-weight: 600;
    color: {MUTED} !important;
    background: {PILL_BG}; border: 1px solid {PILL_BDR};
    padding: 3px 9px; border-radius: 20px;
    max-width: 100px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}}
.rd-btn {{
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 13px; cursor: pointer;
    background: {BTN_BG}; border: 1px solid {BTN_BDR};
    color: {MUTED} !important;
    padding: 4px 9px; border-radius: 8px;
    transition: background .17s ease, color .17s ease,
                box-shadow .17s ease, transform .12s ease, border-color .17s ease;
    text-decoration: none !important; white-space: nowrap;
    min-height: 28px; line-height: 1; font-family: inherit;
}}
.rd-btn:hover {{
    background: {BTN_HOV} !important; color: {ACT_C} !important;
    border-color: rgba(76,175,80,.38) !important;
    box-shadow: 0 0 10px rgba(76,175,80,.20) !important;
    transform: translateY(-1px);
}}
.rd-btn:active {{ transform: scale(0.93); }}

/* Content padding */
.main .block-container,
section[data-testid="stMain"] .block-container {{ padding-top: 68px !important; }}

/* Mobile */
@media (max-width: 600px) {{
    .rd-nav  {{ padding: 0 8px 0 56px !important; height: 48px; }}
    .rd-name {{ display: none !important; }}
    .rd-dot  {{ display: none !important; }}
    .rd-user {{ display: none !important; }}
    .rd-link {{ font-size: 11px !important; padding: 5px 7px !important; }}
    .rd-btn  {{ font-size: 11px !important; padding: 3px 7px !important; }}
}}
@media (max-width: 380px) {{
    .rd-link  {{ font-size: 10px !important; padding: 4px 5px !important; }}
    .rd-right {{ gap: 2px; }}
}}
</style>

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
#  RUN THE CURRENT PAGE
# ══════════════════════════════════════════════════════════
pg.run()
