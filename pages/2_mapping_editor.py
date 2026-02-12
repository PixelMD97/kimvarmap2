import uuid
import pandas as pd
import streamlit as st

from api_client import (
    list_mappings,
    save_all_mappings,
    propose_mappings,
)
from auth_ui import render_auth_status


# ---------------------------------------------------
# Safety
# ---------------------------------------------------

if "project" not in st.session_state:
    st.error("No project selected.")
    st.stop()

project = st.session_state["project"]

render_auth_status()

st.set_page_config(
    page_title="Mapping Editor",
    layout="wide",
)

st.title(f"Mapping Editor – {project}")


# ---------------------------------------------------
# Load mappings from backend
# ---------------------------------------------------

@st.cache_data(show_spinner=False)
def load_mappings(project):
    return list_mappings(project) or []


backend_mappings = load_mappings(project)


# ---------------------------------------------------
# Convert to DataFrame
# ---------------------------------------------------

def backend_to_df(mappings):

    rows = []
    mapping_lookup = {}

    for m in mappings:
        mapping_lookup[m["id"]] = m

        classification = m.get("classification") or {}
        path = classification.get("path") or []

        epic_id = ""
        pdms_id = ""

        for src in m.get("source") or []:
            if src.get("system", "").upper() == "EPIC":
                epic_id = src.get("variable", "")
            if src.get("system", "").upper() == "PDMS":
                pdms_id = src.get("variable", "")

        rows.append({
            "__id__": m["id"],
            "Variable": m.get("name", ""),
            "Organ System": path[0] if len(path) > 0 else "General",
            "Group": path[1] if len(path) > 1 else "General",
            "EPIC ID": epic_id,
            "PDMS ID": pdms_id,
            "Unit": m.get("unit", ""),
            "Status": m.get("status", "proposed"),
        })

    df = pd.DataFrame(rows)
    st.session_state["mapping_lookup"] = mapping_lookup

    return df


df_original = backend_to_df(backend_mappings)

if "mapping_draft_df" not in st.session_state:
    st.session_state["mapping_draft_df"] = df_original.copy()
    st.session_state["mapping_dirty"] = False

df = st.session_state["mapping_draft_df"]


# ---------------------------------------------------
# Editor
# ---------------------------------------------------

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
)

# Dirty tracking
if not edited_df.equals(df):
    st.session_state["mapping_dirty"] = True
    st.session_state["mapping_draft_df"] = edited_df


# ---------------------------------------------------
# Warning
# ---------------------------------------------------

if st.session_state.get("mapping_dirty"):
    st.warning("You have unsaved changes.")


# ---------------------------------------------------
# Save Changes
# ---------------------------------------------------

if st.button("💾 Save Changes"):

    payload = []

    for _, row in edited_df.iterrows():

        mapping_id = row.get("__id__") or str(uuid.uuid4())

        payload.append({
            "id": mapping_id,
            "name": row["Variable"],
            "source": [
                {"system": "EPIC", "variable": row["EPIC ID"]},
                {"system": "PDMS", "variable": row["PDMS ID"]},
            ],
            "mapping_type": "raw",
            "unit": row["Unit"],
            "status": "proposed",   # Always auto-set
            "classification": {
                "path": [
                    row["Organ System"],
                    row["Group"],
                ]
            }
        })

    try:
        save_all_mappings(project, payload)

        st.success("Saved successfully.")
        st.session_state["mapping_dirty"] = False
        st.cache_data.clear()

        st.rerun()

    except Exception as e:
        st.error(str(e))


# ---------------------------------------------------
# Propose Selected
# ---------------------------------------------------

selected_ids = st.multiselect(
    "Select mappings to propose",
    edited_df["__id__"].tolist(),
)

if st.button("🚀 Propose Selected"):
    try:
        propose_mappings(project, selected_ids)
        st.success("Proposal created.")
    except Exception as e:
        st.error(str(e))
