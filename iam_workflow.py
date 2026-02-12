import streamlit as st
import requests
import os


def login_button():
    backend = os.getenv(
        "KIM_API_BASE_URL",
        "https://2025varmapbackend-adgyb5eqghc6bzay.westeurope-01.azurewebsites.net"
    )

    login_url = f"{backend}/auth/login"

    st.markdown(
        f'<a href="{login_url}" target="_self">'
        f'<button>Login with GitHub</button>'
        f'</a>',
        unsafe_allow_html=True,
    )


def handle_callback():
    params = st.query_params

    if "access_token" in params:
        st.session_state["access_token"] = params["access_token"]
        st.query_params.clear()
        st.rerun()
