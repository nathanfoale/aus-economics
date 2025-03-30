import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Budget Dashboard", layout="wide")

# === Custom Styling for Bigger Checkboxes ===
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

# === Data ===
years = list(range(2023, 2031))

health = np.linspace(3, 6.5, len(years))
housing = np.linspace(2, 5, len(years))
edu = np.linspace(2, 3.5, len(years))
green = np.linspace(1, 4.2, len(years))
military = np.linspace(1.5, 3.2, len(years))

surplus = np.linspace(600, 780, len(years))

debt_au = np.linspace(36.8, 35.2, len(years))
oecd = np.linspace(120, 130, len(years))
usa = np.linspace(98, 96, len(years))
germany = np.linspace(68, 61, len(years))

income = np.linspace(350, 460, len(years))
corp = np.linspace(150, 180, len(years))
gst = np.linspace(100, 120, len(years))
cg = np.linspace(80, 110, len(years))

# === Layout ===
st.title("📊 Budget Strategy: Spending, Surplus & Debt Outlook")

# === Spending Controls
st.subheader("📈 New Government Spending by Category (2023–2030)")
cols = st.columns(5)
show_health = cols[0].checkbox("🏥 Health", True)
show_housing = cols[1].checkbox("🏠 Housing", True)
show_edu = cols[2].checkbox("🎓 Education", True)
show_green = cols[3].checkbox("🌱 Green Energy", True)
show_def = cols[4].checkbox("🪖 Military", True)

# === Plot 1: Spending
fig1 = go.Figure()
line_style = dict(width=5)  # Thicker for visibility and legend

if show_health:
    fig1.add_trace(go.Scatter(x=years, y=health, name="🏥 Health", stackgroup='one', line=dict(**line_style)))
if show_housing:
    fig1.add_trace(go.Scatter(x=years, y=housing, name="🏠 Housing", stackgroup='one', line=dict(**line_style)))
if show_edu:
    fig1.add_trace(go.Scatter(x=years, y=edu, name="🎓 Education", stackgroup='one', line=dict(**line_style)))
if show_green:
    fig1.add_trace(go.Scatter(x=years, y=green, name="🌱 Green Energy", stackgroup='one', line=dict(**line_style)))
if show_def:
    fig1.add_trace(go.Scatter(x=years, y=military, name="🪖 Military", stackgroup='one', line=dict(**line_style)))

fig1.update_layout(
    height=450,
    title="New Government Spending",
    legend=dict(
        font=dict(size=16),
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="center",
        x=0.5,
        itemsizing="constant"
    )
)
st.plotly_chart(fig1, use_container_width=True)

# === Plot 2: Surplus
st.subheader("💰 Surplus / Deficit Over Time")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=years, y=surplus, name="Surplus", line=dict(color="lime", width=5)))
fig2.update_layout(
    height=300,
    legend=dict(font=dict(size=14))
)
st.plotly_chart(fig2, use_container_width=True)

# === Debt-to-GDP Controls
st.subheader("🌍 International Debt-to-GDP (%)")
cols2 = st.columns(4)
show_au = cols2[0].checkbox("🇦🇺 Australia", True)
show_oecd = cols2[1].checkbox("🌍 OECD Avg", True)
show_usa = cols2[2].checkbox("🇺🇸 USA", True)
show_ger = cols2[3].checkbox("🇩🇪 Germany", True)

# === Plot 3: Debt-to-GDP
fig3 = go.Figure()
if show_au:
    fig3.add_trace(go.Scatter(x=years, y=debt_au, name="🇦🇺 Australia", line=dict(color="firebrick", width=5)))
if show_oecd:
    fig3.add_trace(go.Scatter(x=years, y=oecd, name="🌍 OECD Avg", line=dict(dash="dot", width=5)))
if show_usa:
    fig3.add_trace(go.Scatter(x=years, y=usa, name="🇺🇸 USA", line=dict(dash="dash", width=5)))
if show_ger:
    fig3.add_trace(go.Scatter(x=years, y=germany, name="🇩🇪 Germany", line=dict(dash="dashdot", width=5)))

fig3.update_layout(
    height=350,
    legend=dict(
        font=dict(size=16),
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="center",
        x=0.5,
        itemsizing="constant"
    )
)
st.plotly_chart(fig3, use_container_width=True)

# === Plot 4: Tax Revenue
st.subheader("🏦 Tax Revenue Breakdown")
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=years, y=income, name="👨‍💼 Income Tax", stackgroup='two', line=dict(width=5)))
fig4.add_trace(go.Scatter(x=years, y=corp, name="🏢 Corporate Tax", stackgroup='two', line=dict(width=5)))
fig4.add_trace(go.Scatter(x=years, y=gst, name="🛒 GST", stackgroup='two', line=dict(width=5)))
fig4.add_trace(go.Scatter(x=years, y=cg, name="📈 Capital Gains", stackgroup='two', line=dict(width=5)))

fig4.update_layout(
    height=350,
    legend=dict(
        font=dict(size=16),
        orientation="h",
        yanchor="bottom",
        y=1.05,
        xanchor="center",
        x=0.5,
        itemsizing="constant"
    )
)
st.plotly_chart(fig4, use_container_width=True)


