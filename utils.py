import json
import os
import hashlib
import streamlit as st

def get_data_file():
    email = st.user.email if st.user.is_logged_in else st.session_state.get("user_email", "default")
    return f"study_data_{hashlib.md5(email.encode()).hexdigest()[:8]}.json"

def save_data():
    DATA_FILE = get_data_file()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "total_seconds":      st.session_state.total_study_seconds,
            "sessions":           st.session_state.completed_sessions,
            "last_subject":       st.session_state.last_subject,
            "history":            st.session_state.study_history,
            "dark_mode":          st.session_state.dark_mode,
            "streak":             st.session_state.streak,
            "last_study_date":    st.session_state.last_study_date,
            "daily_seconds":      st.session_state.daily_seconds,
            "daily_goal_seconds": st.session_state.daily_goal_seconds,
            "lang":               st.session_state.lang,
            "student_name":       st.session_state.get("student_name", ""),
            "user_email":         st.session_state.get("user_email", ""),
        }, f, ensure_ascii=False, indent=2)

def get_schedule_file():
    email = st.user.email if st.user.is_logged_in else st.session_state.get("user_email", "default")
    return f"schedule_data_{hashlib.md5(email.encode()).hexdigest()[:8]}.json"
