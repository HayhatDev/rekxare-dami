import streamlit as st
import json
import os
import hashlib
import base64

# ══════════════════════════════════════════════════════════
#  TRANSLATIONS  (must load before set_page_config uses t())
# ══════════════════════════════════════════════════════════
with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

# ── Early session-state defaults (needed before login gate)
if "lang" not in st.session_state:
    st.session_state.lang = "badini"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text


# ── Shared preference helpers (pages also define these locally
#    so they can call save_preferences() from their own sidebar)
def get_preferences_file():
    if st.user.is_logged_in:
        email = st.user.email
    else:
        email = st.session_state.get("user_email", "default")
    return f"preferences_{hashlib.md5(email.encode()).hexdigest()[:8]}.json"


def save_preferences():
    filename = get_preferences_file()
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({
            "dark_mode": st.session_state.get("dark_mode", True),
            "lang":      st.session_state.get("lang", "badini"),
        }, f, ensure_ascii=False, indent=2)


def load_preferences():
    filename = get_preferences_file()
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            st.session_state.dark_mode = data.get("dark_mode", True)
            st.session_state.lang      = data.get("lang", "badini")
            return True
        except Exception:
            pass
    return False


# ══════════════════════════════════════════════════════════
#  PAGE CONFIG — called ONCE here; pages must NOT call it
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Rekxare Dami",
    page_icon="logo.png",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── PWA
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

# ── Load saved preferences + wire up user session (runs on every page)
if st.user.is_logged_in:
    # Wire user identity into session state once per browser session
    if "user_email" not in st.session_state or not st.session_state.user_email:
        st.session_state.user_email = st.user.email
        st.session_state.data_key   = hashlib.md5(st.user.email.encode()).hexdigest()[:8]
        st.session_state.logged_in  = True
    # Always keep data_key aligned with the logged-in email
    st.session_state.data_key = st.user.email.split("@")[0]
    load_preferences()

# ══════════════════════════════════════════════════════════
#  LOGIN GATE
# ══════════════════════════════════════════════════════════
if not st.user.is_logged_in:
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    *, *::before, *::after {{ box-sizing: border-box; }}

    html, body, .stApp, [data-testid="stAppViewContainer"],
    section[data-testid="stMain"], .main, .main .block-container {{
        background: linear-gradient(135deg, #0f0c29, #1a1a2e, #16213e) !important;
        font-family: 'Inter', system-ui, sans-serif !important;
    }}

    header[data-testid="stHeader"], #MainMenu, footer,
    [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {{
        display: none !important;
    }}

    .main .block-container {{
        padding-top: max(20px, calc(50vh - 260px)) !important;
        padding-bottom: 40px !important;
        padding-left:  20px !important;
        padding-right: 20px !important;
        max-width: 480px !important;
    }}

    .login-wrap {{
        width: 100%;
        display: flex; flex-direction: column; align-items: center;
    }}
    .login-logo {{
        font-size: 72px; line-height: 1; margin-bottom: 12px;
        filter: drop-shadow(0 4px 16px rgba(76,175,80,0.4));
        animation: float 3s ease-in-out infinite;
    }}
    @keyframes float {{
        0%,100% {{ transform: translateY(0); }}
        50%      {{ transform: translateY(-8px); }}
    }}
    .login-title {{
        font-size: 32px; font-weight: 900; letter-spacing: -0.8px;
        color: #ffffff; text-align: center; margin-bottom: 4px;
    }}
    .login-sub {{
        font-size: 14px; color: rgba(255,255,255,0.55);
        text-align: center; margin-bottom: 24px; font-weight: 500;
    }}
    .login-badge {{
        display: inline-flex; align-items: center; gap: 6px;
        background: rgba(76,175,80,0.15); border: 1px solid rgba(76,175,80,0.25);
        color: #81c784; border-radius: 20px; padding: 5px 14px;
        font-size: 11px; font-weight: 700; letter-spacing: 0.5px;
        margin-bottom: 24px;
    }}
    .login-card {{
        background: rgba(0,0,0,0.5);
        border: 1.5px solid rgba(255,255,255,0.13);
        border-radius: 28px;
        padding: 32px 28px 28px;
        width: 100%;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 40px rgba(0,0,0,0.40);
    }}
    .stButton > button {{
        background: linear-gradient(135deg, #388e3c, #4caf50) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 40px !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        min-height: 44px !important;
        box-shadow: 0 2px 8px rgba(76,175,80,0.3) !important;
        transition: all 0.18s ease !important;
        width: 100% !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(76,175,80,0.45) !important;
        filter: brightness(1.05) !important;
    }}
    .login-card .stButton > button {{
        font-size: 16px !important;
        min-height: 52px !important;
        box-shadow: 0 4px 18px rgba(76,175,80,0.35) !important;
    }}
    .divider {{
        display: flex; align-items: center; gap: 12px;
        margin: 24px 0 20px;
        color: rgba(255,255,255,0.35);
        font-size: 12px; font-weight: 600;
    }}
    .divider::before, .divider::after {{
        content: ""; flex: 1; height: 1px;
        background: rgba(255,255,255,0.15);
    }}
    .login-footer {{
        font-size: 12px; color: rgba(255,255,255,0.30);
        text-align: center; margin-top: 24px;
    }}
    </style>

    <div class="login-wrap">
        <div class="login-logo">📚</div>
        <div class="login-title">Rekxare Dami</div>
        <div class="login-sub">{t('login_sub')}</div>
        <div class="login-badge">{t('login_badge')}</div>
        <div class="login-card">
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("بادينى", key="lang_badini_login", use_container_width=True):
            st.session_state.lang = "badini"
            st.rerun()
    with col2:
        if st.button("English", key="lang_en_login", use_container_width=True):
            st.session_state.lang = "english"
            st.rerun()
    with col3:
        if st.button("العربية", key="lang_ar_login", use_container_width=True):
            st.session_state.lang = "arabic"
            st.rerun()

    st.markdown(f'<div class="divider">{t("login_divider")}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("🔐 Google", on_click=st.login, use_container_width=True)

    st.markdown(f'<div class="login-footer">{t("login_footer")}</div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════
#  HANDLE QUERY PARAMS — dark mode & language toggle
#  These fire from the top bar's ?dark_mode=1 / ?lang=cycle links.
#  Handled here (in app.py) so they work on EVERY page.
# ══════════════════════════════════════════════════════════
if "dark_mode" in st.query_params:
    st.session_state.dark_mode = not st.session_state.get("dark_mode", True)
    save_preferences()
    st.query_params.clear()
    st.rerun()

if "lang" in st.query_params and st.query_params["lang"] == "cycle":
    lang_order = ["badini", "english", "arabic"]
    current = st.session_state.get("lang", "badini")
    try:
        idx = lang_order.index(current)
        next_lang = lang_order[(idx + 1) % len(lang_order)]
    except ValueError:
        next_lang = "badini"
    st.session_state.lang = next_lang
    save_preferences()
    st.query_params.clear()
    st.rerun()

# ══════════════════════════════════════════════════════════
#  NAVIGATION
#  position="hidden" removes nav items from the sidebar;
#  the custom HTML top bar handles all navigation instead.
#  url_path gives clean URLs: /  /schedule  /about
# ══════════════════════════════════════════════════════════
pg = st.navigation([
    st.Page("Home.py",              title=t("nav_timer"),    icon="⏱️", default=True),
    st.Page("pages/01_Schedule.py", title=t("nav_schedule"), icon="📅", url_path="schedule"),
    st.Page("pages/02_About.py",    title=t("nav_about"),    icon="✨",  url_path="about"),
], position="hidden")

# Detect active page from the navigation object's title
_title = pg.title
if _title == t("nav_schedule") or "Schedule" in _title or "خشتە" in _title:
    _active = "schedule"
elif _title == t("nav_about") or "About" in _title or "دەربارە" in _title:
    _active = "about"
else:
    _active = "home"
st.session_state.current_page = _active

# ══════════════════════════════════════════════════════════
#  TOP BAR — injected once here, appears on ALL pages
#
#  Fix vs the old custom bar:
#    • Hamburger toggle is NEVER hidden (display:none removed)
#    • Its z-index is raised ABOVE the nav bar (1000001 > 999999)
#    • Nav bar left padding (62px desktop / 56px mobile) leaves
#      room so the hamburger is always reachable
#    • Links use native st.navigation URL paths (/, /schedule,
#      /about) — no ?page= redirect needed
# ══════════════════════════════════════════════════════════
def inject_notion_top_bar():
    is_dark      = st.session_state.get("dark_mode", True)
    current_lang = st.session_state.get("lang", "badini")
    dark_icon    = "☀️" if is_dark else "🌙"
    lang_abbr    = {"badini": "BA", "english": "EN", "arabic": "AR"}.get(current_lang, "🌍")

    try:
        with open("logo.png", "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        logo_src = f"data:image/png;base64,{logo_data}"
    except FileNotFoundError:
        logo_src = "https://via.placeholder.com/28x28/4CAF50/FFFFFF?text=RD"

    if is_dark:
        bar_bg       = "rgba(26, 26, 46, 0.92)"
        bar_border   = "rgba(255, 255, 255, 0.06)"
        text_color   = "#ffffff"
        text_muted   = "rgba(255, 255, 255, 0.55)"
        text_hover   = "#ffffff"
        user_bg      = "rgba(255, 255, 255, 0.06)"
        user_color   = "rgba(255, 255, 255, 0.4)"
        icon_bg      = "rgba(255, 255, 255, 0.04)"
        icon_hover   = "rgba(76, 175, 80, 0.15)"
        shadow       = "0 2px 20px rgba(0, 0, 0, 0.3)"
    else:
        bar_bg       = "rgba(255, 255, 255, 0.92)"
        bar_border   = "rgba(0, 0, 0, 0.06)"
        text_color   = "#1a1a2e"
        text_muted   = "rgba(0, 0, 0, 0.5)"
        text_hover   = "#1a1a2e"
        user_bg      = "rgba(0, 0, 0, 0.04)"
        user_color   = "rgba(0, 0, 0, 0.4)"
        icon_bg      = "rgba(0, 0, 0, 0.04)"
        icon_hover   = "rgba(76, 175, 80, 0.12)"
        shadow       = "0 2px 20px rgba(0, 0, 0, 0.08)"

    active    = st.session_state.get("current_page", "home")
    home_cls  = "active" if active == "home"     else ""
    sched_cls = "active" if active == "schedule" else ""
    about_cls = "active" if active == "about"    else ""
    user_name = st.user.name if st.user.is_logged_in else t("student")

    st.markdown(f'''
<style>
a {{ text-decoration: none !important; }}

/* ── Hamburger ABOVE the nav bar ── */
[data-testid="stSidebarCollapse"],
[data-testid="collapsedControl"],
[data-testid="stBaseButton-header"] {{
    z-index: 1000001 !important;
    top: 8px !important;
}}

/* ── TOP NAVIGATION BAR ── */
.notion-nav-container {{
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 56px;
    background: {bar_bg};
    backdrop-filter: blur(16px) saturate(1.2);
    -webkit-backdrop-filter: blur(16px) saturate(1.2);
    border-bottom: 1px solid {bar_border};
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 28px 0 62px;   /* 62px left = room for hamburger */
    z-index: 999999;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Inter", sans-serif;
    animation: slideDown 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    box-shadow: {shadow};
}}

@keyframes slideDown {{
    0%   {{ transform: translateY(-100%); opacity: 0; }}
    100% {{ transform: translateY(0);     opacity: 1; }}
}}

.notion-nav-brand {{
    display: flex; align-items: center; gap: 12px;
    font-weight: 700; font-size: 17px;
    color: {text_color};
    letter-spacing: -0.3px;
    transition: transform 0.2s ease;
    cursor: default;
    text-shadow: 0 0 20px rgba(76,175,80,0.2);
}}
.notion-nav-brand:hover {{
    transform: scale(1.02);
    text-shadow: 0 0 30px rgba(76,175,80,0.35);
}}
.notion-nav-brand img {{
    height: 28px; width: 28px;
    object-fit: contain; border-radius: 6px;
    transition: all 0.3s ease;
    filter: drop-shadow(0 0 8px rgba(76,175,80,0.3));
}}
.notion-nav-brand img:hover {{
    transform: rotate(-8deg) scale(1.1);
    filter: drop-shadow(0 0 20px rgba(76,175,80,0.6));
}}
.notion-nav-brand .brand-name {{ transition: all 0.3s ease; }}
.notion-nav-brand .brand-name:hover {{ color: #4CAF50; }}
.notion-nav-brand .brand-dot {{
    display: inline-block;
    width: 8px; height: 8px;
    background: #4CAF50; border-radius: 50%;
    margin-left: 2px;
    animation: pulse-dot 2s ease-in-out infinite;
    box-shadow: 0 0 12px rgba(76,175,80,0.5);
}}
@keyframes pulse-dot {{
    0%,100% {{ opacity: 1; transform: scale(1);    box-shadow: 0 0 12px rgba(76,175,80,0.5); }}
    50%     {{ opacity: 0.6; transform: scale(0.85); box-shadow: 0 0 20px rgba(76,175,80,0.8); }}
}}

.notion-nav-links {{ display: flex; align-items: center; gap: 4px; }}

.notion-nav-item {{
    position: relative;
    font-size: 14px; color: {text_muted};
    text-decoration: none !important;
    padding: 8px 18px; border-radius: 8px;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    font-weight: 500; letter-spacing: 0.2px;
}}
.notion-nav-item:hover {{
    background: rgba(76,175,80,0.12);
    color: {text_hover};
    transform: translateY(-1px);
    text-decoration: none !important;
}}
.notion-nav-item.active {{
    color: {text_color};
    font-weight: 600;
    background: rgba(76,175,80,0.12);
    text-decoration: none !important;
}}
.notion-nav-item.active::after {{
    content: '';
    position: absolute;
    bottom: 2px; left: 50%;
    transform: translateX(-50%);
    width: 24px; height: 3px;
    background: #4CAF50; border-radius: 99px;
    animation: underlineIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    box-shadow: 0 0 12px rgba(76,175,80,0.5);
}}
@keyframes underlineIn {{
    0%   {{ width: 0;   opacity: 0; }}
    100% {{ width: 24px; opacity: 1; }}
}}

.notion-nav-right {{ display: flex; align-items: center; gap: 10px; }}

.notion-nav-user {{
    font-size: 12px; color: {user_color}; font-weight: 500;
    background: {user_bg};
    padding: 4px 14px; border-radius: 20px;
    border: 1px solid {bar_border};
    transition: all 0.2s ease;
    max-width: 150px; overflow: hidden;
    text-overflow: ellipsis; white-space: nowrap;
    text-decoration: none !important;
}}
.notion-nav-user:hover {{
    background: rgba(76,175,80,0.08);
    color: {text_color};
}}

.notion-nav-icon-btn {{
    background: {icon_bg}; border: 1px solid {bar_border};
    border-radius: 8px; padding: 6px 10px;
    color: {user_color}; font-size: 14px;
    cursor: pointer; transition: all 0.2s ease;
    display: flex; align-items: center; justify-content: center;
    text-decoration: none !important;
}}
.notion-nav-icon-btn:hover {{
    background: {icon_hover}; color: #4CAF50;
    border-color: rgba(76,175,80,0.2);
    transform: scale(1.05);
}}

/* ── Push main content below the fixed bar ── */
.main .block-container {{ padding-top: 72px !important; }}

/* ── Mobile ── */
@media (max-width: 640px) {{
    .notion-nav-container {{
        padding: 0 14px 0 56px;  /* 56px left on mobile */
        height: 50px;
    }}
    .notion-nav-brand {{ font-size: 14px; gap: 8px; }}
    .notion-nav-brand .brand-name {{ display: none; }}
    .notion-nav-item {{ font-size: 12px; padding: 6px 12px; }}
    .notion-nav-user {{ display: none; }}
    .notion-nav-icon-btn {{ padding: 4px 8px; font-size: 12px; }}
}}
@media (max-width: 400px) {{
    .notion-nav-item {{ font-size: 10px; padding: 4px 8px; }}
    .notion-nav-links {{ gap: 2px; }}
}}
</style>

<div class="notion-nav-container">
    <div class="notion-nav-brand">
        <img src="{logo_src}" alt="Logo">
        <span class="brand-name">Rekxare Dami</span>
        <span class="brand-dot"></span>
    </div>
    <div class="notion-nav-links">
        <a class="notion-nav-item {home_cls}"  href="/"         target="_self">⏱️ {t('nav_timer')}</a>
        <a class="notion-nav-item {sched_cls}" href="/schedule" target="_self">📅 {t('nav_schedule')}</a>
        <a class="notion-nav-item {about_cls}" href="/about"    target="_self">✨ {t('nav_about')}</a>
    </div>
    <div class="notion-nav-right">
        <span class="notion-nav-user">👤 {user_name}</span>
        <a class="notion-nav-icon-btn" href="?dark_mode=1"  target="_self">{dark_icon}</a>
        <a class="notion-nav-icon-btn" href="?lang=cycle"   target="_self">{lang_abbr}</a>
    </div>
</div>
''', unsafe_allow_html=True)


inject_notion_top_bar()

# ── Run the active page (Home.py / 01_Schedule.py / 02_About.py)
pg.run()
