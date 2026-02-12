import streamlit as st


def render_auth_status():
    token = st.session_state.get("access_token")

    if token:
        st.sidebar.success("Authenticated")
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()
    else:
        st.sidebar.warning("Not authenticated")
