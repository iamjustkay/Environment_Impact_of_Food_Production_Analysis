import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------------
# Config
# -------------------------------
st.set_page_config(page_title="🌱 Food Production Impact Dashboard", layout="wide")

st.title("🌍 Environmental Impact of Food Production")
st.markdown("#### Project 3 — Multi-Metric Sustainability Insights (GHG, Water, Land Use)")

# 🔗 GitHub repository link (adjust the URL to your repo)
st.markdown(
    "[View Details on GitHub](https://github.com/iamjustkay/Environment_Impact_of_Food_Production_Analysis)",
    unsafe_allow_html=True
) 

st.markdown("---")

# -------------------------------
# Load & prepare data
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Food_Production.csv")
    df = df.rename(columns={"Packging": "Packaging"})
    for c in df.columns:
        if c != "Food product":
            df[c] = pd.to_numeric(df[c], errors="coerce")

    stage_cols = ["Land use change", "Animal Feed", "Farm",
                  "Processing", "Transport", "Packaging", "Retail"]
    stage_cols = [c for c in stage_cols if c in df.columns]

    if "Total_emissions" in df.columns:
        stage_sum = df[stage_cols].sum(axis=1, skipna=True)
        discrepancy = (df["Total_emissions"] - stage_sum).abs()
        df["Total_emissions_clean"] = np.where(
            discrepancy > 1e-6, stage_sum,
            df["Total_emissions"].fillna(stage_sum)
        )
    else:
        df["Total_emissions_clean"] = df[stage_cols].sum(axis=1, skipna=True)

    return df, stage_cols

df, stage_cols = load_data()

# -------------------------------
# Sidebar filters
# -------------------------------
st.sidebar.header("🔎 Filters")
product_filter = st.sidebar.multiselect(
    "Select food products", options=df["Food product"].unique(),
    default=None
)
if product_filter:
    df = df[df["Food product"].isin(product_filter)]

# -------------------------------
# Q1. Highest GHG foods
# -------------------------------
st.subheader("Q1. Highest greenhouse gas emissions per kg")
q1 = df[["Food product", "Total_emissions_clean"]].dropna().sort_values(
    "Total_emissions_clean", ascending=False).head(10).sort_values("Total_emissions_clean")

fig1 = px.bar(
    q1, x="Total_emissions_clean", y="Food product", orientation="h",
    text="Total_emissions_clean",
    labels={"Total_emissions_clean": "kgCO₂e per kg", "Food product": ""}
)
fig1.update_traces(texttemplate="%{text:.2f}", textposition="outside")
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# Q2. Average emissions by stage
# -------------------------------
st.subheader("Q2. Average emissions by lifecycle stage")
if stage_cols:
    stage_means = df[stage_cols].mean().reset_index()
    stage_means.columns = ["Stage", "kgCO2e_per_kg"]

    fig2 = px.bar(
        stage_means.sort_values("kgCO2e_per_kg", ascending=False),
        x="Stage", y="kgCO2e_per_kg", text="kgCO2e_per_kg",
        labels={"kgCO2e_per_kg": "Avg. kgCO₂e per kg"}
    )
    fig2.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Q3. Breakdown for top 5 emitters
# -------------------------------
st.subheader("Q3. Lifecycle breakdown for top 5 emitting foods")
top5 = df.sort_values("Total_emissions_clean", ascending=False).head(5)["Food product"]
breakdown = df[df["Food product"].isin(top5)][["Food product"] + stage_cols]
long = breakdown.melt(id_vars="Food product", var_name="Stage", value_name="kgCO2e_per_kg")

fig3 = px.bar(
    long, x="kgCO2e_per_kg", y="Food product", color="Stage", orientation="h", barmode="stack",
    text="kgCO2e_per_kg"
)
fig3.update_traces(texttemplate="%{text:.2f}", textposition="inside")
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# Q4. Water vs GHG
# -------------------------------
st.subheader("Q4. Freshwater withdrawals vs. GHG emissions")
water_col = "Freshwater withdrawals per kilogram (liters per kilogram)"
if water_col in df.columns:
    scatter_df = df[["Food product", "Total_emissions_clean", water_col]].dropna()
    fig4 = px.scatter(
        scatter_df, x=water_col, y="Total_emissions_clean", #text="Food product",
        labels={"Total_emissions_clean": "kgCO₂e per kg", water_col: "Freshwater per kg (L)"}
    )
    fig4.update_traces(textposition="top center")
    st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# Q5. Land use
# -------------------------------
st.subheader("Q5. Highest land use per kg")
land_col = "Land use per kilogram (m² per kilogram)"
if land_col in df.columns:
    q5 = df[["Food product", land_col]].dropna().sort_values(land_col, ascending=False).head(10)
    fig5 = px.bar(
        q5.sort_values(land_col), x=land_col, y="Food product", orientation="h", text=land_col,
        labels={land_col: "m² land per kg"}
    )
    fig5.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig5, use_container_width=True)

# -------------------------------
# Q6. Emissions vs scarcity water
# -------------------------------
st.subheader("Q6. Emissions vs scarcity-weighted water use")
scarcity_col = "Scarcity-weighted water use per kilogram (liters per kilogram)"
if scarcity_col in df.columns:
    corr_df = df[["Total_emissions_clean", scarcity_col]].dropna()
    corr = corr_df["Total_emissions_clean"].corr(corr_df[scarcity_col])
    fig6 = px.scatter(
        corr_df, x=scarcity_col, y="Total_emissions_clean",
        labels={"Total_emissions_clean": "kgCO₂e per kg", scarcity_col: "Scarcity water (L/kg)"},
        title=f"Correlation (r = {corr:.2f})"
    )
    st.plotly_chart(fig6, use_container_width=True)

# -------------------------------
# Q7. Policy scenario
# -------------------------------
st.subheader("Q7. Reduction if Transport & Packaging cut by 50%")
scenario_cols = [c for c in ["Transport", "Packaging"] if c in df.columns]
if scenario_cols:
    scenario = df.copy()
    scenario["Scenario_emissions"] = df["Total_emissions_clean"]
    for c in scenario_cols:
        scenario["Scenario_emissions"] = scenario["Scenario_emissions"] - 0.5 * scenario[c].fillna(0)
    scenario["Reduction"] = df["Total_emissions_clean"] - scenario["Scenario_emissions"]

    q7 = scenario[["Food product", "Reduction"]].dropna().sort_values("Reduction", ascending=False).head(10)
    fig7 = px.bar(
        q7.sort_values("Reduction"), x="Reduction", y="Food product", orientation="h", text="Reduction",
        labels={"Reduction": "kgCO₂e saved per kg"}
    )
    fig7.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")
st.info("💡 Data source: Environmental impacts of food production dataset (Our World in Data).")
