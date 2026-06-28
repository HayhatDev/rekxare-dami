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


# ── Preference helpers ──
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
#  PAGE CONFIG  (called ONCE — pages must NOT call it)
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Rekxare Dami",
    page_icon="logo.png",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── PWA tags ──
st.markdown("""
<link rel="manifest" href="/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#1a1a2e">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js');
  }
</script>
""", unsafe_allow_html=True)

# ── Wire user session + load preferences ──
if st.user.is_logged_in:
    if "user_email" not in st.session_state or not st.session_state.user_email:
        st.session_state.user_email = st.user.email
        st.session_state.data_key   = hashlib.md5(st.user.email.encode()).hexdigest()[:8]
        st.session_state.logged_in  = True
    st.session_state.data_key = st.user.email.split("@")[0]
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
header[data-testid="stHeader"],#MainMenu,footer,
[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"],[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],[data-testid="collapsedControl"]{{
    display:none!important;
}}
.main .block-container{{
    padding-top:max(20px,calc(50vh - 260px))!important;
    padding-bottom:40px!important;padding-left:20px!important;
    padding-right:20px!important;max-width:480px!important;
}}
.lw{{width:100%;display:flex;flex-direction:column;align-items:center;}}
.ll{{font-size:72px;line-height:1;margin-bottom:12px;filter:drop-shadow(0 4px 16px rgba(76,175,80,.4));animation:fl 3s ease-in-out infinite;}}
@keyframes fl{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-8px);}}}}
.lt{{font-size:32px;font-weight:900;letter-spacing:-.8px;color:#fff;text-align:center;margin-bottom:4px;}}
.ls{{font-size:14px;color:rgba(255,255,255,.55);text-align:center;margin-bottom:24px;font-weight:500;}}
.lb{{display:inline-flex;align-items:center;gap:6px;background:rgba(76,175,80,.15);border:1px solid rgba(76,175,80,.25);color:#81c784;border-radius:20px;padding:5px 14px;font-size:11px;font-weight:700;letter-spacing:.5px;margin-bottom:24px;}}
.lc{{background:rgba(0,0,0,.5);border:1.5px solid rgba(255,255,255,.13);border-radius:28px;padding:32px 28px 28px;width:100%;backdrop-filter:blur(12px);box-shadow:0 8px 40px rgba(0,0,0,.40);}}
.stButton>button{{background:linear-gradient(135deg,#388e3c,#4caf50)!important;color:#fff!important;border:none!important;border-radius:40px!important;font-weight:700!important;font-size:14px!important;min-height:44px!important;box-shadow:0 2px 8px rgba(76,175,80,.3)!important;transition:all .18s ease!important;width:100%!important;}}
.stButton>button:hover{{transform:translateY(-2px)!important;box-shadow:0 6px 16px rgba(76,175,80,.45)!important;filter:brightness(1.05)!important;}}
.lc .stButton>button{{font-size:16px!important;min-height:52px!important;box-shadow:0 4px 18px rgba(76,175,80,.35)!important;}}
.dv{{display:flex;align-items:center;gap:12px;margin:24px 0 20px;color:rgba(255,255,255,.35);font-size:12px;font-weight:600;}}
.dv::before,.dv::after{{content:"";flex:1;height:1px;background:rgba(255,255,255,.15);}}
.lf{{font-size:12px;color:rgba(255,255,255,.30);text-align:center;margin-top:24px;}}
</style>
<div class="lw">
  <div class="ll">📚</div>
  <div class="lt">Rekxare Dami</div>
  <div class="ls">{t('login_sub')}</div>
  <div class="lb">{t('login_badge')}</div>
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
#  QUERY PARAM HANDLERS  (dark mode, language, page switching)
# ══════════════════════════════════════════════════════════
if "dark_mode" in st.query_params:
    st.session_state.dark_mode = not st.session_state.get("dark_mode", True)
    save_preferences()
    st.query_params.clear()
    st.rerun()

if "lang" in st.query_params and st.query_params["lang"] == "cycle":
    order = ["badini", "english", "arabic"]
    cur   = st.session_state.get("lang", "badini")
    st.session_state.lang = order[(order.index(cur) + 1) % 3] if cur in order else "badini"
    save_preferences()
    st.query_params.clear()
    st.rerun()

# ── PAGE SWITCHING (simple & reliable) ──
page_param = st.query_params.get("page")
if page_param == "schedule":
    st.query_params.clear()
    st.switch_page("pages/01_Schedule.py")
    st.stop()
elif page_param == "about":
    st.query_params.clear()
    st.switch_page("pages/02_About.py")
    st.stop()
# Otherwise stay on Home (default)

# ══════════════════════════════════════════════════════════
#  NAV BAR – Clean, simple, with slide-down animation
# ══════════════════════════════════════════════════════════
def render_nav():
    is_dark = st.session_state.get("dark_mode", True)
    lang    = st.session_state.get("lang", "badini")
    active  = st.session_state.get("current_page", "home")

    dark_icon = "☀️" if is_dark else "🌙"
    lang_abbr = {"badini": "BA", "english": "EN", "arabic": "AR"}.get(lang, "EN")
    user_name = (st.user.name or "Student")[:22] if st.user.is_logged_in else t("student")

    try:
        with open("logo.png", "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width:24px;height:24px;border-radius:5px;vertical-align:middle;filter:drop-shadow(0 0 5px rgba(76,175,80,.4));" alt="">'
    except FileNotFoundError:
        logo_html = "📚"

    # ── Theme tokens ──
    if is_dark:
        B  = "#0d0b24"
        Bd = "rgba(255,255,255,0.07)"
        T  = "#ececec"
        M  = "rgba(255,255,255,0.40)"
        A  = "rgba(76,175,80,0.18)"
        Ac = "#7ec87f"
        H  = "rgba(255,255,255,0.07)"
        Pb = "rgba(255,255,255,0.05)"
        Pd = "rgba(255,255,255,0.09)"
        Sh = "0 4px 24px rgba(0,0,0,0.55)"
        Sb = "rgba(76,175,80,0.13)"
        Sd = "rgba(76,175,80,0.32)"
        Sc = "#7ec87f"
    else:
        B  = "#ffffff"
        Bd = "rgba(0,0,0,0.08)"
        T  = "#18182a"
        M  = "rgba(0,0,0,0.44)"
        A  = "rgba(46,125,50,0.12)"
        Ac = "#2e7d32"
        H  = "rgba(0,0,0,0.05)"
        Pb = "rgba(0,0,0,0.04)"
        Pd = "rgba(0,0,0,0.09)"
        Sh = "0 4px 20px rgba(0,0,0,0.10)"
        Sb = "rgba(46,125,50,0.10)"
        Sd = "rgba(46,125,50,0.26)"
        Sc = "#2e7d32"

    # Active classes
    ha = " active" if active == "home"     else ""
    sa = " active" if active == "schedule" else ""
    aa = " active" if active == "about"    else ""

    nav_timer    = t("nav_timer")
    nav_schedule = t("nav_schedule")
    nav_about    = t("nav_about")

    st.markdown(f"""
<style>
/* ── Hamburger button: visible, high z-index ── */
header[data-testid="stHeader"] {{
    height: 0 !important; min-height: 0 !important;
    overflow: visible !important;
    background: transparent !important;
    box-shadow: none !important; border: none !important;
}}
header[data-testid="stHeader"] * {{ display: none !important; }}

[data-testid="stSidebarCollapse"],
[data-testid="collapsedControl"] {{
    display: flex !important; align-items: center !important;
    justify-content: center !important;
    position: fixed !important; top: 10px !important; left: 10px !important;
    z-index: 2000000 !important;
    width: 36px !important; height: 36px !important;
    background: {Sb} !important; border: 1px solid {Sd} !important;
    border-radius: 9px !important; cursor: pointer !important;
    transition: background .15s ease, border-color .15s ease !important;
    box-shadow: 0 2px 10px rgba(0,0,0,.2) !important;
}}
[data-testid="stSidebarCollapse"]:hover,
[data-testid="collapsedControl"]:hover {{
    background: rgba(76,175,80,.28) !important;
    border-color: rgba(76,175,80,.55) !important;
}}
[data-testid="stSidebarCollapse"] button,
[data-testid="collapsedControl"] button {{
    all: unset !important; cursor: pointer !important;
    width: 100% !important; height: 100% !important;
    display: flex !important; align-items: center !important;
    justify-content: center !important;
}}
[data-testid="stSidebarCollapse"] svg,
[data-testid="collapsedControl"] svg {{
    fill: {Sc} !important; color: {Sc} !important;
    width: 18px !important; height: 18px !important;
}}

/* ── Nav bar ── */
.rd-nav {{
    position: fixed; top: 0; left: 0; right: 0;
    height: 52px;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 16px 0 56px;
    background: {B};
    border-bottom: 1px solid {Bd};
    box-shadow: {Sh};
    backdrop-filter: blur(20px) saturate(1.4);
    -webkit-backdrop-filter: blur(20px) saturate(1.4);
    z-index: 1000;
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Inter",sans-serif;
    box-sizing: border-box;
    animation: rdSlideDown 0.5s cubic-bezier(0.16,1,0.3,1);
}}
@keyframes rdSlideDown {{
    0% {{ transform: translateY(-100%); opacity: 0; }}
    100% {{ transform: translateY(0); opacity: 1; }}
}}
.rd-brand {{
    display: flex; align-items: center; gap: 8px; flex-shrink: 0;
    font-weight: 700; font-size: 15px; color: {T};
}}
.rd-dot {{
    width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0;
    background: #4caf50; box-shadow: 0 0 6px rgba(76,175,80,.7);
    animation: rdPulse 2.6s ease-in-out infinite;
}}
@keyframes rdPulse {{
    0%,100% {{ transform:scale(1); opacity:1; }}
    50%      {{ transform:scale(.72); opacity:.5; }}
}}
.rd-links {{
    display: flex; align-items: center; gap: 2px;
    position: absolute; left: 50%; transform: translateX(-50%);
}}
.rd-link {{
    font-size: 13px; font-weight: 500; color: {M};
    padding: 6px 13px; border-radius: 8px;
    transition: background .15s ease, color .15s ease;
    cursor: pointer; white-space: nowrap;
    text-decoration: none;
}}
.rd-link:hover {{ background: {H}; color: {T}; }}
.rd-link.active {{ background: {A}; color: {Ac}; font-weight: 600; }}

.rd-right {{
    display: flex; align-items: center; gap: 5px; flex-shrink: 0;
}}
.rd-user {{
    font-size: 11px; font-weight: 500; color: {M};
    background: {Pb}; border: 1px solid {Pd};
    padding: 3px 10px; border-radius: 20px;
    max-width: 120px; overflow: hidden;
    text-overflow: ellipsis; white-space: nowrap;
}}
.rd-btn {{
    font-size: 13px; cursor: pointer;
    background: {Pb}; border: 1px solid {Pd}; color: {M};
    padding: 5px 9px; border-radius: 8px;
    transition: background .15s ease, color .15s ease;
    text-decoration: none; white-space: nowrap;
}}
.rd-btn:hover {{ background: {A}; color: {Ac}; border-color: rgba(76,175,80,.3); }}

/* ── Push content down ── */
.main .block-container,
section[data-testid="stMain"] .block-container {{
    padding-top: 66px !important;
}}
section[data-testid="stMain"] > div:first-child {{ padding-top: 0 !important; }}

/* ── Hide Streamlit chrome ── */
footer, [data-testid="stStatusWidget"], [data-testid="stToolbar"],
[data-testid="stDecoration"], #MainMenu {{ display:none !important; }}

/* ── Mobile ── */
@media(max-width:600px) {{
    .rd-nav {{ padding: 0 8px 0 50px !important; }}
    .rd-brand .rd-name {{ display:none !important; }}
    .rd-dot {{ display:none !important; }}
    .rd-user {{ display:none !important; }}
    .rd-link {{ font-size:11px; padding:5px 8px; }}
    .rd-right {{ gap:3px; }}
    .rd-btn {{ font-size:11px; padding:4px 7px; }}
}}
</style>

<div class="rd-nav">
  <div class="rd-brand">
    {logo_html}
    <span class="rd-name">Rekxare Dami</span>
    <span class="rd-dot"></span>
  </div>
  <div class="rd-links">
    <a class="rd-link{ha}" href="/?page=home"     target="_self">⏱️ {nav_timer}</a>
    <a class="rd-link{sa}" href="/?page=schedule" target="_self">📅 {nav_schedule}</a>
    <a class="rd-link{aa}" href="/?page=about"    target="_self">✨ {nav_about}</a>
  </div>
  <div class="rd-right">
    <span class="rd-user">👤 {user_name}</span>
    <a class="rd-btn" href="?dark_mode=1" target="_self">{dark_icon}</a>
    <a class="rd-btn" href="?lang=cycle"  target="_self">{lang_abbr}</a>
  </div>
</div>
""", unsafe_allow_html=True)

render_nav()

# ── Set current_page for active highlight ──
# Detect based on the current file path
import sys
if "01_Schedule" in sys.argv[0]:
    st.session_state.current_page = "schedule"
elif "02_About" in sys.argv[0]:
    st.session_state.current_page = "about"
else:
    st.session_state.current_page = "home"

# ══════════════════════════════════════════════════════════
#  RUN THE PAGE
# ══════════════════════════════════════════════════════════
pg = st.navigation([
    st.Page("Home.py",              title=t("nav_timer"),    icon="⏱️", default=True),
    st.Page("pages/01_Schedule.py", title=t("nav_schedule"), icon="📅", url_path="schedule"),
    st.Page("pages/02_About.py",    title=t("nav_about"),    icon="✨",  url_path="about"),
], position="hidden")
pg.run()
