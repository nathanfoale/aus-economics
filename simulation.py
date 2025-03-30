import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# === Page Setup ===
st.set_page_config(page_title="Housing Supply Simulation", layout="wide")
st.title("\U0001F3E8 Housing Supply Stress Simulation Dashboard")

# === Constants ===
years = list(range(2024, 2030))
initial_population = 26.7  # million

# === Sidebar User Inputs ===
st.sidebar.header("\U0001F527 Simulation Settings")
people_per_home = st.sidebar.slider("People per Household", 1.8, 3.5, 2.5, 0.1)
backlog = st.sidebar.number_input("Initial Housing Backlog (Homes)", value=30000, step=1000)
rba_elasticity = st.sidebar.slider("RBA Price Elasticity Factor", 1.0, 5.0, 2.5)

# === Growth Rates and Scenarios ===
growth_rates = {
    "ABS (1.3%)": 0.013,
    "Treasury (1.4%)": 0.014,
    "High Migration (1.7%)": 0.017,
    "Labor Budget Migration Path": "custom"
}

supply_scenarios = {
    "Labor Target (240k/year)": 240_000,
    "Labor Full Plan (240k + 18k aff.)": 240_000 + (18_000 / 5),
    "Moderate Shortfall (180k/year)": 180_000,
    "Severe Shortfall (150k/year)": 150_000
}

grate = st.sidebar.selectbox("Population Growth Path", list(growth_rates.keys()))
supply = st.sidebar.selectbox("Housing Supply Scenario", list(supply_scenarios.keys()))

# === Simulation Function ===
def simulate(growth_rate, supply_per_year):
    if growth_rate == "custom":
        net_migration = [435_000, 335_000, 260_000, 225_000, 225_000]
        pop = [initial_population * 1e6]
        for mig in net_migration:
            pop.append(pop[-1] + mig)
        pop = [p / 1e6 for p in pop]  # back to millions
    else:
        pop = [initial_population]
        for _ in range(1, len(years)):
            pop.append(pop[-1] * (1 + growth_rate))

    demand = [(pop[i] - pop[i - 1]) * 1e6 / people_per_home for i in range(1, len(pop))]
    cum_demand = np.cumsum(demand) + backlog
    cum_supply = np.cumsum([supply_per_year] * len(demand))
    price_pressure = ((cum_demand - cum_supply) / cum_demand) * rba_elasticity * 100
    net_surplus = cum_supply - cum_demand
    return demand, cum_demand, cum_supply, price_pressure, net_surplus

# === Run Simulation ===
g_rate = growth_rates[grate]
s_val = supply_scenarios[supply]
d, cum_d, cum_s, p, u = simulate(g_rate, s_val)
final_surplus = u[-1]

# === Plot ===
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    row_heights=[0.35, 0.33, 0.32],
    subplot_titles=[
        "\U0001F3D7️ Cumulative Housing Demand vs Supply",
        "\U0001F4C8 Estimated Rental Price Pressure (%)",
        "\U0001F3E1 Net Housing Surplus (Positive = Oversupply)"
    ]
)

fig.add_trace(go.Scatter(x=years[1:], y=cum_d, name="Demand", line=dict(color="firebrick", width=3)), row=1, col=1)
fig.add_trace(go.Scatter(x=years[1:], y=cum_s, name="Supply", line=dict(color="seagreen", width=3)), row=1, col=1)
fig.add_trace(go.Scatter(x=years[1:], y=p, name="Price Pressure %", line=dict(color="darkorange", width=3, dash="dash")), row=2, col=1)
fig.add_trace(go.Scatter(x=years[1:], y=u, name="Net Surplus", line=dict(color="royalblue", width=3)), row=3, col=1)
fig.add_hline(y=0, line_dash="dot", line_color="gray", row=3, col=1)

fig.update_layout(
    height=900,
    title=f"\U0001F3E8 Housing Simulation: {grate} + {supply}",
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(size=12)),
    xaxis_title="Year",
    yaxis_title="Homes",
    yaxis2_title="% Pressure",
    yaxis3_title="Surplus (Homes)",
    hovermode="x unified"
)

# === Narrative ===
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
### \U0001F4D6 Interpretation:
- **Red = Cumulative housing demand**
- **Green = Targeted housing supply**
- **Orange = Rental price pressure**
- **Blue = Net surplus or shortfall**
""")

# === Summary Output ===
st.markdown("""### \U0001F9FE Summary Metrics""")
st.metric("Final Net Housing Surplus", f"{int(final_surplus):,} homes")
st.metric("Total Demand (2024–2029)", f"{int(np.sum(d)):,} homes")
st.metric("Estimated Rent Pressure in 2029", f"{p[-1]:.1f}%")

# === Conditional Highlight ===
if final_surplus > 0:
    st.success(f"✅ Projected oversupply of {int(final_surplus):,} homes.")
elif final_surplus < 0:
    st.error(f"⚠️ Projected shortfall of {abs(int(final_surplus)):,} homes.")
else:
    st.info("⚖️ Demand and supply are perfectly balanced.")

# === Special Note ===
if grate == "Labor Budget Migration Path":
    st.info("\U0001F4CA This projection uses the Labor Budget’s staged migration intake strategy.")
