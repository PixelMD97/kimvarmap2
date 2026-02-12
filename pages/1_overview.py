import streamlit as st
from api_client import (
    list_projects,
    create_project,
    get_project,
)
from auth_ui import render_auth_status


render_auth_status()

st.set_page_config(
    page_title="KIM VarMap – Overview",
    layout="wide",
)

st.title("KIM VarMap")
st.markdown("### Project Selection")

# ---------------------------------------------------
# Load available projects
# ---------------------------------------------------

try:
    projects = list_projects()
except Exception as e:
    st.error(f"Failed to load projects: {e}")
    st.stop()

project_names = [p["name"] for p in projects]

mode = st.radio(
    "Project mode",
    ["Use existing project", "Create new project"],
)

# ---------------------------------------------------
# EXISTING
# ---------------------------------------------------

if mode == "Use existing project":

    selected = st.selectbox("Select project", project_names)

    if st.button("Continue →"):
        st.session_state["project"] = selected
        st.switch_page("pages/2_mapping_editor.py")

# ---------------------------------------------------
# CREATE NEW
# ---------------------------------------------------

if mode == "Create new project":

    name = st.text_input("Project name (branch name)")
    display_name = st.text_input("Display name")
    collaborators = st.text_input("Collaborators (comma separated GitHub usernames)")

    if st.button("Create Project"):

        try:
            new_project = create_project(
                name=name.strip(),
                display_name=display_name.strip(),
                collaborators=[c.strip() for c in collaborators.split(",") if c.strip()],
            )

            st.session_state["project"] = new_project["name"]
            st.success("Project created.")
            st.switch_page("pages/2_mapping_editor.py")

        except Exception as e:
            st.error(str(e))
