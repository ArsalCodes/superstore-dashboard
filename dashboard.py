import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Load dataset with proper encoding and parse dates
df = pd.read_csv("data/Superstore.csv", encoding="latin1", parse_dates=["Order Date"])

st.title("📊 Super Store Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Category filter
category_filter = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Date range filter
min_date = df["Order Date"].min()
max_date = df["Order Date"].max()
date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

# Apply filters
filtered_df = df[
    (df["Category"].isin(category_filter)) &
    (df["Order Date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
]

# --- Sales Trend ---
st.subheader("Sales Trend Over Time")
monthly_sales = filtered_df.resample('ME', on="Order Date").sum()
fig_sales = px.line(monthly_sales, x=monthly_sales.index, y="Sales", title="Monthly Sales")
st.plotly_chart(fig_sales)

# --- Profit Breakdown ---
st.subheader("Profit by Sub-Category")
fig_profit = px.bar(filtered_df, x="Sub-Category", y="Profit", color="Category", title="Profit Breakdown")
st.plotly_chart(fig_profit)

# --- RFM Analysis ---
st.subheader("RFM Analysis")
rfm_df = filtered_df.groupby("Customer ID").agg({
    "Order Date": lambda x: (filtered_df["Order Date"].max() - x.max()).days,
    "Order ID": "count",
    "Sales": "sum"
}).rename(columns={"Order Date":"Recency","Order ID":"Frequency","Sales":"Monetary"})

rfm_df = rfm_df.reset_index()

st.dataframe(rfm_df.head())
fig_rfm = px.scatter(rfm_df, x="Recency", y="Frequency", size="Monetary",
                     hover_name="Customer ID", title="RFM Segmentation")
st.plotly_chart(fig_rfm)
