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
#  PAGE CONFIG  ← must be FIRST Streamlit call
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Rekxare Dami",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── PWA meta ──
st.markdown("""
<link rel="manifest" href="/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#1a1a2e">
<script>
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js').catch(()=>{});
  }
</script>
""", unsafe_allow_html=True)

# ── Wire user session + load preferences ──
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
    animation:float 3s ease-in-out infinite, glow-icon 3s ease-in-out infinite;}}
@keyframes float{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-10px);}}}}
@keyframes glow-icon{{
  0%,100%{{filter:drop-shadow(0 4px 16px rgba(76,175,80,.4));}}
  50%{{filter:drop-shadow(0 4px 28px rgba(76,175,80,.85)) drop-shadow(0 0 40px rgba(76,175,80,.4));}}
}}
.lt{{font-size:32px;font-weight:900;letter-spacing:-.8px;color:#fff;text-align:center;
    margin-bottom:4px;
    animation:glow-text 4s ease-in-out infinite;}}
@keyframes glow-text{{
  0%,100%{{text-shadow:0 0 10px rgba(76,175,80,.3);}}
  50%{{text-shadow:0 0 20px rgba(76,175,80,.7),0 0 40px rgba(76,175,80,.4),0 0 60px rgba(76,175,80,.2);}}
}}
.ls{{font-size:14px;color:rgba(255,255,255,.55);text-align:center;margin-bottom:24px;font-weight:500;}}
.lb{{display:inline-flex;align-items:center;gap:6px;background:rgba(76,175,80,.15);
    border:1px solid rgba(76,175,80,.25);color:#81c784;border-radius:20px;
    padding:5px 14px;font-size:11px;font-weight:700;letter-spacing:.5px;margin-bottom:24px;}}
.lc{{background:rgba(0,0,0,.5);border:1.5px solid rgba(255,255,255,.13);border-radius:28px;
    padding:32px 28px 28px;width:100%;backdrop-filter:blur(12px);
    box-shadow:0 8px 40px rgba(0,0,0,.40);}}
.stButton>button{{background:linear-gradient(135deg,#388e3c,#4caf50)!important;
    color:#fff!important;border:none!important;border-radius:40px!important;
    font-weight:700!important;font-size:14px!important;min-height:44px!important;
    box-shadow:0 2px 8px rgba(76,175,80,.3)!important;transition:all .18s ease!important;
    width:100%!important;}}
.stButton>button:hover{{transform:translateY(-2px)!important;
    box-shadow:0 6px 16px rgba(76,175,80,.45)!important;filter:brightness(1.05)!important;}}
.lc .stButton>button{{font-size:16px!important;min-height:52px!important;
    box-shadow:0 4px 18px rgba(76,175,80,.35)!important;}}
.dv{{display:flex;align-items:center;gap:12px;margin:24px 0 20px;
    color:rgba(255,255,255,.35);font-size:12px;font-weight:600;}}
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
#  NAVIGATION  — position="hidden" means we draw our own nav bar.
#  st.navigation() handles URL path changes and browser tab titles
#  automatically.  Do NOT call st.switch_page() anywhere in this file.
# ══════════════════════════════════════════════════════════
pg = st.navigation(
    [
        st.Page("Home.py",              title="Rekxare Dami · " + t("nav_timer"),    icon="⏱️", default=True),
        st.Page("pages/01_Schedule.py", title="Rekxare Dami · " + t("nav_schedule"), icon="📅", url_path="schedule"),
        st.Page("pages/02_About.py",    title="Rekxare Dami · " + t("nav_about"),    icon="✨",  url_path="about"),
    ],
    position="hidden",
)

# ── Detect active page from the live Page object ──
_upath = getattr(pg, "url_path", "")
if _upath == "schedule":
    _active = "schedule"
elif _upath == "about":
    _active = "about"
else:
    _active = "home"

st.session_state.current_page = _active

# ══════════════════════════════════════════════════════════
#  CUSTOM NAV BAR
# ══════════════════════════════════════════════════════════
def render_nav(active: str):
    is_dark = st.session_state.get("dark_mode", True)
    lang    = st.session_state.get("lang", "badini")

    user_name = "Student"
    if st.user.is_logged_in:
        raw = st.user.name or st.user.email or "Student"
        user_name = raw[:20]

    try:
        with open("logo.png", "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        logo_html = (
            f'<img src="data:image/png;base64,{logo_b64}" '
            f'class="rd-logo" alt="logo">'
        )
    except FileNotFoundError:
        logo_html = '<span class="rd-logo-emoji">📚</span>'

    # ── Theme tokens ──
    if is_dark:
        NAV_BG   = "rgba(13,11,36,0.92)"
        NAV_BDR  = "rgba(255,255,255,0.08)"
        NAV_SH   = "0 4px 32px rgba(0,0,0,0.60)"
        TXT      = "#ececec"
        MUTED    = "rgba(255,255,255,0.42)"
        ACTIVE_BG= "rgba(76,175,80,0.18)"
        ACTIVE_C = "#7ec87f"
        HOVER_BG = "rgba(255,255,255,0.07)"
        PILL_BG  = "rgba(255,255,255,0.06)"
        PILL_BDR = "rgba(255,255,255,0.10)"
        SB_BG    = "rgba(76,175,80,0.13)"
        SB_BDR   = "rgba(76,175,80,0.35)"
        SB_ICON  = "#7ec87f"
    else:
        NAV_BG   = "rgba(255,255,255,0.94)"
        NAV_BDR  = "rgba(0,0,0,0.08)"
        NAV_SH   = "0 4px 24px rgba(0,0,0,0.12)"
        TXT      = "#18182a"
        MUTED    = "rgba(0,0,0,0.44)"
        ACTIVE_BG= "rgba(46,125,50,0.12)"
        ACTIVE_C = "#2e7d32"
        HOVER_BG = "rgba(0,0,0,0.05)"
        PILL_BG  = "rgba(0,0,0,0.05)"
        PILL_BDR = "rgba(0,0,0,0.09)"
        SB_BG    = "rgba(46,125,50,0.10)"
        SB_BDR   = "rgba(46,125,50,0.28)"
        SB_ICON  = "#2e7d32"

    ha = " nav-active" if active == "home"     else ""
    sa = " nav-active" if active == "schedule" else ""
    aa = " nav-active" if active == "about"    else ""

    nav_timer    = t("nav_timer")
    nav_schedule = t("nav_schedule")
    nav_about    = t("nav_about")
    lang_abbr    = {"badini": "BA", "english": "EN", "arabic": "AR"}.get(lang, "EN")

    st.markdown(f"""
<style>
/* ════════════════════════════════════════════════════════
   SIDEBAR TOGGLE BUTTON — fixed using the correct
   Streamlit 1.36+ test-id.  This element is OUTSIDE the
   stHeader, so "header * {{ display:none }}" does NOT touch it.
   ════════════════════════════════════════════════════════ */

/* 1. Collapse the stHeader strip to zero height (keep overflow
      visible so nothing clips the sibling sidebar button)      */
header[data-testid="stHeader"] {{
    height: 0 !important;
    min-height: 0 !important;
    overflow: visible !important;
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
    padding: 0 !important;
}}
/* 2. Hide ONLY the inner toolbar divs, NOT the sidebar control */
header[data-testid="stHeader"] > div {{
    display: none !important;
}}

/* 3. Style the real sidebar collapse control                   */
[data-testid="stSidebarCollapsedControl"] {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    position: fixed !important;
    top: 8px !important;
    left: 10px !important;
    z-index: 2100000 !important;
    width: 36px !important;
    height: 36px !important;
    background: {SB_BG} !important;
    border: 1.5px solid {SB_BDR} !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    box-shadow: 0 2px 12px rgba(0,0,0,.22) !important;
    transition: background 0.18s, border-color 0.18s, box-shadow 0.18s !important;
}}
[data-testid="stSidebarCollapsedControl"]:hover {{
    background: rgba(76,175,80,0.28) !important;
    border-color: rgba(76,175,80,0.60) !important;
    box-shadow: 0 0 14px rgba(76,175,80,.35) !important;
}}
[data-testid="stSidebarCollapsedControl"] button {{
    all: unset !important;
    width: 100% !important;
    height: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
}}
[data-testid="stSidebarCollapsedControl"] svg {{
    fill: {SB_ICON} !important;
    color: {SB_ICON} !important;
    width: 18px !important;
    height: 18px !important;
}}

/* ════════════════════════════════════════════════════════
   NAVBAR
   ════════════════════════════════════════════════════════ */
.rd-nav {{
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 14px 0 54px;
    background: {NAV_BG};
    border-bottom: 1px solid {NAV_BDR};
    box-shadow: {NAV_SH};
    backdrop-filter: blur(24px) saturate(1.5);
    -webkit-backdrop-filter: blur(24px) saturate(1.5);
    z-index: 1500000;
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
    box-sizing: border-box;
    /* Slide-down entry animation */
    animation: rdSlideDown 0.55s cubic-bezier(0.16, 1, 0.3, 1) both;
}}
@keyframes rdSlideDown {{
    0%   {{ transform: translateY(-100%); opacity: 0; }}
    100% {{ transform: translateY(0);     opacity: 1; }}
}}

/* ── Brand ── */
.rd-brand {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    text-decoration: none !important;
}}
.rd-logo {{
    width: 24px; height: 24px;
    border-radius: 6px;
    vertical-align: middle;
    animation: logoFloat 3.5s ease-in-out infinite, logoGlow 3.5s ease-in-out infinite;
}}
@keyframes logoFloat {{
    0%,100% {{ transform: translateY(0);    }}
    50%      {{ transform: translateY(-3px); }}
}}
@keyframes logoGlow {{
    0%,100% {{ filter: drop-shadow(0 0  5px rgba(76,175,80,.40)); }}
    50%      {{ filter: drop-shadow(0 0 14px rgba(76,175,80,.85))
                        drop-shadow(0 0 28px rgba(76,175,80,.35)); }}
}}
.rd-logo-emoji {{
    font-size: 22px;
    animation: logoFloat 3.5s ease-in-out infinite, logoGlow 3.5s ease-in-out infinite;
    display: inline-block;
}}
.rd-name {{
    font-size: 15px;
    font-weight: 800;
    letter-spacing: -0.3px;
    color: {TXT} !important;
    /* Pulsing glow on the brand name */
    animation: brandGlow 4s ease-in-out infinite;
    background: linear-gradient(135deg, {TXT}, #4CAF50, {TXT});
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmerText 4s linear infinite, brandPulse 4s ease-in-out infinite;
}}
@keyframes shimmerText {{
    0%   {{ background-position: 0%   center; }}
    100% {{ background-position: 200% center; }}
}}
@keyframes brandPulse {{
    0%,100% {{ opacity: 1;    }}
    50%      {{ opacity: 0.85; }}
}}
.rd-dot {{
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #4caf50;
    box-shadow: 0 0 6px 2px rgba(76,175,80,.65);
    animation: dotPulse 2.4s ease-in-out infinite;
    flex-shrink: 0;
}}
@keyframes dotPulse {{
    0%,100% {{ transform: scale(1);    box-shadow: 0 0 6px 2px rgba(76,175,80,.65); }}
    50%      {{ transform: scale(0.65); box-shadow: 0 0 3px 1px rgba(76,175,80,.30); }}
}}

/* ── Nav links (centered) ── */
.rd-links {{
    display: flex;
    align-items: center;
    gap: 2px;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
}}
.rd-link {{
    font-size: 13px;
    font-weight: 500;
    color: {MUTED} !important;
    padding: 6px 13px;
    border-radius: 9px;
    transition: background 0.18s ease, color 0.18s ease, box-shadow 0.18s ease;
    cursor: pointer;
    white-space: nowrap;
    text-decoration: none !important;
    position: relative;
}}
.rd-link::after {{
    content: '';
    position: absolute;
    bottom: 4px; left: 50%; transform: translateX(-50%);
    width: 0; height: 2px;
    background: {ACTIVE_C};
    border-radius: 2px;
    transition: width 0.22s ease;
}}
.rd-link:hover {{
    background: {HOVER_BG} !important;
    color: {TXT} !important;
}}
.rd-link:hover::after {{ width: 60%; }}
.rd-link.nav-active {{
    background: {ACTIVE_BG} !important;
    color: {ACTIVE_C} !important;
    font-weight: 700 !important;
    box-shadow: 0 0 12px rgba(76,175,80,0.28),
                inset 0 0 10px rgba(76,175,80,0.08);
}}
.rd-link.nav-active::after {{ width: 70%; }}

/* ── Right pill (user + lang pill) ── */
.rd-right {{
    display: flex;
    align-items: center;
    gap: 5px;
    flex-shrink: 0;
}}
.rd-user {{
    font-size: 11px;
    font-weight: 600;
    color: {MUTED} !important;
    background: {PILL_BG};
    border: 1px solid {PILL_BDR};
    padding: 4px 10px;
    border-radius: 20px;
    max-width: 110px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}}
.rd-lang {{
    font-size: 11px;
    font-weight: 700;
    color: {ACTIVE_C} !important;
    background: {ACTIVE_BG};
    border: 1px solid rgba(76,175,80,0.28);
    padding: 4px 8px;
    border-radius: 8px;
    letter-spacing: 0.4px;
}}

/* ── Push page content below fixed nav ── */
.main .block-container,
section[data-testid="stMain"] .block-container {{
    padding-top: 68px !important;
}}

/* ── Hide Streamlit chrome we don't need ── */
footer,
[data-testid="stStatusWidget"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu {{ display: none !important; }}

/* ── Mobile responsive ── */
@media (max-width: 600px) {{
    .rd-nav  {{ padding: 0 8px 0 52px !important; height: 48px; }}
    .rd-name {{ display: none !important; }}
    .rd-dot  {{ display: none !important; }}
    .rd-user {{ display: none !important; }}
    .rd-link {{ font-size: 11px !important; padding: 5px 8px !important; }}
    .rd-lang {{ font-size: 10px !important; padding: 3px 6px !important; }}
}}
@media (max-width: 380px) {{
    .rd-link {{ font-size: 10px !important; padding: 4px 6px !important; }}
}}
</style>

<div class="rd-nav">
  <a class="rd-brand" href="/" target="_self">
    {logo_html}
    <span class="rd-name">Rekxare Dami</span>
    <span class="rd-dot"></span>
  </a>

  <div class="rd-links">
    <a class="rd-link{ha}" href="/"          target="_self">⏱️ {nav_timer}</a>
    <a class="rd-link{sa}" href="/schedule"  target="_self">📅 {nav_schedule}</a>
    <a class="rd-link{aa}" href="/about"     target="_self">✨ {nav_about}</a>
  </div>

  <div class="rd-right">
    <span class="rd-user">👤 {user_name}</span>
    <span class="rd-lang">{lang_abbr}</span>
  </div>
</div>
""", unsafe_allow_html=True)


render_nav(_active)

# ══════════════════════════════════════════════════════════
#  RUN THE CURRENT PAGE
#  st.navigation() updates the browser URL and tab title
#  automatically — no st.switch_page() needed.
# ══════════════════════════════════════════════════════════
pg.run()
