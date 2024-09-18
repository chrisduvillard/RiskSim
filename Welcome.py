import streamlit as st

# Set the page configuration with a custom title, icon, and layout
st.set_page_config(
    page_title="Risk Management Simulator",
    page_icon="🎲",
    layout="wide",
)

# Main title and subtitle
st.title("Welcome to the Risk Management Simulator 🎲")
st.markdown("### Empowering Your Trading Decisions Through Risk Analysis")

# Place an image in the app
# Replace 'header_image.jpg' with the path to your image file
st.image('docs/images/header_image.jpg', use_column_width=False, width=700)  # Image width - 350 pixels

# Explanations about the various pages
st.markdown("""
---
#### Navigate Through the App Using the Sidebar:

- **Risk-Return Analysis**: 
    - Explore how different trading parameters affect your expected returns and risks.
    - Simulate various scenarios to understand potential outcomes.
- **Win Rate Analysis** *(Coming Soon)*:
    - Delve into how changes in win rates impact your overall performance.
    - Visualize the sensitivity of your strategy to win rate variations.
- **Advanced Metrics** *(Coming Soon)*:
    - Analyze advanced risk metrics like Sharpe Ratio, Sortino Ratio, and more.
    - Optimize your strategy based on these key performance indicators.

---
#### About This App

Understanding and managing risk is crucial for successful trading and investing. This simulator allows you to:

- **Visualize** the impact of key trading parameters.
- **Simulate** different scenarios to make informed decisions.
- **Optimize** your strategies for better risk-adjusted returns.

Whether you're a novice trader or an experienced professional, this tool is designed to provide valuable insights into your trading performance.

---
#### How to Use

1. **Select a Page**: Use the sidebar on the left to navigate between different analyses.
2. **Adjust Parameters**: Each page contains interactive controls to modify simulation parameters.
3. **Run Simulations**: Click on 'Run Simulation' to generate updated results based on your inputs.
4. **Interpret Results**: Use the provided charts and metrics to understand the potential outcomes.

---
*Developed by [Christophe Duvillard](https://www.linkedin.com/in/christopheduvillard/).*

""")
