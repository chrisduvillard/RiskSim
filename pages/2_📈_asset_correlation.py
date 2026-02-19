import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st

from utils.style import footer


def is_positive_definite(matrix: np.ndarray) -> bool:
    """Check if a matrix is positive definite."""
    return bool(np.all(np.linalg.eigvals(matrix) > 0))


def nearest_positive_definite(A: np.ndarray) -> np.ndarray:
    """Find the nearest positive-definite matrix to input A."""
    B = (A + A.T) / 2
    _, s, Vh = np.linalg.svd(B)
    H = np.dot(Vh.T, np.dot(np.diag(s), Vh))
    A2 = (B + H) / 2
    A3 = (A2 + A2.T) / 2

    if is_positive_definite(A3):
        return A3

    spacing = np.spacing(np.linalg.norm(A))
    identity = np.eye(A.shape[0])
    k = 1
    while not is_positive_definite(A3):
        min_eig = np.min(np.real(np.linalg.eigvals(A3)))
        A3 += identity * (-min_eig * k**2 + spacing)
        k += 1
    return A3


def generate_uniform_correlation_matrix(n: int, corr: float) -> np.ndarray:
    """Generate a correlation matrix where all off-diagonal entries equal corr."""
    corr_matrix = np.full((n, n), corr)
    np.fill_diagonal(corr_matrix, 1.0)
    return corr_matrix


def generate_random_correlation_matrix(
    n: int, min_corr: float, max_corr: float
) -> np.ndarray:
    """Generate a random symmetric correlation matrix with values in [min_corr, max_corr]."""
    rng = np.random.default_rng()
    random_corrs = rng.uniform(low=min_corr, high=max_corr, size=(n, n))
    corr_matrix = (random_corrs + random_corrs.T) / 2
    np.fill_diagonal(corr_matrix, 1.0)
    return corr_matrix


def calculate_metrics(
    prices: pd.Series,
    returns: pd.Series,
    num_years: int,
    risk_free_rate: float,
) -> dict:
    """Calculate performance metrics for an asset or portfolio."""
    total_return = prices.iloc[-1] / prices.iloc[0] - 1
    annualized_return = (1 + total_return) ** (1 / num_years) - 1
    annualized_volatility = returns.std() * np.sqrt(252)
    max_drawdown = ((prices.cummax() - prices) / prices.cummax()).max()
    sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility

    target_return = 0
    downside_returns = returns[returns < target_return]
    if len(downside_returns) > 0:
        downside_deviation = (
            np.sqrt((downside_returns**2).mean()) * np.sqrt(252)
        )
        sortino_ratio = (annualized_return - risk_free_rate) / downside_deviation
    else:
        sortino_ratio = np.nan

    calmar_ratio = annualized_return / max_drawdown if max_drawdown != 0 else np.nan

    return {
        "Total Cumulative Return": total_return,
        "Annualized Return": annualized_return,
        "Annualized Volatility": annualized_volatility,
        "Maximum Drawdown": max_drawdown,
        "Sharpe Ratio": sharpe_ratio,
        "Sortino Ratio": sortino_ratio,
        "Calmar Ratio": calmar_ratio,
    }


def simulate_portfolio(
    num_assets: int,
    corr_matrix: np.ndarray,
    mean_vector: np.ndarray,
    volatility_vector: np.ndarray,
    trading_days: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Simulate asset prices from a multivariate normal model.

    Returns:
        Tuple of (prices DataFrame, log_returns DataFrame).
    """
    stddev_matrix = np.diag(volatility_vector)
    cov_matrix = stddev_matrix @ corr_matrix @ stddev_matrix

    log_returns = np.random.multivariate_normal(
        mean=mean_vector - 0.5 * volatility_vector**2,
        cov=cov_matrix,
        size=trading_days,
    )
    columns = [f"Asset {i + 1}" for i in range(num_assets)]
    log_returns_df = pd.DataFrame(log_returns, columns=columns)

    prices = np.exp(log_returns_df.cumsum()) * 100
    portfolio = prices.mean(axis=1)
    prices["Portfolio"] = portfolio

    return prices, log_returns_df


def style_metrics_table(metrics_df: pd.DataFrame):
    """Apply formatting and conditional highlighting to a metrics DataFrame."""
    styled = metrics_df.style.format(
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

    def highlight_max(s):
        is_max = s == s.max()
        return ["background-color: lightgreen" if v else "" for v in is_max]

    def highlight_min(s):
        is_min = s == s.min()
        return ["background-color: lightcoral" if v else "" for v in is_min]

    highlight_rules = {
        "Total Cumulative Return": highlight_max,
        "Annualized Return": highlight_max,
        "Annualized Volatility": highlight_min,
        "Maximum Drawdown": highlight_min,
        "Sharpe Ratio": highlight_max,
        "Sortino Ratio": highlight_max,
        "Calmar Ratio": highlight_max,
    }

    for metric, func in highlight_rules.items():
        styled = styled.apply(func, subset=[metric])

    return styled


def app():
    """Main function for the Asset Correlation page."""
    st.title("Synthetic Asset Portfolio Simulator")
    st.markdown(
        "This app simulates the price evolution of a portfolio of assets "
        "with different correlations."
    )

    # --- Sidebar inputs ---
    st.sidebar.header("Simulation Parameters")
    num_assets = st.sidebar.slider(
        "Number of Assets", min_value=1, max_value=50, value=10
    )

    st.sidebar.header("Correlation Parameters")
    corr_type = st.sidebar.selectbox(
        "Correlation Type",
        ("Use single correlation", "Specify correlation range"),
        help="Choose how to set correlations between assets.",
    )

    if corr_type == "Use single correlation":
        correlation = st.sidebar.slider(
            "Average Correlation between Assets",
            min_value=-1.0, max_value=1.0, value=0.4, step=0.01, format="%.2f",
        )
        min_corr = max_corr = None
    else:
        min_corr = st.sidebar.slider(
            "Minimum Correlation",
            min_value=-1.0, max_value=1.0, value=-0.2, step=0.01, format="%.2f",
            help="Minimum correlation between assets.",
        )
        max_corr = st.sidebar.slider(
            "Maximum Correlation",
            min_value=-1.0, max_value=1.0, value=0.6, step=0.01, format="%.2f",
            help="Maximum correlation between assets.",
        )
        correlation = None
        if min_corr > max_corr:
            st.sidebar.error(
                "Minimum correlation cannot be greater than maximum correlation."
            )

    num_years = st.sidebar.slider(
        "Number of Years to Plot", min_value=1, max_value=10, value=5
    )

    st.sidebar.header("Return Parameters")
    mean_annual_return = st.sidebar.number_input(
        "Mean Annual Return (%)", value=10.0, step=0.1
    )
    annual_volatility = st.sidebar.number_input(
        "Annual Volatility (%)", value=20.0, step=0.1
    )
    risk_free_rate = st.sidebar.number_input(
        "Risk-Free Rate (%)", value=0.0, step=0.01
    )

    st.sidebar.header("Advanced Options")
    randomize_mean = st.sidebar.checkbox(
        "Randomize Mean Returns", value=False,
        help="If checked, mean returns will vary across assets.",
    )
    randomize_volatility = st.sidebar.checkbox(
        "Randomize Volatility", value=False,
        help="If checked, volatilities will vary across assets.",
    )

    # --- Run simulation on button click ---
    if not st.sidebar.button("Run Simulation"):
        st.info("Adjust parameters in the sidebar, then click **Run Simulation**.")
        footer()
        return

    with st.spinner("Running simulation..."):
        # Convert to decimals
        mean_annual_ret = mean_annual_return / 100
        annual_vol = annual_volatility / 100
        rf_rate = risk_free_rate / 100

        trading_days_per_year = 252
        mean_daily_return = (1 + mean_annual_ret) ** (1 / trading_days_per_year) - 1
        daily_volatility = annual_vol / np.sqrt(trading_days_per_year)
        trading_days = num_years * trading_days_per_year

        # Generate per-asset parameters
        if randomize_mean:
            mean_vector = np.random.uniform(
                low=mean_daily_return * 0.5, high=mean_daily_return * 1.5,
                size=num_assets,
            )
        else:
            mean_vector = np.full(num_assets, mean_daily_return)

        if randomize_volatility:
            volatility_vector = np.random.uniform(
                low=daily_volatility * 0.5, high=daily_volatility * 1.5,
                size=num_assets,
            )
        else:
            volatility_vector = np.full(num_assets, daily_volatility)

        # Build correlation matrix
        if corr_type == "Use single correlation":
            corr_matrix = generate_uniform_correlation_matrix(num_assets, correlation)
        else:
            corr_matrix = generate_random_correlation_matrix(
                num_assets, min_corr, max_corr
            )
            corr_matrix = nearest_positive_definite(corr_matrix)

        if not is_positive_definite(corr_matrix):
            st.error(
                "The correlation matrix is not positive definite. "
                "Please adjust the correlation settings."
            )
            footer()
            return

        # --- Main simulation ---
        prices, log_returns = simulate_portfolio(
            num_assets, corr_matrix, mean_vector, volatility_vector, trading_days,
        )

        # Price chart
        st.header("Asset Price Simulation")
        fig = go.Figure()
        for column in prices.columns:
            fig.add_trace(
                go.Scatter(x=prices.index, y=prices[column], name=column)
            )
        fig.update_layout(
            xaxis_title="Trading Days", yaxis_title="Price",
            legend_title="Assets", height=600,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Per-asset metrics
        st.header("Performance Metrics")
        metrics_data = []
        for column in log_returns.columns:
            m = calculate_metrics(
                prices[column], log_returns[column], num_years, rf_rate,
            )
            m["Asset"] = column
            metrics_data.append(m)

        portfolio_returns = log_returns.mean(axis=1)
        m = calculate_metrics(
            prices["Portfolio"], portfolio_returns, num_years, rf_rate,
        )
        m["Asset"] = "Portfolio"
        metrics_data.append(m)

        metrics_df = pd.DataFrame(metrics_data).set_index("Asset")
        st.table(style_metrics_table(metrics_df))

        # Correlation heatmap
        st.header("Correlation Matrix")
        asset_labels = [f"Asset {i + 1}" for i in range(num_assets)]
        corr_df = pd.DataFrame(
            corr_matrix, columns=asset_labels, index=asset_labels,
        )
        fig_corr = px.imshow(
            corr_df, text_auto=".2f", aspect="auto",
            color_continuous_scale="viridis", origin="lower",
            title="Asset Correlation Matrix",
        )
        fig_corr.update_layout(height=600)
        st.plotly_chart(fig_corr, use_container_width=True)

        # --- Correlation sweep ---
        st.header("Portfolio Performance Across Different Correlations")
        correlation_values = np.arange(-1.0, 1.1, 0.2)
        portfolio_prices_dict = {}
        skipped_correlations = []
        metrics_correlations = []

        for corr in correlation_values:
            if corr_type == "Use single correlation":
                sweep_corr_matrix = generate_uniform_correlation_matrix(
                    num_assets, corr,
                )
            else:
                sweep_corr_matrix = generate_random_correlation_matrix(
                    num_assets, min_corr, max_corr,
                )
                sweep_corr_matrix = nearest_positive_definite(sweep_corr_matrix)

            if not is_positive_definite(sweep_corr_matrix):
                skipped_correlations.append(corr)
                continue

            sweep_prices, sweep_log_returns = simulate_portfolio(
                num_assets, sweep_corr_matrix, mean_vector,
                volatility_vector, trading_days,
            )
            portfolio_prices_dict[f"Corr {corr:.1f}"] = sweep_prices["Portfolio"]

            sweep_portfolio_returns = sweep_log_returns.mean(axis=1)
            pm = calculate_metrics(
                sweep_prices["Portfolio"], sweep_portfolio_returns,
                num_years, rf_rate,
            )
            pm["Correlation"] = f"{corr:.1f}"
            metrics_correlations.append(pm)

        if portfolio_prices_dict:
            portfolio_prices_df = pd.DataFrame(portfolio_prices_dict)
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
                xaxis_title="Trading Days", yaxis_title="Portfolio Price",
                legend_title="Correlation", height=600,
            )
            st.plotly_chart(fig2, use_container_width=True)

            st.header("Performance Metrics Across Different Correlations")
            metrics_df_corr = pd.DataFrame(metrics_correlations).set_index(
                "Correlation"
            )
            st.table(style_metrics_table(metrics_df_corr))

        if skipped_correlations:
            st.warning(
                "The following correlation values were skipped because they "
                "resulted in non-positive definite correlation matrices: "
                + ", ".join(f"{c:.1f}" for c in skipped_correlations)
            )

    footer()


app()
