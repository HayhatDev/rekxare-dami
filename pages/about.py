import streamlit as st

st.set_page_config(
    page_title="About | Rekxare Dami",
    page_icon="📚",
    layout="centered"
)

st.title("📚 About Rekxare Dami")

st.markdown("""
### What is Rekxare Dami?

Rekxare Dami is a **free, multilingual study time organizer** built for students. It helps you manage your study sessions, track your progress, and plan your week, all in your own language.

---

### Why was it built?

Most productivity apps are available only in English or Arabic. Kurdish students — especially Badini speakers had no study tool in their native language. Rekxare Dami fills that gap.

---

### Features

- ⏱️ **Live Countdown Timer** with visual progress circle.
- 📊 **Study Statistics** (total time, sessions, streaks, daily goals).
- 🗓️ **7-Day Schedule Planner** with task progress bars.
- 🌙 **Dark Mode**.
- 🌍 **3 Languages:** Badini Kurdish, English, Arabic.
- 💾 **Auto-save** (your data stays even after closing the browser).

---

### Tech Stack

| Technology | Used for |
| :--- | :--- |
| **Python** | Core logic |
| **Streamlit** | Web framework |
| **HTML / CSS** | Custom styling |
| **SVG** | Timer circle animation |
| **JSON** | Data storage |
| **Streamlit Cloud** | Hosting |

---

### Built by

**Hayhat Tahir** : a high school student from Kurdistan Region, Iraq. Passionate about computer engineering, robotics, and technology.

---

### Links

- 🔗 **Live App:** [rekxare-dami.streamlit.app](https://rekxare-dami.streamlit.app)
- 🐙 **GitHub:** [github.com/HayhatDev/rekxare-dami](https://github.com/HayhatDev/rekxare-dami)
- 📸 **Instagram:** [@Zanst.21](https://instagram.com/Zanst.21)
""")

st.divider()
st.caption("© 2026 Hayhat Tahir. Thanks to everyone checked or used the app!")
