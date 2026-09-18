"""
pages/2_Plot.py — Third page of the app.

Plots the imported reservoir data with a dropdown to choose a single column
(or all columns) and a select_slider to pick a range of months. Defaults to
the first month.
"""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Plot", page_icon="📈", layout="wide")
st.title("Reservoir Data Plot")


RENAME_MAP = {
    "dato_Id": "Date",
    "fyllingsgrad": "Fill_degree",
    "kapasitet_TWh": "Capacity_TWh",
    "fylling_TWh": "Fill_TWh",
    "fyllingsgrad_forrige_uke": "Fill_degree_prev_week",
    "endring_fyllingsgrad": "Fill_degree_change",
}


@st.cache_data
def load_data(path: str = "data/reservoirs.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.rename(columns=RENAME_MAP)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


df = load_data()
value_columns = [c for c in df.columns if c != "Date"]

# --- Controls -------------------------------------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    choice = st.selectbox(
        "Column to plot",
        options=["All columns"] + value_columns,
        index=0,
    )

# Build month labels (Year-Month) for the slider, in chronological order
df["_month"] = df["Date"].dt.to_period("M").astype(str)
months = sorted(df["_month"].unique())

with col2:
    start_month, end_month = st.select_slider(
        "Month range",
        options=months,
        value=(months[0], months[0]),  # default: first month only
    )

mask = (df["_month"] >= start_month) & (df["_month"] <= end_month)
plot_df = df.loc[mask].set_index("Date")

# --- Plot -------------------------------------------------------------
st.subheader(f"{choice} — {start_month} to {end_month}")

if choice == "All columns":
    st.line_chart(plot_df[value_columns], use_container_width=True)
else:
    st.line_chart(plot_df[[choice]], use_container_width=True)

st.caption("Axis: Date (x) vs. selected column's value in its own unit (y) — "
           "Fill_degree/Fill_degree_change are fractions, Capacity_TWh/Fill_TWh are in TWh.")
