import pandas as pd
import plotly.express as px
import streamlit as st

# Page config must be the first Streamlit command
st.set_page_config(page_title="Financial ETL Dashboard", layout="wide")


@st.cache_data
def load_data():
    # Load the clean, processed parquet file
    df = pd.read_parquet("data/processed/transactions_clean.parquet")
    # Extract month/year for trending
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return df


df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
selected_categories = st.sidebar.multiselect(
    "Select Category", options=df["category"].unique(), default=df["category"].unique()
)
selected_sources = st.sidebar.multiselect(
    "Select Source System",
    options=df["source_system"].unique(),
    default=df["source_system"].unique(),
)

# Apply filters
filtered_df = df[
    (df["category"].isin(selected_categories))
    & (df["source_system"].isin(selected_sources))
]

# --- MAIN DASHBOARD ---
st.title(" Financial Transaction Dashboard")
st.markdown("Interactive BI reporting layer built on top of the custom ETL pipeline.")

# KPI CARDS
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", f"{len(filtered_df):,}")
col2.metric("Total Volume", f"${filtered_df['amount'].sum():,.2f}")
col3.metric("Average Transaction", f"${filtered_df['amount'].mean():,.2f}")
col4.metric("Unique Customers", f"{filtered_df['customer_id'].nunique():,}")

st.divider()

# CHARTS
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Monthly Transaction Volume Trend")
    # Group by month
    trend_data = filtered_df.groupby("month")["amount"].sum().reset_index()
    fig_line = px.line(
        trend_data,
        x="month",
        y="amount",
        markers=True,
        title="Volume over Time",
        template="plotly_white",
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col_chart2:
    st.subheader("Breakdown by Category")
    cat_data = filtered_df.groupby("category")["amount"].sum().reset_index()
    fig_bar = px.bar(
        cat_data,
        x="amount",
        y="category",
        orientation="h",
        color="amount",
        color_continuous_scale="Viridis",
        title="Total Volume per Category",
        template="plotly_white",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# FILTERABLE DATA TABLE
st.subheader("Transactional Data Explorer")
st.dataframe(
    filtered_df.sort_values(by="date", ascending=False),
    column_config={
        "amount": st.column_config.NumberColumn(format="$ %.2f"),
        "date": st.column_config.DateColumn(format="YYYY-MM-DD"),
    },
    use_container_width=True,
)
