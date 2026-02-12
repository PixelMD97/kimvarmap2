import streamlit as st
from iam_workflow import handle_callback, login_button

st.set_page_config(
    page_title="KIM VarMap",
    page_icon="🧠",
    layout="wide",
)

# Handle OAuth redirect
handle_callback()

# If not authenticated → show login screen
if "access_token" not in st.session_state:
    st.title("KIM VarMap")
    st.markdown("### GitHub Login Required")
    login_button()
    st.stop()

# If authenticated → redirect to overview
st.switch_page("pages/1_overview.py")
