"""
pages/1_Data_Table.py — Second page of the app.

Shows the imported reservoir data as a table, with one row per column of
the CSV, using st.column_config.LineChartColumn() to preview the first
month of each series inline.
"""
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Data Table", page_icon="📋", layout="wide")
st.title("Data Table")


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
    """Load the reservoir CSV, rename headers to English, and parse the
    Date column. Cached so the app doesn't re-read the file from disk on
    every interaction."""
    df = pd.read_csv(path)
    df = df.rename(columns=RENAME_MAP)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


df = load_data()

# Roughly the first month of data (assumes weekly rows -> ~4-5 rows)
first_month_mask = df["Date"] < (df["Date"].min() + pd.Timedelta(days=31))
first_month = df.loc[first_month_mask]

# Build a "one row per column" table: each data column becomes a row, with
# a small line-chart preview of its first month of values.
value_columns = [c for c in df.columns if c != "Date"]
table_rows = []
for col in value_columns:
    table_rows.append(
        {
            "Column": col,
            "First month": first_month[col].tolist(),
            "Min": df[col].min(),
            "Max": df[col].max(),
        }
    )
summary_df = pd.DataFrame(table_rows)

st.dataframe(
    summary_df,
    column_config={
        "First month": st.column_config.LineChartColumn(
            "First month",
            help="Preview of the first month of values for this column",
            width="medium",
        )
    },
    hide_index=True,
    use_container_width=True,
)

with st.expander("Show raw imported data"):
    st.dataframe(df, use_container_width=True)
