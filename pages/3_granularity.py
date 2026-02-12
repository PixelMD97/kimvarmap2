import streamlit as st
import pandas as pd

from auth_ui import render_auth_status

if "project" not in st.session_state:
    st.error("No project selected.")
    st.stop()

project = st.session_state["project"]

render_auth_status()

st.set_page_config(
    page_title="Granularity",
    layout="wide",
)

st.title(f"Granularity – {project}")

st.markdown("""
Define optional extraction logic.

This is currently demo-mode only.
No backend persistence yet.
""")

if "granularity_df" not in st.session_state:
    st.session_state["granularity_df"] = pd.DataFrame(
        columns=["Variable", "Summary", "Time Basis"]
    )

df = st.session_state["granularity_df"]

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
)

st.session_state["granularity_df"] = edited_df

st.success("Granularity draft saved locally.")

if st.button("Back to Mapping Editor"):
    st.switch_page("pages/2_mapping_editor.py")

if st.button("Continue to Export →"):
    st.switch_page("pages/4_export.py")
