
# RiskSim: Risk-Return and Asset Correlation Simulator

**RiskSim** is a Python-based tool designed for portfolio and risk simulation. It offers an intuitive interface to model risk-return dynamics and assess portfolio performance under various asset correlation scenarios, providing deep insights into risk management strategies and investment outcomes.

## Link to the app

[Click here to access the app](https://risk-return-analysis.streamlit.app/)

## Features

- **Risk-Return Analysis**: Simulate various risk-return scenarios using adjustable parameters like win rate, trades per year, risk per trade, and return per unit of risk (RPUR). Uses Monte Carlo simulation to estimate expected returns and drawdowns.
- **Asset Correlation Simulator**: Generate and visualize portfolio performance based on customizable asset correlation matrices, with options for single or random correlation ranges. Computes Sharpe, Sortino, Calmar ratios, max drawdown, and more.

## Screenshots

![Risk-Return Analysis Screenshot](docs/images/image.png)
*Risk-Return Analysis Page*

![Risk-Return Analysis Screenshot](docs/images/image_2.png)
*Risk-Return Analysis Page*

![Asset Correlation Screenshot](docs/images/image_3.png)
*Asset Correlation Simulation Page*

![Asset Correlation Screenshot](docs/images/image_4.png)
*Asset Correlation Simulation Page*

## Project Structure

```
RiskSim/
├── Welcome.py                         # Streamlit entrypoint (landing page)
├── pages/
│   ├── 1_🎯_risk_return_analysis.py   # Risk-return Monte Carlo simulation
│   └── 2_📈_asset_correlation.py      # Asset correlation portfolio simulator
├── config/
│   └── slider_configs.py              # Centralized slider defaults and bounds
├── utils/
│   ├── risk_simulation.py             # TradingSimulator class + drawdown simulation
│   └── style.py                       # Footer and metric box HTML helpers
├── tests/
│   ├── test_risk_simulation.py        # Tests for simulation logic
│   └── test_style.py                  # Tests for style helpers
├── docs/
│   ├── audit_report.md                # Codebase audit report
│   └── images/                        # Screenshots and header image
├── .github/workflows/ci.yml           # GitHub Actions CI (ruff + pytest)
├── pyproject.toml                     # Ruff and pytest configuration
├── requirements.txt                   # Python dependencies
├── CHANGELOG.md                       # Change log
├── LICENSE.txt                        # MIT License
└── README.md
```

## Setup

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/chrisduvillard/RiskSim.git
cd RiskSim

# Create and activate a virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run Welcome.py
```

This launches the app in your browser. Use the sidebar to navigate between pages.

### Run Tests

```bash
pip install pytest
pytest -v
```

### Run Linter

```bash
pip install ruff
ruff check .
```

## Methodology

### Risk-Return Analysis

The Risk-Return Analysis page uses **Monte Carlo simulation** to model trading outcomes. Given a set of parameters (number of trades per year, win rate, risk per trade, and return per unit of risk), the simulator:

1. Generates random trade sequences where each trade is a win or loss based on the specified win rate
2. Applies compounding: each trade's P&L is a percentage of the *current* AUM (not the initial capital)
3. Repeats this process thousands of times to build a distribution of outcomes
4. Reports average returns across different RPUR levels and win rates
5. Estimates the expected maximum consecutive-loss drawdown

### Asset Correlation Simulation

The Asset Correlation page generates synthetic multi-asset portfolios using **correlated geometric Brownian motion**:

1. Builds a correlation matrix (uniform or random within a range), ensuring positive definiteness
2. Constructs a covariance matrix from per-asset volatilities and the correlation matrix
3. Samples multivariate normal log-returns and converts to price paths
4. Computes per-asset and portfolio performance metrics (Sharpe, Sortino, Calmar, max drawdown)
5. Sweeps across correlation levels to show how diversification affects portfolio risk

## License

This project is licensed under the MIT License. See the [LICENSE.txt](LICENSE.txt) file for details.

## Author

Made by [Christophe Duvillard](https://www.linkedin.com/in/christopheduvillard/)
