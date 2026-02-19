import streamlit as st

st.set_page_config(
    page_title="RiskSim: Risk Management Simulator",
    page_icon="🎲",
    layout="wide",
)

st.markdown("""
    <h1 style="font-size: 3rem; font-weight: bold; text-align: center;">
        Welcome to the Risk Management Simulator 🎲
    </h1>
    <h3 style="font-size: 1.25rem; opacity: 0.6; text-align: center; margin-bottom: 25px;">
        Empowering Your Trading Decisions Through Risk Analysis
    </h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 4, 2])
with col2:
    st.image("docs/images/header_image.jpg", width=700)

st.markdown("""
---
#### Explore the Features of RiskSim:
**Navigate Through the App Using the Sidebar:**

- **Risk-Return Analysis**:
    - Simulate how various trading parameters, such as win rate, number of trades, and risk per trade, affect your overall performance.
    - Use Monte Carlo simulations to explore potential outcomes based on your trading strategy.
    - Visualize the trade-off between risk and return to optimize your approach.

- **Asset Correlation Simulation**:
    - Generate portfolios of assets with different correlation structures, and simulate their price evolution over time.
    - Adjust the number of assets, correlation range, and key return parameters to test portfolio performance.
    - Analyze performance metrics such as Sharpe Ratio, Maximum Drawdown, and Annualized Return to assess the strength of your portfolio under various correlation regimes.


---
#### How to Get Started:

1. **Select a Page**: Use the sidebar on the left to navigate between different analyses.
2. **Adjust Parameters**: Each page offers interactive controls to modify the simulation parameters.
3. **Run Simulations**: Click 'Run Simulation' to generate updated results based on your inputs.
4. **Analyze Results**: Use the charts and performance metrics to interpret the potential outcomes.

---
*Developed by [Christophe Duvillard](https://www.linkedin.com/in/christopheduvillard/), designed to help traders better manage their risk and improve decision-making.*
""")
