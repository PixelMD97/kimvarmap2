import streamlit as st
import requests
import os

from auth_ui import render_auth_status

if "project" not in st.session_state:
    st.error("No project selected.")
    st.stop()

project = st.session_state["project"]
token = st.session_state.get("access_token")

render_auth_status()

st.set_page_config(
    page_title="Export",
    layout="wide",
)

st.title(f"Export – {project}")

base_url = os.getenv(
    "KIM_API_BASE_URL",
    "https://2025varmapbackend-adgyb5eqghc6bzay.westeurope-01.azurewebsites.net"
).rstrip("/")

if st.button("Download CSV from Backend"):

    try:
        response = requests.get(
            f"{base_url}/projects/{project}/mappings/export.csv",
            headers={"Authorization": f"Bearer {token}"},
        )

        response.raise_for_status()

        st.download_button(
            label="Download CSV",
            data=response.content,
            file_name=f"{project}_mappings.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(str(e))

if st.button("← Back to Granularity"):
    st.switch_page("pages/3_granularity.py")
