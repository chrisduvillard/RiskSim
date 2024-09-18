import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# Set the page layout
st.set_page_config(layout="wide")

# Title
st.title("Synthetic Asset Portfolio Simulator")

# Subtitle and description
st.markdown(
    """
    This app simulates the price evolution of a portfolio of assets with different correlations.
    """
)

# Sidebar inputs
st.sidebar.header("Simulation Parameters")

# Number of assets
num_assets = st.sidebar.slider("Number of Assets", min_value=1, max_value=50, value=10)

# Correlation input
correlation = st.sidebar.slider(
    "Average Correlation between Assets",
    min_value=-1.0,
    max_value=1.0,
    value=0.4,
    step=0.01,
    format="%.2f",
)

# Number of years
num_years = st.sidebar.slider(
    "Number of Years to Plot", min_value=1, max_value=10, value=5
)

# Simulation parameters
st.sidebar.header("Return Parameters")

# Annual parameters
mean_annual_return = st.sidebar.number_input(
    "Mean Annual Return (%)", value=10.0, step=0.1
)
annual_volatility = st.sidebar.number_input(
    "Annual Volatility (%)", value=20.0, step=0.1
)

# Risk-free rate
risk_free_rate = st.sidebar.number_input("Risk-Free Rate (%)", value=0.0, step=0.01)

# Randomize mean returns
st.sidebar.header("Advanced Options")
randomize_mean = st.sidebar.checkbox(
    "Randomize Mean Returns",
    value=False,
    help="If checked, mean returns will vary across assets.",
)
randomize_volatility = st.sidebar.checkbox(
    "Randomize Volatility",
    value=False,
    help="If checked, volatilities will vary across assets.",
)

# Convert percentages to decimals
mean_annual_return /= 100
annual_volatility /= 100
risk_free_rate /= 100

# Trading days per year
trading_days_per_year = 252

# Convert annual parameters to daily
mean_daily_return = (1 + mean_annual_return) ** (1 / trading_days_per_year) - 1
daily_volatility = annual_volatility / np.sqrt(trading_days_per_year)

# Generate mean returns and volatilities per asset
if randomize_mean:
    mean_vector = np.random.uniform(
        low=mean_daily_return * 0.5, high=mean_daily_return * 1.5, size=num_assets
    )
else:
    mean_vector = np.full(num_assets, mean_daily_return)

if randomize_volatility:
    volatility_vector = np.random.uniform(
        low=daily_volatility * 0.5, high=daily_volatility * 1.5, size=num_assets
    )
else:
    volatility_vector = np.full(num_assets, daily_volatility)

# Generate the correlation matrix


def generate_correlation_matrix(n, corr):
    corr_matrix = np.full((n, n), corr)
    np.fill_diagonal(corr_matrix, 1.0)
    return corr_matrix

# Ensure positive definiteness


def is_positive_definite(matrix):
    return np.all(np.linalg.eigvals(matrix) > 0)


corr_matrix = generate_correlation_matrix(num_assets, correlation)

# Check for positive definiteness
if not is_positive_definite(corr_matrix):
    st.error(
        f"The correlation matrix is not positive definite for correlation={correlation:.2f} "
        f"and number of assets={num_assets}. Please adjust the correlation."
    )
else:
    # Number of trading days
    trading_days = num_years * trading_days_per_year

    # Generate the covariance matrix
    stddev_matrix = np.diag(volatility_vector)
    cov_matrix = stddev_matrix @ corr_matrix @ stddev_matrix

    # Generate log returns
    log_returns = np.random.multivariate_normal(
        mean=mean_vector - 0.5 * volatility_vector ** 2,
        cov=cov_matrix,
        size=trading_days,
    )
    log_returns = pd.DataFrame(
        log_returns, columns=[f"Asset {i+1}" for i in range(num_assets)]
    )

    # Calculate cumulative returns
    prices = np.exp(log_returns.cumsum())
    prices *= 100  # Start prices at 100

    # Calculate portfolio
    portfolio = prices.mean(axis=1)
    prices["Portfolio"] = portfolio

    # Plot the time series
    st.header("Asset Price Simulation")
    fig = go.Figure()

    for column in prices.columns:
        fig.add_trace(go.Scatter(x=prices.index, y=prices[column], name=column))

    fig.update_layout(
        xaxis_title="Trading Days",
        yaxis_title="Price",
        legend_title="Assets",
        height=600,
    )

    st.plotly_chart(fig, use_container_width=True)

    # Calculate metrics
    st.header("Performance Metrics")

    def calculate_metrics(prices, returns):
        metrics = {}
        total_return = prices.iloc[-1] / prices.iloc[0] - 1
        annualized_return = (1 + total_return) ** (1 / num_years) - 1
        annualized_volatility = returns.std() * np.sqrt(trading_days_per_year)
        max_drawdown = ((prices.cummax() - prices) / prices.cummax()).max()
        sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility

        # Downside deviation
        target_return = 0
        downside_returns = returns[returns < target_return]
        if len(downside_returns) > 0:
            downside_deviation = (
                np.sqrt((downside_returns ** 2).mean()) * np.sqrt(trading_days_per_year)
            )
            sortino_ratio = (annualized_return - risk_free_rate) / downside_deviation
        else:
            downside_deviation = np.nan
            sortino_ratio = np.nan

        calmar_ratio = annualized_return / max_drawdown

        metrics["Total Cumulative Return"] = total_return
        metrics["Annualized Return"] = annualized_return
        metrics["Annualized Volatility"] = annualized_volatility
        metrics["Maximum Drawdown"] = max_drawdown
        metrics["Sharpe Ratio"] = sharpe_ratio
        metrics["Sortino Ratio"] = sortino_ratio
        metrics["Calmar Ratio"] = calmar_ratio

        return metrics

    metrics_data = []

    for column in log_returns.columns:
        asset_prices = prices[column]
        asset_returns = log_returns[column]
        metrics = calculate_metrics(asset_prices, asset_returns)
        metrics["Asset"] = column
        metrics_data.append(metrics)

    # Portfolio metrics
    portfolio_returns = log_returns.mean(axis=1)
    portfolio_prices = prices["Portfolio"]
    metrics = calculate_metrics(portfolio_prices, portfolio_returns)
    metrics["Asset"] = "Portfolio"
    metrics_data.append(metrics)

    metrics_df = pd.DataFrame(metrics_data)
    metrics_df.set_index("Asset", inplace=True)

    # Format the dataframe
    styled_metrics_df = metrics_df.style.format(
        {
            "Total Cumulative Return": "{:.2%}",
            "Annualized Return": "{:.2%}",
            "Annualized Volatility": "{:.2%}",
            "Maximum Drawdown": "{:.2%}",
            "Sharpe Ratio": "{:.2f}",
            "Sortino Ratio": "{:.2f}",
            "Calmar Ratio": "{:.2f}",
        }
    )

    # Apply conditional formatting
    def highlight_max(s):
        is_max = s == s.max()
        return ["background-color: lightgreen" if v else "" for v in is_max]

    def highlight_min(s):
        is_min = s == s.min()
        return ["background-color: lightcoral" if v else "" for v in is_min]

    # Apply the highlighting to specific columns
    metrics_to_highlight = {
        "Total Cumulative Return": highlight_max,
        "Annualized Return": highlight_max,
        "Annualized Volatility": highlight_min,
        "Maximum Drawdown": highlight_min,
        "Sharpe Ratio": highlight_max,
        "Sortino Ratio": highlight_max,
        "Calmar Ratio": highlight_max,
    }

    for metric, func in metrics_to_highlight.items():
        styled_metrics_df = styled_metrics_df.apply(func, subset=[metric])

    st.table(styled_metrics_df)

    # Show correlation matrix
    st.header("Correlation Matrix")
    corr_df = pd.DataFrame(
        corr_matrix,
        columns=[f"Asset {i+1}" for i in range(num_assets)],
        index=[f"Asset {i+1}" for i in range(num_assets)],
    )
    st.dataframe(corr_df.style.format("{:.2f}"))

    # Second chart: Portfolios with different correlations
    st.header("Portfolio Performance Across Different Correlations")

    correlation_values = np.arange(-1.0, 1.1, 0.2)
    portfolio_prices_dict = {}
    skipped_correlations = []
    metrics_correlations = []

    for corr in correlation_values:
        # Generate the correlation matrix
        corr_matrix = generate_correlation_matrix(num_assets, corr)

        # Check for positive definiteness
        if not is_positive_definite(corr_matrix):
            skipped_correlations.append(corr)
            continue  # Skip this correlation value

        # Generate the covariance matrix
        stddev_matrix = np.diag(volatility_vector)
        cov_matrix = stddev_matrix @ corr_matrix @ stddev_matrix

        # Generate log returns
        log_returns = np.random.multivariate_normal(
            mean=mean_vector - 0.5 * volatility_vector ** 2,
            cov=cov_matrix,
            size=trading_days,
        )
        log_returns = pd.DataFrame(
            log_returns, columns=[f"Asset {i+1}" for i in range(num_assets)]
        )

        # Calculate cumulative returns
        prices = np.exp(log_returns.cumsum())
        prices *= 100  # Start prices at 100

        # Calculate portfolio
        portfolio = prices.mean(axis=1)
        portfolio_prices_dict[f"Corr {corr:.1f}"] = portfolio

        # Calculate portfolio metrics
        portfolio_returns = log_returns.mean(axis=1)
        portfolio_metrics = calculate_metrics(portfolio, portfolio_returns)
        portfolio_metrics["Correlation"] = f"{corr:.1f}"
        metrics_correlations.append(portfolio_metrics)

    # Check if we have any valid portfolios
    if portfolio_prices_dict:
        # Create a DataFrame of portfolios
        portfolio_prices_df = pd.DataFrame(portfolio_prices_dict)

        # Plot the portfolios
        fig2 = go.Figure()

        for column in portfolio_prices_df.columns:
            fig2.add_trace(
                go.Scatter(
                    x=portfolio_prices_df.index,
                    y=portfolio_prices_df[column],
                    name=column,
                )
            )

        fig2.update_layout(
            xaxis_title="Trading Days",
            yaxis_title="Portfolio Price",
            legend_title="Correlation",
            height=600,
        )

        st.plotly_chart(fig2, use_container_width=True)

        # Performance metrics table for portfolios with different correlations
        st.header("Performance Metrics Across Different Correlations")

        metrics_df_corr = pd.DataFrame(metrics_correlations)
        metrics_df_corr.set_index("Correlation", inplace=True)

        # Format the dataframe
        styled_metrics_df_corr = metrics_df_corr.style.format(
            {
                "Total Cumulative Return": "{:.2%}",
                "Annualized Return": "{:.2%}",
                "Annualized Volatility": "{:.2%}",
                "Maximum Drawdown": "{:.2%}",
                "Sharpe Ratio": "{:.2f}",
                "Sortino Ratio": "{:.2f}",
                "Calmar Ratio": "{:.2f}",
            }
        )

        # Apply conditional formatting
        for metric, func in metrics_to_highlight.items():
            styled_metrics_df_corr = styled_metrics_df_corr.apply(func, subset=[metric])

        st.table(styled_metrics_df_corr)

    if skipped_correlations:
        st.warning(
            f"The following correlation values were skipped because they resulted in non-positive definite correlation matrices: {', '.join([f'{c:.1f}' for c in skipped_correlations])}"
        )
