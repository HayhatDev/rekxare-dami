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
#  TOP BAR  —  JS-persistent, survives Streamlit reruns
#
#  How it works:
#   1. st.markdown() injects CSS + a hidden nav template + a script
#   2. The script moves the nav div to document.body (outside
#      Streamlit's managed container) so Streamlit's virtual DOM
#      reconciliation can NEVER remove or re-animate it
#   3. A MutationObserver on body watches for accidental removal
#      and re-attaches within ~8 ms if it ever happens
#   4. On each rerun the script only UPDATES active-link classes
#      and the user name — no DOM rebuild, no flash, no animation
#   5. The CSS is moved to <head> with a stable id so dark/light
#      token changes propagate cleanly without flicker
#   6. Sidebar hamburger is styled above the bar (z-index 1100000)
#      and always visible — display:none is never applied to it
# ══════════════════════════════════════════════════════════
def inject_notion_top_bar():
    is_dark      = st.session_state.get("dark_mode", True)
    current_lang = st.session_state.get("lang", "badini")
    dark_icon    = "☀️" if is_dark else "🌙"
    lang_abbr    = {"badini": "BA", "english": "EN", "arabic": "AR"}.get(current_lang, "EN")
    active       = st.session_state.get("current_page", "home")

    raw_name = (st.user.name if st.user.is_logged_in else t("student")) or "Student"
    user_name = raw_name[:22].replace("\\", "").replace("'", "").replace('"', "")

    try:
        with open("logo.png", "rb") as f:
            logo_src = "data:image/png;base64," + base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        logo_src = "https://placehold.co/26x26/4CAF50/FFFFFF?text=RD"

    # ── Design tokens
    if is_dark:
        bar_bg      = "rgba(13,11,36,0.96)"
        bar_border  = "rgba(255,255,255,0.07)"
        text_main   = "#ececec"
        text_muted  = "rgba(255,255,255,0.42)"
        active_bg   = "rgba(76,175,80,0.18)"
        active_clr  = "#7ec87f"
        hover_bg    = "rgba(255,255,255,0.055)"
        pill_bg     = "rgba(255,255,255,0.05)"
        pill_brd    = "rgba(255,255,255,0.08)"
        shadow      = "0 1px 0 rgba(255,255,255,0.04),0 6px 28px rgba(0,0,0,0.50)"
        sb_bg       = "rgba(76,175,80,0.13)"
        sb_brd      = "rgba(76,175,80,0.28)"
        sb_clr      = "#7ec87f"
    else:
        bar_bg      = "rgba(255,255,255,0.97)"
        bar_border  = "rgba(0,0,0,0.07)"
        text_main   = "#18182a"
        text_muted  = "rgba(0,0,0,0.42)"
        active_bg   = "rgba(56,142,60,0.12)"
        active_clr  = "#2e7d32"
        hover_bg    = "rgba(0,0,0,0.045)"
        pill_bg     = "rgba(0,0,0,0.04)"
        pill_brd    = "rgba(0,0,0,0.08)"
        shadow      = "0 1px 0 rgba(0,0,0,0.06),0 4px 20px rgba(0,0,0,0.09)"
        sb_bg       = "rgba(56,142,60,0.10)"
        sb_brd      = "rgba(56,142,60,0.22)"
        sb_clr      = "#2e7d32"

    home_cls  = "active" if active == "home"     else ""
    sched_cls = "active" if active == "schedule" else ""
    about_cls = "active" if active == "about"    else ""

    nav_timer    = t("nav_timer")
    nav_schedule = t("nav_schedule")
    nav_about    = t("nav_about")

    st.markdown(f"""
<!-- RD NAV INJECTION -->
<style id="rd-css-src">

/* ── Sidebar toggle: styled, always on top ── */
[data-testid="stSidebarCollapse"],
[data-testid="collapsedControl"] {{
    position: fixed !important;
    top: 11px !important;
    left: 11px !important;
    z-index: 1100000 !important;
    background: {sb_bg} !important;
    border: 1px solid {sb_brd} !important;
    border-radius: 9px !important;
    transition: background 0.18s ease, border-color 0.18s ease !important;
}}
[data-testid="stSidebarCollapse"]:hover,
[data-testid="collapsedControl"]:hover {{
    background: rgba(76,175,80,0.26) !important;
    border-color: rgba(76,175,80,0.45) !important;
}}
[data-testid="stSidebarCollapse"] svg,
[data-testid="stSidebarCollapse"] button,
[data-testid="collapsedControl"] svg,
[data-testid="collapsedControl"] button {{
    color: {sb_clr} !important;
    fill:  {sb_clr} !important;
}}

/* ── Persistent nav bar ── */
#rd-nav {{
    position: fixed !important;
    top: 0 !important; left: 0 !important; right: 0 !important;
    height: 52px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 0 18px 0 56px !important;
    background: {bar_bg} !important;
    border-bottom: 1px solid {bar_border} !important;
    box-shadow: {shadow} !important;
    backdrop-filter: blur(22px) saturate(1.5) !important;
    -webkit-backdrop-filter: blur(22px) saturate(1.5) !important;
    z-index: 999999 !important;
    font-family: -apple-system,BlinkMacSystemFont,"Segoe UI","Inter",sans-serif !important;
    box-sizing: border-box !important;
}}
#rd-nav * {{ box-sizing: border-box; text-decoration: none !important; }}

/* Brand */
.rd-brand {{
    display: flex; align-items: center; gap: 8px; flex-shrink: 0;
    font-weight: 700; font-size: 15.5px; letter-spacing: -0.25px;
    color: {text_main};
}}
.rd-brand img {{
    width: 25px; height: 25px; border-radius: 6px; object-fit: contain;
    filter: drop-shadow(0 0 6px rgba(76,175,80,0.4));
    flex-shrink: 0;
}}
.rd-dot {{
    width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0;
    background: #4caf50;
    box-shadow: 0 0 7px rgba(76,175,80,0.65);
    animation: rd-pulse 2.6s ease-in-out infinite;
}}
@keyframes rd-pulse {{
    0%,100% {{ transform: scale(1);    opacity: 1; }}
    50%     {{ transform: scale(0.72); opacity: 0.5; }}
}}

/* Nav links — centered absolutely so they don't shift with sidebar */
.rd-links {{
    display: flex; align-items: center; gap: 1px;
    position: absolute; left: 50%; transform: translateX(-50%);
}}
.rd-link {{
    font-size: 13px; font-weight: 500;
    color: {text_muted};
    padding: 6px 13px; border-radius: 8px;
    transition: background 0.15s ease, color 0.15s ease;
    white-space: nowrap; cursor: pointer;
}}
.rd-link:hover {{ background: {hover_bg}; color: {text_main}; }}
.rd-link.active {{
    background: {active_bg} !important;
    color: {active_clr} !important;
    font-weight: 600 !important;
}}

/* Right controls */
.rd-right {{ display: flex; align-items: center; gap: 5px; flex-shrink: 0; }}

.rd-user {{
    font-size: 11px; font-weight: 500; color: {text_muted};
    background: {pill_bg}; border: 1px solid {pill_brd};
    padding: 4px 11px; border-radius: 20px;
    max-width: 120px; overflow: hidden;
    text-overflow: ellipsis; white-space: nowrap;
}}
.rd-btn {{
    font-size: 13px; cursor: pointer;
    background: {pill_bg}; border: 1px solid {pill_brd};
    color: {text_muted};
    padding: 5px 9px; border-radius: 8px;
    transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
    white-space: nowrap;
}}
.rd-btn:hover {{
    background: {active_bg}; color: {active_clr};
    border-color: rgba(76,175,80,0.28);
}}

/* Push page content below the bar */
.main .block-container,
section[data-testid="stMain"] .block-container {{
    padding-top: 68px !important;
}}

/* Mobile */
@media (max-width: 600px) {{
    #rd-nav {{ padding: 0 10px 0 50px !important; height: 48px !important; }}
    .rd-brand-name {{ display: none !important; }}
    .rd-dot {{ display: none !important; }}
    .rd-link {{ font-size: 11px; padding: 5px 8px; }}
    .rd-user {{ display: none !important; }}
    .rd-btn {{ font-size: 11px; padding: 4px 7px; }}
    .rd-links {{ gap: 0; }}
}}
@media (max-width: 360px) {{
    .rd-link {{ font-size: 10px; padding: 4px 6px; }}
    .rd-right {{ gap: 3px; }}
}}
</style>

<!-- Hidden template — JS lifts this into document.body -->
<div id="rd-nav-tpl" style="display:none!important;visibility:hidden!important">
  <div id="rd-nav">
    <div class="rd-brand">
      <img src="{logo_src}" alt="">
      <span class="rd-brand-name">Rekxare Dami</span>
      <span class="rd-dot"></span>
    </div>
    <div class="rd-links">
      <a id="rd-lnk-home"     class="rd-link {home_cls}"  href="/"         target="_self">⏱️ {nav_timer}</a>
      <a id="rd-lnk-schedule" class="rd-link {sched_cls}" href="/schedule" target="_self">📅 {nav_schedule}</a>
      <a id="rd-lnk-about"    class="rd-link {about_cls}" href="/about"    target="_self">✨ {nav_about}</a>
    </div>
    <div class="rd-right">
      <span id="rd-username" class="rd-user">👤 {user_name}</span>
      <a class="rd-btn" href="?dark_mode=1" target="_self">{dark_icon}</a>
      <a class="rd-btn" href="?lang=cycle"  target="_self">{lang_abbr}</a>
    </div>
  </div>
</div>

<script>
(function() {{
  var ACTIVE = '{active}';
  var UNAME  = '👤 {user_name}';

  function moveCSS() {{
    var src = document.getElementById('rd-css-src');
    if (!src) return;
    var dest = document.getElementById('rd-css');
    if (!dest) {{
      dest    = document.createElement('style');
      dest.id = 'rd-css';
      document.head.appendChild(dest);
    }}
    dest.textContent = src.textContent;
    src.remove();
  }}

  function mountNav() {{
    var tpl = document.getElementById('rd-nav-tpl');
    var nav = document.getElementById('rd-nav');

    // If nav already in body, skip full mount
    if (nav && nav.parentElement === document.body) {{
      updateNav(nav);
      if (tpl) tpl.remove();
      return;
    }}

    // Lift nav from template into body
    if (tpl) {{
      var inner = tpl.querySelector('#rd-nav');
      if (inner) {{
        document.body.appendChild(inner);
        nav = inner;
      }}
      tpl.remove();
    }}

    if (nav) updateNav(nav);
  }}

  function updateNav(nav) {{
    // Update active link (no DOM rebuild — just class swap)
    ['home','schedule','about'].forEach(function(p) {{
      var el = document.getElementById('rd-lnk-' + p);
      if (!el) return;
      if (p === ACTIVE) el.classList.add('active');
      else              el.classList.remove('active');
    }});
    // Update user name
    var u = document.getElementById('rd-username');
    if (u) u.textContent = UNAME;
  }}

  function init() {{
    moveCSS();
    mountNav();
  }}

  init();
  requestAnimationFrame(init);

  // Guard: if Streamlit ever removes #rd-nav from body, re-mount fast
  if (!window.__rdObs) {{
    window.__rdObs = new MutationObserver(function(muts) {{
      for (var i = 0; i < muts.length; i++) {{
        var removed = muts[i].removedNodes;
        for (var j = 0; j < removed.length; j++) {{
          if (removed[j].id === 'rd-nav') {{
            setTimeout(function() {{
              document.body.appendChild(removed[0]);
              updateNav(removed[0]);
            }}, 8);
            return;
          }}
        }}
      }}
    }});
    window.__rdObs.observe(document.body, {{childList: true}});
  }}
}})();
</script>
""", unsafe_allow_html=True)


inject_notion_top_bar()

# ── Run the active page (Home.py / 01_Schedule.py / 02_About.py)
pg.run()
