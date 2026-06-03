import streamlit as st
import json

with open("translations.json", "r", encoding="utf-8") as f:
    TRANSLATIONS = json.load(f)

if "lang" not in st.session_state:
    st.session_state.lang = "badini"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def t(key, **kwargs):
    text = TRANSLATIONS.get(st.session_state.lang, TRANSLATIONS["badini"]).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

st.set_page_config(
    page_title=t("about_title"),
    page_icon="📚",
    layout="centered"
)

is_dark = st.session_state.dark_mode
if is_dark:
    bg_color = "#1a1a2e"
    text_color = "#e2e2e2"
    card_bg = "rgba(255,255,255,0.06)"
    card_border = "rgba(255,255,255,0.09)"
else:
    bg_color = "#e8edf5"
    text_color = "#1a1a2e"
    card_bg = "#ffffff"
    card_border = "#dde3ed"

st.markdown(f"""
<style>
    .stApp, .main .block-container {{
        background-color: {bg_color} !important;
    }}
    .stApp * {{
        color: {text_color} !important;
    }}
    .about-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }}
    h2, h3 {{
        margin-top: 8px;
        margin-bottom: 12px;
    }}
    ul {{
        padding-left: 20px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
    }}
    td {{
        padding: 8px 12px;
    }}
</style>
""", unsafe_allow_html=True)

st.title(f"📚 {t('about_title')}")

st.markdown(f"""
<div class="about-card">
    <h3>{t('about_what')}</h3>
    <p>{t('about_what_desc')}</p>
</div>

<div class="about-card">
    <h3>{t('about_why')}</h3>
    <p>{t('about_why_desc')}</p>
</div>

<div class="about-card">
    <h3>🚀 {t('about_features')}</h3>
    <ul>
        <li>⏱️ <strong>{t('feature_timer')}</strong> {t('feature_timer_desc')}</li>
        <li>📊 <strong>{t('feature_stats')}</strong> {t('feature_stats_desc')}</li>
        <li>🗓️ <strong>{t('feature_schedule')}</strong> {t('feature_schedule_desc')}</li>
        <li>🌙 <strong>{t('feature_dark_mode')}</strong></li>
        <li>🌍 <strong>{t('feature_languages')}</strong></li>
        <li>💾 <strong>{t('feature_save')}</strong> {t('feature_save_desc')}</li>
    </ul>
</div>

<div class="about-card">
    <h3>💻 {t('about_tech_stack')}</h3>
    <table>
        <tr><td><strong>Python</strong></td><td>{t('tech_python')}</td></tr>
        <tr><td><strong>Streamlit</strong></td><td>{t('tech_streamlit')}</td></tr>
        <tr><td><strong>HTML / CSS</strong></td><td>{t('tech_html_css')}</td></tr>
        <tr><td><strong>SVG</strong></td><td>{t('tech_svg')}</td></tr>
        <tr><td><strong>JSON</strong></td><td>{t('tech_json')}</td></tr>
        <tr><td><strong>Streamlit Cloud</strong></td><td>{t('tech_cloud')}</td></tr>
    </table>
</div>

<div class="about-card">
    <h3>👤 {t('about_built_by')}</h3>
    <p>{t('about_built_by_desc')}</p>
</div>

<div class="about-card">
    <h3>🔗 {t('about_links')}</h3>
    <p>
        🔗 <strong>{t('link_live')}:</strong> <a href="https://rekxare-dami.streamlit.app">rekxare-dami.streamlit.app</a><br>
        🐙 <strong>GitHub:</strong> <a href="https://github.com/HayhatDev/rekxare-dami">github.com/HayhatDev/rekxare-dami</a><br>
        📸 <strong>Instagram:</strong> <a href="https://instagram.com/Zanst.21">@Zanst.21</a>
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()
st.caption(t("about_footer"))
