# dashboard.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

uploaded = st.sidebar.file_uploader("Upload your own CSV", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.success("Using uploaded data ✅")
else:
    df = pd.read_csv("data.csv")
    st.info("Using sample data (from `data.csv`)")

st.set_page_config(page_title="Mini ETL Dashboard", layout="centered")
st.title("🏠 Mini ETL Dashboard")

df = pd.read_csv("data.csv")

# Sidebar filters
cities = ["(All)"] + sorted(df["city"].unique().tolist())
city = st.sidebar.selectbox("City", cities)
year_min, year_max = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider(
    "Year range", year_min, year_max, (year_min, year_max), step=1
)

mask = (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])
if city != "(All)":
    mask &= df["city"] == city
filtered = df[mask]

st.subheader("Data preview")
st.dataframe(filtered.head())

# KPIs
st.subheader("Summary metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total rows", len(filtered))
col2.metric("Unique cities", filtered["city"].nunique())
if not filtered.empty:
    col3.metric("Average price", f"£{filtered['price'].mean():,.0f}")
else:
    col3.metric("Average price", "—")

# Chart: average price by city within filters
st.subheader("Average price by city")
grouped = filtered.groupby("city")["price"].mean().sort_values(ascending=False)

st.subheader("Trend of average price by year")
trend = filtered.groupby("year")["price"].mean()

st.line_chart(trend)

fig, ax = plt.subplots()
grouped.plot(kind="bar", ax=ax)
ax.set_ylabel("Average price")
st.pyplot(fig)

st.subheader("Download cleaned dataset")
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="cleaned_data.csv",
    mime="text/csv",
)
