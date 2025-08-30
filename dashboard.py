# dashboard.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Mini ETL Dashboard", layout="centered")
st.title("🏠 Mini ETL Dashboard")

df = pd.read_csv("data.csv")

# Sidebar filters
cities = ["(All)"] + sorted(df["city"].unique().tolist())
city = st.sidebar.selectbox("City", cities)
year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider("Year range", year_min, year_max, (year_min, year_max), step=1)

mask = (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])
if city != "(All)":
    mask &= df["city"] == city
filtered = df[mask]

st.subheader("Data preview")
st.dataframe(filtered.head())

# KPIs
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Rows", len(filtered))
col2.metric("Cities", filtered["city"].nunique())
col3.metric("Avg price", f"£{filtered['price'].mean():,.0f}" if not filtered.empty else "—")

# Chart: average price by city within filters
st.subheader("Average price by city")
grouped = filtered.groupby("city")["price"].mean().sort_values(ascending=False)

fig, ax = plt.subplots()
grouped.plot(kind="bar", ax=ax)
ax.set_ylabel("Average price")
st.pyplot(fig)
