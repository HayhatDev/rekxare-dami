import streamlit as st
import hashlib


@st.cache_resource
def get_supabase():
    from supabase import create_client
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])


def get_user_key() -> str:
    if st.user.is_logged_in:
        email = st.user.email
    else:
        email = st.session_state.get("user_email", "default")
    return hashlib.md5(email.encode()).hexdigest()[:8]


# ── Study Data ──────────────────────────────────────────────

def save_data():
    get_supabase().table("study_data").upsert({
        "user_key": get_user_key(),
        "data": {
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
        }
    }).execute()


def load_data():
    try:
        res = get_supabase().table("study_data") \
            .select("data").eq("user_key", get_user_key()).maybe_single().execute()
        if not res.data:
            return
        data = res.data["data"]
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    st.session_state.total_study_seconds = data.get("total_seconds", 0)
    st.session_state.completed_sessions  = data.get("sessions", 0)
    st.session_state.last_subject        = data.get("last_subject", "—")
    st.session_state.study_history       = data.get("history", [])
    st.session_state.dark_mode           = data.get("dark_mode", True)
    st.session_state.streak              = data.get("streak", 0)
    st.session_state.last_study_date     = data.get("last_study_date", "")
    st.session_state.daily_seconds       = data.get("daily_seconds", 0)
    st.session_state.daily_goal_seconds  = data.get("daily_goal_seconds", 7200)
    st.session_state.lang                = data.get("lang", "badini")
    st.session_state.student_name        = data.get("student_name", "")
    st.session_state.user_email          = data.get("user_email", "")
    if st.session_state.user_email:
        st.session_state.logged_in = True


# ── Schedule ────────────────────────────────────────────────

def save_schedule():
    get_supabase().table("schedules").upsert({
        "user_key": get_user_key(),
        "schedule": st.session_state.schedule,
    }).execute()


def load_schedule() -> dict:
    try:
        res = get_supabase().table("schedules") \
            .select("schedule").eq("user_key", get_user_key()).maybe_single().execute()
        if res.data:
            return res.data["schedule"]
    except Exception as e:
        print(f"Error loading schedule: {e}")
    return {}


def get_schedule_data() -> dict:
    return load_schedule()


# ── Preferences ─────────────────────────────────────────────

def save_preferences():
    get_supabase().table("user_prefs").upsert({
        "user_key": get_user_key(),
        "lang":      st.session_state.get("lang", "badini"),
        "dark_mode": st.session_state.get("dark_mode", True),
    }).execute()


def load_preferences():
    try:
        res = get_supabase().table("user_prefs") \
            .select("lang,dark_mode").eq("user_key", get_user_key()).maybe_single().execute()
        if res.data:
            st.session_state.dark_mode = res.data.get("dark_mode", True)
            st.session_state.lang      = res.data.get("lang", "badini")
            return True
    except Exception as e:
        print(f"Error loading preferences: {e}")
    return False


# ── Legacy shims so old imports don't break ─────────────────
def get_data_file():        return ""
def get_schedule_file():    return ""
def get_preferences_file(): return ""
