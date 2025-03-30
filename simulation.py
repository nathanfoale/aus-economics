import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# === Page Setup ===
st.set_page_config(page_title="Housing Supply Simulation", layout="wide")
st.title("🏘️ Housing Supply Stress Simulation Dashboard")

# === Constants ===
years = list(range(2024, 2030))
initial_population = 26.7
people_per_home = 2.5
backlog = 30_000
rba_elasticity = 2.5

# === Population growth rates
growth_rates = {
    "ABS (1.3%)": 0.013,
    "Treasury (1.4%)": 0.014,
    "High Migration (1.7%)": 0.017,
    "Labor Budget Migration Path": "custom"
}

# === Housing supply scenarios
supply_scenarios = {
    "Labor Target (240k/year)": 240_000,
    "Labor Full Plan (240k + 18k aff.)": 240_000 + (18_000 / 5),
    "Moderate Shortfall (180k/year)": 180_000,
    "Severe Shortfall (150k/year)": 150_000
}

# === Simulation function ===
def simulate(growth_rate, supply_per_year):
    if growth_rate == "custom":
        net_migration = [435_000, 335_000, 260_000, 225_000, 225_000]
        pop = [initial_population * 1e6]
        for mig in net_migration:
            pop.append(pop[-1] + mig)
        pop = [p / 1e6 for p in pop]  # Convert back to millions
    else:
        pop = [initial_population]
        for _ in range(1, len(years)):
            pop.append(pop[-1] * (1 + growth_rate))

    demand = [(pop[i] - pop[i - 1]) * 1e6 / people_per_home for i in range(1, len(pop))]
    cum_demand = np.cumsum(demand) + backlog
    cum_supply = np.cumsum([supply_per_year] * len(demand))
    price_pressure = ((cum_demand - cum_supply) / cum_demand) * rba_elasticity * 100
    net_surplus = cum_supply - cum_demand
    return cum_demand, cum_supply, price_pressure, net_surplus

# === User Inputs ===
st.sidebar.header("Simulation Settings")
grate = st.sidebar.selectbox("Population Growth", list(growth_rates.keys()))
supply = st.sidebar.selectbox("Supply Scenario", list(supply_scenarios.keys()))

# === Run simulation ===
g_rate = growth_rates[grate]
s_val = supply_scenarios[supply]
d, s, p, u = simulate(g_rate, s_val)

# === Plot ===
fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.08,
    row_heights=[0.35, 0.33, 0.32],
    subplot_titles=[
        "🏗️ Cumulative Housing Demand vs Supply",
        "📈 Estimated Rental Price Pressure (%)",
        "🏡 Net Housing Surplus (Positive = Oversupply)"
    ]
)

fig.add_trace(go.Scatter(x=years[1:], y=d, name="Demand", line=dict(color="firebrick", width=3)), row=1, col=1)
fig.add_trace(go.Scatter(x=years[1:], y=s, name="Supply", line=dict(color="seagreen", width=3)), row=1, col=1)
fig.add_trace(go.Scatter(x=years[1:], y=p, name="Price Pressure %", line=dict(color="darkorange", width=3, dash="dash")), row=2, col=1)
fig.add_trace(go.Scatter(x=years[1:], y=u, name="Net Surplus", line=dict(color="royalblue", width=3)), row=3, col=1)
fig.add_hline(y=0, line_dash="dot", line_color="gray", row=3, col=1)

fig.update_layout(
    height=900,
    title=f"🏘️ Housing Supply Stress Simulation: {grate} + {supply}",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="center",
        x=0.5,
        font=dict(size=12)
    ),
    xaxis_title="Year",
    yaxis_title="Homes",
    yaxis2_title="% Pressure",
    yaxis3_title="Surplus (Homes)",
    hovermode="x unified"
)

# === Narrative ===
st.markdown("""
### 📘 Interpretation:
- **Red = Cumulative housing demand** (based on population)
- **Green = Labor housing supply goal**
- **Orange = Rental price pressure**, 
- **Blue = Net surplus or shortfall.**

""")

st.plotly_chart(fig, use_container_width=True)



