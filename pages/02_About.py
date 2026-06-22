import streamlit as st
import json

if not st.user.is_logged_in:
    st.switch_page("app.py")
    st.stop()
    
    
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

st.set_page_config(
    page_title=t("about_title"),
    page_icon="📚",
    layout="centered",
)

# ── PWA (after set_page_config)
st.markdown("""
<link rel="manifest" href="/manifest.json">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  THEME TOKENS
# ══════════════════════════════════════════════════════════
is_dark = st.session_state.dark_mode
if is_dark:
    APP_BG       = "#1a1a2e"
    SB_BG        = "#16213e"
    CARD_BG      = "rgba(255,255,255,0.06)"
    CARD_BORDER  = "rgba(255,255,255,0.10)"
    TEXT_PRIMARY = "#e2e2e2"
    TEXT_MUTED   = "#8a8fa8"
    DIVIDER      = "rgba(255,255,255,0.08)"
    HERO_GRAD    = "linear-gradient(135deg, rgba(76,175,80,0.18) 0%, rgba(33,150,243,0.12) 100%)"
    HERO_BDR     = "rgba(76,175,80,0.22)"
    BADGE_BG     = "rgba(255,255,255,0.07)"
    BADGE_BDR    = "rgba(255,255,255,0.12)"
    LINK_BG      = "rgba(255,255,255,0.05)"
    LINK_BDR     = "rgba(255,255,255,0.09)"
    STAT_BG      = "rgba(255,255,255,0.05)"
    STAT_BDR     = "rgba(255,255,255,0.09)"
    FEAT_HOVER   = "rgba(255,255,255,0.04)"
    TABLE_ALT    = "rgba(255,255,255,0.03)"
else:
    APP_BG       = "#e8edf5"
    SB_BG        = "#f4f7fb"
    CARD_BG      = "#ffffff"
    CARD_BORDER  = "#dde3ed"
    TEXT_PRIMARY = "#1a1a2e"
    TEXT_MUTED   = "#6b7280"
    DIVIDER      = "#dde3ed"
    HERO_GRAD    = "linear-gradient(135deg, rgba(76,175,80,0.09) 0%, rgba(33,150,243,0.06) 100%)"
    HERO_BDR     = "rgba(76,175,80,0.20)"
    BADGE_BG     = "#edf0f7"
    BADGE_BDR    = "#c8d4e8"
    LINK_BG      = "#ffffff"
    LINK_BDR     = "#dde3ed"
    STAT_BG      = "#ffffff"
    STAT_BDR     = "#dde3ed"
    FEAT_HOVER   = "#f8faff"
    TABLE_ALT    = "#f4f7fb"

# ══════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMainBlockContainer"],
section[data-testid="stMain"],
.main .block-container {{
    background-color: {APP_BG} !important;
    font-family: 'Inter', system-ui, sans-serif !important;
}}
[data-testid="stSidebar"] {{ background-color: {SB_BG} !important; }}
.stApp *, [data-testid="stSidebar"] * {{ color: {TEXT_PRIMARY} !important; }}

/* ── MOBILE safe area ── */
.main .block-container {{
    padding-left:   max(1rem, env(safe-area-inset-left))   !important;
    padding-right:  max(1rem, env(safe-area-inset-right))  !important;
    padding-bottom: max(1.5rem, env(safe-area-inset-bottom)) !important;
}}

/* ── Hero ── */
.hero-card {{
    background: {HERO_GRAD};
    border: 1.5px solid {HERO_BDR};
    border-radius: 28px;
    padding: 40px 28px 32px;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 4px 28px rgba(76,175,80,0.10);
    position: relative;
    overflow: hidden;
}}
.hero-card::before {{
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(76,175,80,0.12), transparent 70%);
    pointer-events: none;
}}
.hero-icon {{
    font-size: 72px; line-height: 1; margin-bottom: 16px; display: block;
    filter: drop-shadow(0 4px 16px rgba(76,175,80,0.35));
    animation: float 3s ease-in-out infinite;
}}
@keyframes float {{
    0%,100% {{ transform: translateY(0); }}
    50%      {{ transform: translateY(-8px); }}
}}
.hero-title {{
    font-size: 36px; font-weight: 900; letter-spacing: -1px;
    color: {TEXT_PRIMARY} !important; margin-bottom: 8px; line-height: 1.1;
}}
.hero-tagline {{
    font-size: 15px; color: {TEXT_MUTED} !important;
    font-weight: 500; line-height: 1.5; max-width: 320px; margin: 0 auto 20px;
}}
.hero-badge {{
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(76,175,80,0.14); border: 1.5px solid rgba(76,175,80,0.28);
    color: #4CAF50 !important; border-radius: 20px;
    padding: 6px 16px; font-size: 12px; font-weight: 700;
    letter-spacing: 0.5px;
}}

/* ── Stats row ── */
.stats-row {{
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 12px; margin-bottom: 24px;
}}
.stat-box {{
    background: {STAT_BG};
    border: 1.5px solid {STAT_BDR};
    border-radius: 20px; padding: 20px 12px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    transition: transform 0.15s ease;
}}
.stat-box:active {{ transform: scale(0.97); }}
.stat-number {{
    font-size: 32px; font-weight: 900; line-height: 1;
    letter-spacing: -1px; margin-bottom: 6px;
}}
.stat-label {{
    font-size: 11px; font-weight: 700;
    color: {TEXT_MUTED} !important;
    text-transform: uppercase; letter-spacing: 0.6px;
}}

/* ── Section title ── */
.section-title {{
    font-size: 12px; font-weight: 800; letter-spacing: 1.2px;
    text-transform: uppercase; color: {TEXT_MUTED} !important;
    margin: 28px 0 14px; display: flex; align-items: center; gap: 10px;
}}
.section-line {{ flex: 1; height: 1px; background: {DIVIDER}; }}

/* ── Feature cards grid ── */
.features-grid {{
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 12px; margin-bottom: 24px;
}}
.feat-card {{
    background: {CARD_BG};
    border: 1.5px solid {CARD_BORDER};
    border-radius: 20px; padding: 20px 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    border-top: 3px solid var(--accent);
}}
.feat-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.10);
}}
.feat-icon  {{ font-size: 28px; margin-bottom: 10px; display: block; }}
.feat-title {{
    font-size: 14px; font-weight: 800;
    color: {TEXT_PRIMARY} !important; margin-bottom: 6px; line-height: 1.3;
}}
.feat-desc  {{
    font-size: 12px; color: {TEXT_MUTED} !important;
    line-height: 1.5; font-weight: 500;
}}

/* ── Tech stack chips ── */
.tech-grid {{
    display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px;
}}
.tech-chip {{
    display: inline-flex; align-items: center; gap: 7px;
    background: {BADGE_BG}; border: 1.5px solid {BADGE_BDR};
    border-radius: 20px; padding: 8px 16px;
    font-size: 13px; font-weight: 700;
    transition: transform 0.12s ease;
}}
.tech-chip:active {{ transform: scale(0.96); }}
.tech-chip-dot {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}

/* ── Developer / link cards ── */
.dev-card {{
    background: {CARD_BG}; border: 1.5px solid {CARD_BORDER};
    border-radius: 24px; padding: 28px 24px; margin-bottom: 16px;
    box-shadow: 0 3px 18px rgba(0,0,0,0.06);
    display: flex; align-items: center; gap: 20px;
}}
.dev-avatar {{
    width: 64px; height: 64px; border-radius: 50%;
    background: linear-gradient(135deg, #4CAF50, #2196F3);
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(76,175,80,0.30);
}}
.dev-name   {{ font-size: 18px; font-weight: 800; letter-spacing: -0.3px; }}
.dev-handle {{ font-size: 13px; color: {TEXT_MUTED} !important; margin-top: 3px; font-weight: 500; }}

.link-row {{
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 10px; margin-bottom: 24px;
}}
.link-card {{
    background: {LINK_BG}; border: 1.5px solid {LINK_BDR};
    border-radius: 16px; padding: 16px 12px; text-align: center;
    text-decoration: none !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    display: block;
}}
.link-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
    border-color: #4CAF50;
}}
.link-icon  {{ font-size: 26px; margin-bottom: 6px; display: block; }}
.link-label {{
    font-size: 11px; font-weight: 700;
    color: {TEXT_MUTED} !important;
    text-transform: uppercase; letter-spacing: 0.5px;
}}
.link-url   {{
    font-size: 11px; font-weight: 600;
    color: #4CAF50 !important; margin-top: 2px;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}}

/* ── About card (generic) ── */
.about-card {{
    background: {CARD_BG}; border: 1.5px solid {CARD_BORDER};
    border-radius: 20px; padding: 22px 20px; margin-bottom: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}}
.about-card h3 {{
    font-size: 16px; font-weight: 800; margin: 0 0 10px;
    letter-spacing: -0.2px;
}}
.about-card p, .about-card li {{
    font-size: 14px; line-height: 1.65;
    color: {TEXT_MUTED} !important; font-weight: 500;
}}
.about-card ul {{ padding-left: 18px; margin: 0; }}
.about-card li {{ margin-bottom: 6px; }}

/* ── Table ── */
.tech-table {{ width: 100%; border-collapse: collapse; margin: 0; }}
.tech-table tr:nth-child(even) td {{ background: {TABLE_ALT}; }}
.tech-table td {{
    padding: 10px 12px; font-size: 13px;
    border-bottom: 1px solid {DIVIDER};
}}
.tech-table td:first-child {{ font-weight: 700; width: 38%; }}
.tech-table tr:last-child td {{ border-bottom: none; }}

/* ── Hackathon ribbon ── */
.hackathon-banner {{
    background: linear-gradient(135deg, rgba(106,27,154,0.14), rgba(171,71,188,0.08));
    border: 1.5px solid rgba(171,71,188,0.25);
    border-radius: 16px; padding: 16px 20px;
    display: flex; align-items: center; gap: 14px; margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(106,27,154,0.10);
}}
.hackathon-icon {{ font-size: 32px; flex-shrink: 0; }}
.hackathon-title {{ font-size: 14px; font-weight: 800; color: #ab47bc !important; }}
.hackathon-sub   {{ font-size: 12px; color: {TEXT_MUTED} !important; margin-top: 2px; font-weight: 500; }}

/* ── Footer ── */
.about-footer {{
    text-align: center; padding: 16px 0 8px;
    font-size: 12px; color: {TEXT_MUTED} !important;
    border-top: 1px solid {DIVIDER}; margin-top: 8px;
}}

hr {{ border-color: {DIVIDER} !important; margin: 20px 0 !important; }}
.stAlert {{ border-radius: 14px !important; }}
.stApp a {{ color: #4CAF50 !important; }}

{"""/* ── Arabic RTL */
.hero-card, .hero-tagline, .hackathon-banner, .hackathon-title, .hackathon-sub,
.about-card, .about-card h3, .about-card p,
.feat-card, .feat-title, .feat-desc,
.dev-card, .dev-name, .dev-handle,
.stat-box, .stat-label,
.about-footer, .section-title, .tech-chip { direction: rtl; text-align: right; }
.dev-card { flex-direction: row-reverse; }
""" if st.session_state.lang == "arabic" else ""}

/* ── Mobile ── */
@media (max-width: 640px) {{
    .hero-card   {{ padding: 28px 18px 24px; border-radius: 22px; }}
    .hero-icon   {{ font-size: 56px; }}
    .hero-title  {{ font-size: 28px; }}
    .hero-tagline {{ font-size: 14px; }}
    .stats-row   {{ gap: 8px; }}
    .stat-box    {{ padding: 16px 8px; border-radius: 16px; }}
    .stat-number {{ font-size: 26px; }}
    .features-grid {{ grid-template-columns: 1fr; gap: 10px; }}
    .dev-card    {{ padding: 20px 16px; gap: 14px; }}
    .dev-avatar  {{ width: 52px; height: 52px; font-size: 22px; }}
    .dev-name    {{ font-size: 16px; }}
    .link-row    {{ grid-template-columns: 1fr; gap: 8px; }}
    .link-card   {{ display: flex; align-items: center; gap: 12px;
                    text-align: left; padding: 12px 16px; }}
    .link-icon   {{ margin-bottom: 0; font-size: 22px; }}
}}
@media (max-width: 380px) {{
    .stats-row   {{ grid-template-columns: 1fr; }}
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero-card">
    <span class="hero-icon">📚</span>
    <div class="hero-title">Rekxare Dami</div>
    <div class="hero-tagline">
        {t('app_tagline')}
    </div>
    <div class="hero-badge">✨ {t('about_features')}</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  HACKATHON BANNER
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hackathon-banner">
    <div class="hackathon-icon">🏆</div>
    <div>
        <div class="hackathon-title">{t('hackathon_project')}</div>
        <div class="hackathon-sub">{t('hackathon_sub')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  STATS
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="stats-row">
    <div class="stat-box">
        <div class="stat-number" style="color:#4CAF50;">3</div>
        <div class="stat-label">{t('stat_pages')}</div>
    </div>
    <div class="stat-box">
        <div class="stat-number" style="color:#2196F3;">3</div>
        <div class="stat-label">{t('stat_languages')}</div>
    </div>
    <div class="stat-box">
        <div class="stat-number" style="color:#FF9800;">∞</div>
        <div class="stat-label">{t('stat_sessions')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  WHAT / WHY
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="about-card">
    <h3>💡 {t('about_what')}</h3>
    <p>{t('about_what_desc')}</p>
</div>
<div class="about-card">
    <h3>🎯 {t('about_why')}</h3>
    <p>{t('about_why_desc')}</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  FEATURES GRID
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="section-title">
    🚀 {t('about_features')}
    <div class="section-line"></div>
</div>
<div class="features-grid">
    <div class="feat-card" style="--accent:#4CAF50;">
        <span class="feat-icon">⏱️</span>
        <div class="feat-title">{t('feature_timer')}</div>
        <div class="feat-desc">{t('feature_timer_desc')}</div>
    </div>
    <div class="feat-card" style="--accent:#2196F3;">
        <span class="feat-icon">📊</span>
        <div class="feat-title">{t('feature_stats')}</div>
        <div class="feat-desc">{t('feature_stats_desc')}</div>
    </div>
    <div class="feat-card" style="--accent:#FF9800;">
        <span class="feat-icon">🗓️</span>
        <div class="feat-title">{t('feature_schedule')}</div>
        <div class="feat-desc">{t('feature_schedule_desc')}</div>
    </div>
    <div class="feat-card" style="--accent:#9C27B0;">
        <span class="feat-icon">🤖</span>
        <div class="feat-title">{t('feature_ai_scheduler')}</div>
        <div class="feat-desc">{t('feature_ai_scheduler_desc')}</div>
    </div>
    <div class="feat-card" style="--accent:#607D8B;">
        <span class="feat-icon">🌙</span>
        <div class="feat-title">{t('feature_dark_mode')}</div>
        <div class="feat-desc">{t('feature_dark_mode_desc')}</div>
    </div>
    <div class="feat-card" style="--accent:#00BCD4;">
        <span class="feat-icon">🌍</span>
        <div class="feat-title">{t('feature_languages')}</div>
        <div class="feat-desc">{t('feature_languages_desc')}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  TECH STACK
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="section-title">
    💻 {t('about_tech_stack')}
    <div class="section-line"></div>
</div>
<div class="tech-grid">
    <span class="tech-chip">
        <span class="tech-chip-dot" style="background:#3776AB;"></span>
        Python 3
    </span>
    <span class="tech-chip">
        <span class="tech-chip-dot" style="background:#FF4B4B;"></span>
        Streamlit
    </span>
    <span class="tech-chip">
        <span class="tech-chip-dot" style="background:#F7DF1E;"></span>
        HTML / CSS / JS
    </span>
    <span class="tech-chip">
        <span class="tech-chip-dot" style="background:#4CAF50;"></span>
        JSON Storage
    </span>
    <span class="tech-chip">
        <span class="tech-chip-dot" style="background:#9C27B0;"></span>
        Groq AI / Llama 3
    </span>
    <span class="tech-chip">
        <span class="tech-chip-dot" style="background:#2196F3;"></span>
        Streamlit Cloud
    </span>
    <span class="tech-chip">
        <span class="tech-chip-dot" style="background:#FF9800;"></span>
        PWA + Service Worker
    </span>
    <span class="tech-chip">
        <span class="tech-chip-dot" style="background:#607D8B;"></span>
        SVG Animations
    </span>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  BUILT BY
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="section-title">
    👤 {t('about_built_by')}
    <div class="section-line"></div>
</div>
<div class="dev-card">
    <div class="dev-avatar">👨‍💻</div>
    <div>
        <div class="dev-name">HayhatDev</div>
        <div class="dev-handle">@Zanst.21 · Full-stack student developer</div>
        <div style="margin-top:8px;font-size:13px;color:{TEXT_MUTED};font-weight:500;">
            {t('about_built_by_desc')}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  LINKS
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="section-title">
    🔗 {t('about_links')}
    <div class="section-line"></div>
</div>
<div class="link-row">
    <a class="link-card" href="https://rekxare-dami.streamlit.app" target="_blank">
        <span class="link-icon">🌐</span>
        <div class="link-label">{t('link_live')}</div>
        <div class="link-url">rekxare-dami.streamlit.app</div>
    </a>
    <a class="link-card" href="https://github.com/HayhatDev/rekxare-dami" target="_blank">
        <span class="link-icon">🐙</span>
        <div class="link-label">GitHub</div>
        <div class="link-url">HayhatDev/rekxare-dami</div>
    </a>
    <a class="link-card" href="https://instagram.com/Zanst.21" target="_blank">
        <span class="link-icon">📸</span>
        <div class="link-label">Instagram</div>
        <div class="link-url">@Zanst.21</div>
    </a>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="about-footer">
    {t("about_footer")}<br>
    <span style="opacity:0.6;margin-top:4px;display:block;">{t('made_with')}</span>
</div>
""", unsafe_allow_html=True)
