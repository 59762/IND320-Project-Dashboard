"""
Home.py — Front page of the IND320 Streamlit app.

Streamlit automatically builds a sidebar navigation menu from every .py file
placed inside the /pages folder, so no manual menu code is needed here — the
sidebar with links to the other three pages appears as soon as this app runs
with `streamlit run Home.py`.
"""
import streamlit as st

st.set_page_config(
    page_title="IND320 Project - Dashboard Basics",
    page_icon="📊",
    layout="wide",
)

st.title("IND320 Project Work — Dashboard Basics")

st.markdown(
    """
    Welcome! Use the sidebar on the left to navigate between pages:

    - **Home** (this page)
    - **Data Table** — table view of the imported reservoir data
    - **Plot** — interactive plot of the imported reservoir data
    - **About** — extra / dummy page (placeholder for now)

    ---
    This is dummy header/test content for the part-1 hand-in. Replace this
    text with a short project description once the real content is ready.
    """
)
