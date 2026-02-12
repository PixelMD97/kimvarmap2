import streamlit as st
from iam_workflow import (
    handle_callback,
    is_authenticated,
    login_button,
)

st.set_page_config(
    page_title="KIM VarMap",
    page_icon="🧠",
    layout="wide",
)

# Handle OAuth redirect
handle_callback()

# If authenticated → go to overview
if is_authenticated():
    st.switch_page("pages/1_overview.py")

# Otherwise show login
st.title("KIM VarMap")
st.markdown("### GitHub Login Required")

login_button()
