# ── Page persistence helper ──
def get_current_page():
    """Get the current page from session state or query params."""
    # First check session state
    if "page" in st.session_state:
        return st.session_state.page
    
    # Then check query params (for refresh persistence)
    query_params = st.query_params
    if "page" in query_params:
        return query_params["page"]
    
    # Default to home
    return "home"

def set_current_page(page):
    """Set the current page in both session state and query params."""
    st.session_state.page = page
    st.query_params["page"] = page

def switch_to_page(page):
    """Switch to a different page and save the state."""
    set_current_page(page)
    
    if page == "home":
        st.switch_page("Home.py")
    elif page == "schedule":
        st.switch_page("pages/01_Schedule.py")
    elif page == "about":
        st.switch_page("pages/02_About.py")
