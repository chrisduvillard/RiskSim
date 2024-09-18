import streamlit as st

# Set the page configuration with a custom title, icon, and layout
st.set_page_config(
    page_title="RiskSim: Risk Management Simulator",
    page_icon="🎲",
    layout="wide",
)

# Main title and subtitle with enhanced styling
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        color: #2c3e50;
        font-weight: bold;
        text-align: center;
    }
    .sub-title {
        font-size: 1.25rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 25px;
    }
    </style>
    <h1 class="main-title">Welcome to the Risk Management Simulator 🎲</h1>
    <h3 class="sub-title">Empowering Your Trading Decisions Through Risk Analysis</h3>
""", unsafe_allow_html=True)

# Place an image in the app
# Replace 'header_image.jpg' with the path to your image file
st.image('docs/images/header_image.jpg', use_column_width=True, caption="Explore Risk and Portfolio Dynamics")

# Explanations about the various pages
st.markdown("""
---
#### 🔍 Explore the Features of RiskSim:
**Navigate Through the App Using the Sidebar:**

- **📊 Risk-Return Analysis**: 
    - Explore how different trading parameters affect your expected returns and risks.
    - Simulate various scenarios to understand potential outcomes.
- **📈 Win Rate Analysis** *(Coming Soon)*:
    - Dive deep into how win rate variations impact overall performance.
    - Visualize the sensitivity of your strategy to changes in win rate.
- **📉 Advanced Metrics** *(Coming Soon)*:
    - Analyze advanced metrics like the Sharpe Ratio, Sortino Ratio, and more.
    - Optimize your strategy with these key performance indicators for a comprehensive risk-return assessment.

---
#### 💡 Why Use This App?

In the world of trading and investing, **understanding risk** is fundamental. This app empowers you to:

- **Visualize** how key trading parameters impact performance.
- **Simulate** various scenarios to make data-driven decisions.
- **Optimize** your strategy for improved risk-adjusted returns.

Whether you're new to trading or an experienced professional, RiskSim is designed to offer valuable insights for improving your strategy.

---
#### 📘 How to Get Started:

1. **Select a Page**: Use the sidebar on the left to navigate between different analyses.
2. **Adjust Parameters**: Each page offers interactive controls to modify the simulation parameters.
3. **Run Simulations**: Click 'Run Simulation' to generate updated results based on your inputs.
4. **Analyze Results**: Use the charts and performance metrics to interpret the potential outcomes.

---
*Developed by [Christophe Duvillard](https://www.linkedin.com/in/christopheduvillard/), designed to help traders better manage their risk and improve decision-making.*
""")
