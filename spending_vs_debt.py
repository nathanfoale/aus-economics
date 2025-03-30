import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Budget Dashboard", layout="wide")

st.markdown("""
    <style>
        input[type="checkbox"] {
            transform: scale(1.5);
            margin-right: 10px;
        }
        label[data-testid="stMarkdownContainer"] > div {
            font-size: 1.2rem;
        }
    </style>
""", unsafe_allow_html=True)

# === Data (Realistic Treasury/ABS-Inspired) ===
years = list(range(2023, 2031))

health = np.linspace(124.8, 135, len(years))
housing = np.linspace(21, 25, len(years))
edu = np.linspace(54.0, 60, len(years))
green = np.linspace(1.2, 3.5, len(years))
military = np.linspace(51.5, 56, len(years))

surplus = [-27.6, -42.1, -35.7, -37.2, -36.9, -30, -25, -20]  # 2024–2031

income = np.linspace(357.8, 390, len(years))
corp = np.linspace(145.5, 160, len(years))
gst = np.linspace(99.3, 110, len(years))
cg = np.linspace(42.8, 60, len(years))  # Combining super + other taxes as proxy

debt_au = [33.7, 35.5, 36.5, 36.9, 36.8, 36.2, 35.0, 33.5]
oecd = [120, 125, 128, 130, 131, 132, 134, 135]
usa = [98, 97, 96, 96, 95, 95, 94, 93]
germany = [68, 65, 63, 61, 60, 60, 59, 58]

# === Additional Datasets ===
cpi_years = [2020, 2021, 2022, 2023, 2024]
cpi_values = [0.9, 3.5, 6.8, 7.8, 3.6]
real_wage_growth = [0.2, -1.2, -3.0, -2.3, 0.5]
time = [2020, 2021, 2022, 2023, 2024]
wpi = [1.4, 2.3, 3.1, 3.6, 4.1]
unemployment = [6.9, 5.1, 3.5, 3.6, 3.9]

world_labels = ["Australia", "USA", "OECD Avg", "Germany"]
debt_values = [35.5, 97, 120, 61]
spend_values = [27, 37, 45, 49]

# === Layout ===
st.title("\U0001F4CA Labor Budget Strategy: Spending, Surplus & Debt Outlook")


# === New Government Spending by Category ===
st.subheader("\U0001F4C8 New Government Spending by Category (2023–2030)")
cols = st.columns(5)
show_health = cols[0].checkbox("\U0001F3E5 Health", True)
show_housing = cols[1].checkbox("\U0001F3E0 Housing", True)
show_edu = cols[2].checkbox("\U0001F393 Education", True)
show_green = cols[3].checkbox("\U0001F331 Green Energy", True)
show_def = cols[4].checkbox("\U0001FA96 Military", True)

fig1 = go.Figure()
line_style = dict(width=5)
if show_health:
    fig1.add_trace(go.Scatter(x=years, y=health, name="\U0001F3E5 Health", stackgroup='one', line=dict(**line_style)))
if show_housing:
    fig1.add_trace(go.Scatter(x=years, y=housing, name="\U0001F3E0 Housing", stackgroup='one', line=dict(**line_style)))
if show_edu:
    fig1.add_trace(go.Scatter(x=years, y=edu, name="\U0001F393 Education", stackgroup='one', line=dict(**line_style)))
if show_green:
    fig1.add_trace(go.Scatter(x=years, y=green, name="\U0001F331 Green Energy", stackgroup='one', line=dict(**line_style)))
if show_def:
    fig1.add_trace(go.Scatter(x=years, y=military, name="\U0001FA96 Military", stackgroup='one', line=dict(**line_style)))

fig1.update_layout(
    height=450,
    title="New Government Spending",
    legend=dict(font=dict(size=16), orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5)
)
st.plotly_chart(fig1, use_container_width=True)

# === Expandable Sections by Category ===
with st.expander("\U0001F3E1 Housing Programs Detail (2025–26)"):
    st.markdown("""
    - $21 billion committed to housing programs
    - $6.3 billion in support for first home buyers
    - $9.3 billion to combat homelessness
    - $4.5 billion for state housing infrastructure backlogs
    """)

with st.expander("\U0001F3E5 Health Spending Detail (2025–26)"):
    st.markdown("""
    - $124.8 billion total health funding
    - $3.4 billion for aged care reforms
    - $2.2 billion for Medicare and PBS expansion
    - $1.2 billion in mental health initiatives
    """)

with st.expander("\U0001F393 Education Spending Detail (2025–26)"):
    st.markdown("""
    - $54 billion on education and training
    - $1.8 billion for universities and research
    - $1.5 billion for school upgrades and equity programs
    - $750 million in vocational training and apprenticeships
    - 20% reduction in student HELP and other student debts (pending legislation), cutting $16 billion in total
    - Income repayment threshold raised to $67,000 in 2025–26
    - Indexation change removes $3 billion in past student debt
    - Example: Sachini's debt drops from $35k to $28k and repayment from $2,800 to $1,950
    """)

with st.expander("\U0001F331 Green Energy & Climate Detail (2025–26)"):
    st.markdown("""
    - $1.2 billion for energy transformation
    - $500 million for clean hydrogen development
    - $300 million for net zero transition support
    - $150 million for nature and biodiversity protection
    - $1.3 billion for solar battery rollout & community energy
    - $1 billion for clean transport transition
    - $17 billion infrastructure spend across rail, ports, EV routes
    - $300 million for net zero support for heavy industry
    """)

with st.expander("\U0001FA96 Military and Defence Spending Detail (2025–26)"):
    st.markdown("""
    - $51.5 billion defence budget
    - $9.3 billion on AUKUS and submarine capabilities
    - $4.2 billion for cyber and space defence
    - $1.8 billion for veteran support and housing
    """)

# === Surplus ===
st.subheader("\U0001F4B0 Surplus / Deficit Over Time")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=years, y=surplus, name="Surplus", line=dict(color="lime", width=5)))
fig2.update_layout(height=300, legend=dict(font=dict(size=14)))
st.plotly_chart(fig2, use_container_width=True)

# === Debt ===
st.subheader("\U0001F30D International Debt-to-GDP (%)")
cols2 = st.columns(4)
show_au = cols2[0].checkbox("\U0001F1E6\U0001F1FA Australia", True)
show_oecd = cols2[1].checkbox("\U0001F30D OECD Avg", True)
show_usa = cols2[2].checkbox("\U0001F1FA\U0001F1F8 USA", True)
show_ger = cols2[3].checkbox("\U0001F1E9\U0001F1EA Germany", True)

fig3 = go.Figure()
if show_au:
    fig3.add_trace(go.Scatter(x=years, y=debt_au, name="\U0001F1E6\U0001F1FA Australia", line=dict(color="firebrick", width=5)))
if show_oecd:
    fig3.add_trace(go.Scatter(x=years, y=oecd, name="\U0001F30D OECD Avg", line=dict(dash="dot", width=5)))
if show_usa:
    fig3.add_trace(go.Scatter(x=years, y=usa, name="\U0001F1FA\U0001F1F8 USA", line=dict(dash="dash", width=5)))
if show_ger:
    fig3.add_trace(go.Scatter(x=years, y=germany, name="\U0001F1E9\U0001F1EA Germany", line=dict(dash="dashdot", width=5)))

fig3.update_layout(height=350, legend=dict(font=dict(size=16), orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5))
st.plotly_chart(fig3, use_container_width=True)

# === Tax Revenue ===
st.subheader("\U0001F3E6 Tax Revenue Breakdown")
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=years, y=income, name="\U0001F468‍\U0001F4BC Income Tax", stackgroup='two', line=dict(width=5)))
fig4.add_trace(go.Scatter(x=years, y=corp, name="\U0001F3E2 Corporate Tax", stackgroup='two', line=dict(width=5)))
fig4.add_trace(go.Scatter(x=years, y=gst, name="\U0001F6D2 GST", stackgroup='two', line=dict(width=5)))
fig4.add_trace(go.Scatter(x=years, y=cg, name="\U0001F4C8 Capital Gains (Proxy)", stackgroup='two', line=dict(width=5)))

fig4.update_layout(
    height=350,
    legend=dict(font=dict(size=16), orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5)
)

st.plotly_chart(fig4, use_container_width=True)

labels = ['Income Tax', 'Company/Resource Tax', 'GST', 'Other']
values = [357.8, 145.5, 99.3, 78.4]  # Roughly aligned with budget numbers
colors = ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0']

fig_rev = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker=dict(colors=colors))])

st.plotly_chart(fig_rev, use_container_width=True)

# === Cost of Living Section ===
st.header("\U0001F6D2 Cost of Living Pressures")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Annual CPI Inflation (%)")
    fig_cpi = go.Figure()
    fig_cpi.add_trace(go.Bar(x=cpi_years, y=cpi_values, name="CPI Inflation", marker_color='orange'))
    fig_cpi.update_layout(height=300, xaxis_title="Year", yaxis_title="%", title="CPI Inflation Rate")
    st.plotly_chart(fig_cpi, use_container_width=True)

with col2:
    st.markdown("""
    #### Budget Relief Measures:
    - $300 energy relief to all households
    - 20% HELP/student debt cut (~$7,000 average)
    - PBS medicines capped at $31.60
    - $536/year average Stage 3 tax cut
    """)

# === Jobs & Wages ===
st.header("\U0001F4BC Jobs & Wages")
fig_jobs = go.Figure()
fig_jobs.add_trace(go.Scatter(x=time, y=wpi, mode='lines+markers', name="Wage Price Index (WPI)", line=dict(width=4)))
fig_jobs.add_trace(go.Scatter(x=time, y=real_wage_growth, mode='lines+markers', name="Real Wage Growth", line=dict(width=4, dash='dash')))
fig_jobs.add_trace(go.Scatter(x=time, y=unemployment, mode='lines+markers', name="Unemployment Rate", line=dict(width=4, dash='dot')))
fig_jobs.update_layout(height=400, title="WPI, Real Wage Growth & Unemployment", xaxis_title="Year")
st.plotly_chart(fig_jobs, use_container_width=True)

# === Australia vs World ===
st.title("\U0001F30D Australia vs. World")

st.subheader("Debt to GDP and Spending Comparison")
fig_world = go.Figure()
fig_world.add_trace(go.Bar(x=world_labels, y=debt_values, name="Debt to GDP (%)", marker_color='firebrick'))
fig_world.add_trace(go.Bar(x=world_labels, y=spend_values, name="Gov Spending (% GDP)", marker_color='royalblue'))
fig_world.update_layout(barmode='group', height=400, title="Debt & Spending: Australia vs. OECD Peers", yaxis_title="%")
st.plotly_chart(fig_world, use_container_width=True)

# === International Benchmarking ===
st.header("\U0001F30E International Benchmarking")
st.markdown("Compare Australia’s position globally on key spending and economic metrics.")

benchmark_labels = ["Australia", "USA", "OECD Avg", "Germany"]

# === Combined GDP and Gov Spending per Capita ===
gdp_per_capita = [67500, 80500, 52300, 56000]  # USD (2024 est)
spending_per_capita = [29500, 33500, 26700, 29100]  # USD (proxy est)

fig_combined = go.Figure()

fig_combined.add_trace(go.Bar(
    x=benchmark_labels,
    y=gdp_per_capita,
    name="GDP per Capita",
    marker_color="royalblue"
))

fig_combined.add_trace(go.Bar(
    x=benchmark_labels,
    y=spending_per_capita,
    name="Gov Spending per Capita",
    marker_color="darkcyan"
))

fig_combined.update_layout(
    barmode='group',
    height=400,
    title="GDP vs Gov Spending per Capita (USD, 2024)",
    xaxis_title="Country",
    yaxis_title="USD",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
)

st.plotly_chart(fig_combined, use_container_width=True)


# === Spending by Category as % of GDP ===
st.subheader("Key Spending Categories (% of GDP)")
categories = ["Health", "Education", "Defence", "Green Energy", "Housing"]
australia_pct = [9.6, 5.9, 2.0, 0.3, 1.4]
oecd_pct = [8.9, 4.8, 1.6, 0.5, 1.1]
us_pct = [17.0, 6.0, 3.5, 0.4, 1.2]
germany_pct = [11.2, 4.6, 1.4, 0.6, 0.9]

fig_pct = go.Figure()
fig_pct.add_trace(go.Bar(name='Australia', x=categories, y=australia_pct))
fig_pct.add_trace(go.Bar(name='USA', x=categories, y=us_pct))
fig_pct.add_trace(go.Bar(name='OECD Avg', x=categories, y=oecd_pct))
fig_pct.add_trace(go.Bar(name='Germany', x=categories, y=germany_pct))

fig_pct.update_layout(
    barmode='group',
    height=450,
    title="Category Spending as % of GDP",
    yaxis_title="% of GDP",
    xaxis_title="Category"
)
st.plotly_chart(fig_pct, use_container_width=True)


# === Global Economic Snapshot ===
st.sidebar.header("\U0001F30D Global Economic Snapshot")
st.sidebar.markdown("### Real GDP Growth (2025)")
st.sidebar.markdown("- **Australia:** 2.25%")
st.sidebar.markdown("- **USA:** 2.0%")
st.sidebar.markdown("- **China:** 5.0%")
st.sidebar.markdown("- **OECD Avg:** 1.7%")
st.sidebar.markdown("\n### Inflation Forecasts (2025)")
st.sidebar.markdown("- **Australia:** 2.5%")
st.sidebar.markdown("- **USA:** 2.3%")
st.sidebar.markdown("- **OECD Avg:** 2.6%")

# === 🔮 Future Budget Simulator ===
st.title("\U0001F9D9️ Interactive Budget Simulator (2025–2030)")

st.markdown("Adjust key categories to see potential impact on surplus and debt.")

col1, col2, col3, col4 = st.columns(4)
health_adj = col1.slider("Health Spending (%)", -10, 10, 0)
edu_adj = col2.slider("Education Spending (%)", -10, 10, 0)
housing_adj = col3.slider("Housing Spending (%)", -10, 10, 0)
defence_adj = col4.slider("Defence Spending (%)", -10, 10, 0)

# Budget impact multipliers (in $B per 1%)
health_multiplier = 1.3
edu_multiplier = 0.8
housing_multiplier = 0.9
defence_multiplier = 1.1

total_budget_impact = (
    health_adj * health_multiplier +
    edu_adj * edu_multiplier +
    housing_adj * housing_multiplier +
    defence_adj * defence_multiplier
)

base_surplus = [-27.6, -42.1, -35.7, -37.2, -36.9, -30, -25, -20]
updated_surplus = [s - total_budget_impact for s in base_surplus]

st.line_chart(updated_surplus, height=250)
st.caption("Note: Simulation is illustrative. 1% = ~$1.3B (health), $0.8B (edu), $0.9B (housing), $1.1B (defence)")


# === 🧪 Policy Scenario Buttons ===
st.subheader("🧪 Policy Scenario Simulator")
st.markdown("Choose a policy reform to simulate its impact.")

scenario = st.selectbox("Select a Policy Reform:", [
    "Stage 3 tax cuts delayed",
    "Increase rent assistance",
    "Boost early childhood funding"
])

if scenario == "Stage 3 tax cuts delayed":
    st.markdown("""
    <div style='background-color:#256029;padding:15px;border-radius:10px;color:white'>
        💰 <b>Estimated surplus boost:</b> $12B<br>
        🏠 <b>Avg household pays:</b> $536 more
    </div>
    """, unsafe_allow_html=True)

elif scenario == "Increase rent assistance":
    st.markdown("""
    <div style='background-color:#1b6ca8;padding:15px;border-radius:10px;color:white'>
        📉 <b>Surplus impact:</b> –$4.6B<br>
        👨‍👩‍👧 <b>Helps ~1.1M renters</b><br>
        📊 <b>CPI housing pressure reduced</b>
    </div>
    """, unsafe_allow_html=True)

elif scenario == "Boost early childhood funding":
    st.markdown("""
    <div style='background-color:#6b4caf;padding:15px;border-radius:10px;color:white'>
        🧒 <b>$5B investment into early childhood reforms</b><br>
        📈 <b>Boosts long-term GDP via productivity gains</b>
    </div>
    """, unsafe_allow_html=True)


# === 👤 Personal Budget Benefit Calculator ===
st.subheader("\U0001F9D1‍⚖️ How Does the Budget Affect Me?")

with st.form("personal_budget_form"):
    age = st.slider("Your Age:", 18, 80, 25)
    income = st.number_input("Annual Income ($):", value=60000)
    has_help = st.radio("Do you have student debt (HELP)?", ["Yes", "No"])
    renting = st.radio("Are you renting?", ["Yes", "No"])
    childcare = st.radio("Do you have children in early education?", ["Yes", "No"])
    state = st.selectbox("Your State or Territory", ["VIC", "NSW", "SA", "WA", "QLD", "TAS", "ACT", "NT"])
    submitted = st.form_submit_button("Calculate My Benefits")

if submitted:
    tax_cut = 536 if income > 45000 else 250
    help_benefit = 7000 if has_help == "Yes" else 0
    rent_multiplier = 1.2 if renting == "Yes" and state in ["NSW", "VIC"] else 1
    rent_benefit = int(700 * rent_multiplier) if renting == "Yes" else 0
    medicare_benefit = 180 if age >= 18 else 0
    childcare_benefit = 1500 if childcare == "Yes" else 0

    total = tax_cut + help_benefit + rent_benefit + medicare_benefit + childcare_benefit

    st.metric("\U0001F4B0 Total Estimated Benefit", f"${total:,}")
    st.markdown(f"""
- 💳 **Stage 3 Tax Cut**: ${tax_cut}
- 🎓 **HELP Debt Wipe**: ${help_benefit}
- 🏠 **Rent Assistance**: ${rent_benefit}
- 💊 **PBS/Medicare Relief**: ${medicare_benefit}
- 🧒 **Childcare Support**: ${childcare_benefit}
""")

    if total > 3000:
        st.success("✅ You're one of the bigger winners from the 2025 Budget!")
    elif total > 1000:
        st.info("📈 You'll receive meaningful cost-of-living support.")
    else:
        st.warning("💬 You may receive limited benefits. Consider exploring state-level relief programs.")


# === 📍 State-by-State Comparison ===
st.subheader("\U0001F5FA️ State-by-State Budget View")
st.markdown("Explore how funding and housing pressures differ by state.")

state = st.selectbox("Select State:", ["VIC", "NSW", "SA", "WA", "QLD", "TAS", "ACT", "NT"])

state_data = {
    "NSW": {"housing_funding": 5.2, "rent_growth": 7.1, "vacancy": 1.1},
    "VIC": {"housing_funding": 4.5, "rent_growth": 6.9, "vacancy": 1.3},
    "QLD": {"housing_funding": 3.9, "rent_growth": 8.2, "vacancy": 0.9},
    "WA": {"housing_funding": 2.1, "rent_growth": 5.8, "vacancy": 1.7},
    "SA": {"housing_funding": 1.8, "rent_growth": 5.0, "vacancy": 1.4},
    "TAS": {"housing_funding": 0.9, "rent_growth": 4.7, "vacancy": 1.5},
    "ACT": {"housing_funding": 1.0, "rent_growth": 3.5, "vacancy": 2.0},
    "NT": {"housing_funding": 0.6, "rent_growth": 2.8, "vacancy": 2.5},
}

data = state_data[state]
st.metric("Housing Funding ($B)", f"{data['housing_funding']:.1f}")
st.metric("Rent Growth (YoY %)", f"{data['rent_growth']:.1f}%")
st.metric("Vacancy Rate (%)", f"{data['vacancy']:.1f}%")




