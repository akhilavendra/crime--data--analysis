import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Crime Data Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Crime Data Analysis Dashboard")
st.caption("India | Sample data for educational use")

# Fictional sample dataset
df = pd.DataFrame({
    "State": [
        "Andhra Pradesh", "Telangana", "Karnataka",
        "Maharashtra", "Tamil Nadu", "Andhra Pradesh",
        "Telangana", "Karnataka", "Maharashtra",
        "Tamil Nadu"
    ],
    "City": [
        "Visakhapatnam", "Hyderabad", "Bengaluru",
        "Mumbai", "Chennai", "Vijayawada",
        "Warangal", "Mysuru", "Pune", "Coimbatore"
    ],
    "Crime Type": [
        "Theft", "Cybercrime", "Fraud", "Theft", "Assault",
        "Fraud", "Theft", "Cybercrime", "Assault", "Theft"
    ],
    "Year": [
        2021, 2022, 2023, 2024, 2021,
        2022, 2023, 2024, 2022, 2023
    ],
    "Cases": [120, 180, 95, 220, 80, 90, 130, 110, 210, 75]
})

st.sidebar.header("🔎 Filters")

states = st.sidebar.multiselect(
    "Select State",
    sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

years = st.sidebar.multiselect(
    "Select Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

filtered = df[
    df["State"].isin(states) &
    df["Year"].isin(years)
]

a, b, c = st.columns(3)
a.metric("Total Cases", int(filtered["Cases"].sum()))
b.metric("States", filtered["State"].nunique())
c.metric("Cities", filtered["City"].nunique())

left, right = st.columns(2)

with left:
    st.subheader("Crime Type Analysis")
    if not filtered.empty:
        chart = filtered.groupby(
            "Crime Type", as_index=False
        )["Cases"].sum()
        fig = px.bar(
            chart,
            x="Crime Type",
            y="Cases",
            color="Crime Type",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("State-wise Analysis")
    if not filtered.empty:
        chart = filtered.groupby(
            "State", as_index=False
        )["Cases"].sum()
        fig = px.pie(
            chart,
            names="State",
            values="Cases",
            hole=0.4,
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Crime Records")
st.dataframe(filtered, use_container_width=True, hide_index=True)

st.download_button(
    "Download Sample CSV",
    data=df.to_csv(index=False),
    file_name="sample_crime_data.csv",
    mime="text/csv"
)

st.info(
    "These are fictional sample values for learning only, "
    "not official crime statistics or live police data."
)