import numpy as np
import plotly.express as plotly_express
import plotly.graph_objects as go
import streamlit as st

from config.slider_configs import SLIDER_CONFIGS
from utils.risk_simulation import TradingSimulator, simulate_drawdown
from utils.style import footer, metric_box


def _viridis_colors(values: list[float]) -> list[str]:
    """Map a list of numeric values to Viridis color scale strings."""
    min_val, max_val = min(values), max(values)
    span = max_val - min_val
    normalized = [
        (v - min_val) / span if span != 0 else 0.5 for v in values
    ]
    colorscale = plotly_express.colors.sequential.Viridis
    return [colorscale[int(n * (len(colorscale) - 1))] for n in normalized]


def _add_expected_return_annotation(
    fig: go.Figure,
    x_label: str,
    y_value: float,
    y_range: float,
) -> None:
    """Add an 'Expected Return' annotation arrow to a bar chart."""
    offset = y_range * 0.05 if y_range != 0 else 5
    fig.add_annotation(
        x=x_label,
        y=y_value + offset,
        text="Expected Return",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        ax=0,
        ay=-30,
        font=dict(family="Arial, sans-serif", size=14, color="black"),
        align="center",
        arrowcolor="black",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
        bgcolor="rgba(255, 255, 255, 0.9)",
        opacity=0.9,
    )


def create_bar_chart_figure(
    results: dict[float, list[float]],
    return_per_unit_risk_value: float,
) -> go.Figure:
    """Bar chart of average % return over different RPUR levels."""
    sorted_results = sorted(results.items(), key=lambda x: np.mean(x[1]))
    averages = [float(np.mean(data)) for _, data in sorted_results]
    colors = _viridis_colors(averages)
    x_labels = [f"RPR {rpur:.2f}" for rpur, _ in sorted_results]

    min_result, max_result = min(averages), max(averages)
    y_range = max_result - min_result
    y_tick_interval = y_range / 10 if y_range != 0 else 1
    y_ticks = np.arange(min_result, max_result + y_tick_interval, y_tick_interval)

    # Single trace with per-bar colors so categorical axis works correctly
    fig = go.Figure(go.Bar(
        x=x_labels,
        y=averages,
        marker_color=colors,
        hoverinfo="text",
        hovertext=[f"RPUR: {rpur:.2f}<br>Avg Return: {avg:.2f}%"
                   for (rpur, _), avg in zip(sorted_results, averages)],
        text=[f"{avg:.2f}%" for avg in averages],
        textposition="outside",
        textfont=dict(size=12, color="black"),
    ))

    fig.update_layout(
        title="Average Percentage Return Over Different Levels of Return Per Unit Risk",
        yaxis=dict(
            title="Average Percentage Return (%)",
            tickvals=y_ticks,
            ticktext=[f"{t:.2f}%" for t in y_ticks],
            showgrid=True, gridwidth=1, gridcolor="LightGrey",
        ),
        xaxis=dict(tickangle=-45, automargin=True),
        showlegend=False,
        height=600,
        font=dict(family="Helvetica, sans-serif", size=12, color="#333"),
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    avg_return_for_annotation = float(np.mean(results[return_per_unit_risk_value]))
    _add_expected_return_annotation(
        fig,
        x_label=f"RPR {return_per_unit_risk_value:.2f}",
        y_value=avg_return_for_annotation,
        y_range=y_range,
    )
    return fig


def create_win_rate_vs_return_chart(
    simulator: TradingSimulator,
    return_per_unit_risk: float,
    num_simulations: int = 10_000,
    win_rate_value: float | None = None,
) -> go.Figure:
    """Bar chart of average % return vs. win rate for a given RPUR."""
    win_rates = np.arange(
        SLIDER_CONFIGS["win_rate"]["min_value"],
        SLIDER_CONFIGS["win_rate"]["max_value"] + 1,
        2,
    )
    avg_returns: list[float] = []

    for wr in win_rates:
        simulator.win_rate = wr / 100
        final_aums = simulator.simulate_year(return_per_unit_risk, num_simulations)
        pct_returns = [(aum / simulator.initial_aum - 1) * 100 for aum in final_aums]
        avg_returns.append(float(np.mean(pct_returns)))

    colors = _viridis_colors(avg_returns)
    x_labels = [f"WR {r:.0f}" for r in win_rates]
    min_return, max_return = min(avg_returns), max(avg_returns)
    y_range = max_return - min_return
    y_ticks = np.arange(
        np.floor(min_return / 10) * 10,
        np.ceil(max_return / 10) * 10 + 10,
        10,
    )

    # Single trace with per-bar colors so categorical axis works correctly
    fig = go.Figure(go.Bar(
        x=x_labels,
        y=avg_returns,
        text=[f"{r:.2f}%" for r in avg_returns],
        textposition=["inside" if r < 0 else "outside" for r in avg_returns],
        marker_color=colors,
        textfont=dict(size=12),
        hoverinfo="text",
        hovertext=[f"Win Rate: {wr:.0f}%<br>Return: {r:.2f}%"
                   for wr, r in zip(win_rates, avg_returns)],
    ))

    fig.update_layout(
        title="Average Percentage Return vs. Win Rate",
        xaxis=dict(
            title="Win Rate (%)",
            tickangle=-45,
            automargin=True,
        ),
        yaxis=dict(
            title="Average Percentage Return (%)",
            tickvals=y_ticks,
            ticktext=[f"{t}%" for t in y_ticks],
            showgrid=True, gridwidth=1, gridcolor="LightGrey",
            range=[np.floor(min_return / 10) * 10, np.ceil(max_return / 10) * 10],
        ),
        showlegend=False,
        font=dict(family="Helvetica, sans-serif", size=12, color="#333"),
        height=600,
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    if win_rate_value is not None:
        avg_for_annotation = float(np.interp(win_rate_value, win_rates, avg_returns))
        _add_expected_return_annotation(
            fig,
            x_label=f"WR {win_rate_value:.0f}",
            y_value=avg_for_annotation,
            y_range=y_range,
        )

    return fig


def app() -> None:
    """Main function for the Risk-Return Analysis page."""
    st.markdown(
        '<h1 style="color: #1c2e4a;">Risk-Return Analysis</h1>',
        unsafe_allow_html=True,
    )
    st.markdown("""
        <div style="text-align: center; padding: 22px;">
            <h4 style="color: #5D6D7E;">Stay Alive Long Enough to Get Lucky</h4>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.header("Simulation Parameters ⚙️")
    st.sidebar.markdown(
        "<small><em>Adjust the parameters to simulate different "
        "risk management scenarios.</em></small>",
        unsafe_allow_html=True,
    )

    nb_trades_per_year = st.sidebar.slider(
        "Number of Trades per Year", **SLIDER_CONFIGS["trades_per_year"],
    )
    win_rate = st.sidebar.slider(
        "Avg Win Rate (%)", **SLIDER_CONFIGS["win_rate"],
    )
    risk_per_trade = st.sidebar.slider(
        "Risk per Trade (%)", **SLIDER_CONFIGS["risk_per_trade"],
    )
    return_per_unit_risk_value = st.sidebar.slider(
        "Avg Return Per Unit Risk", **SLIDER_CONFIGS["return_per_unit_risk"],
    )
    st.sidebar.markdown(
        "<small><em>RPUR: Return per Unit of Risk. "
        "This is the expected return for each unit of risk taken.</em></small>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        "<small><em>The max drawdown is the largest loss you could experience "
        "if all your losing trades occurred consecutively.</em></small>",
        unsafe_allow_html=True,
    )

    initial_aum = 100_000.0
    simulator = TradingSimulator(
        initial_aum, win_rate / 100, nb_trades_per_year, risk_per_trade / 100,
    )

    max_drawdown = nb_trades_per_year * (1 - win_rate / 100) * risk_per_trade
    average_drawdown = simulate_drawdown(
        win_rate, nb_trades_per_year, risk_per_trade, simulations=10_000,
    )

    # Display metrics
    cols = st.columns(6)
    metrics = [
        ("# of Trades/Year", f"{nb_trades_per_year}"),
        ("Win Rate", f"{win_rate}%"),
        ("Risk per Trade", f"{risk_per_trade}%"),
        ("Avg Return/Risk", f"{return_per_unit_risk_value}x"),
        ("Expected Drawdown", f"{round(average_drawdown, 1)}%"),
        ("Max Drawdown", f"{round(max_drawdown, 1)}%"),
    ]
    for col, (title, value) in zip(cols, metrics):
        with col:
            st.markdown(metric_box(title, value), unsafe_allow_html=True)

    st.write("")

    if st.sidebar.button("Run Simulation"):
        with st.spinner("Running simulations..."):
            results: dict[float, list[float]] = {}
            rpur_range = np.linspace(0.5, 8.0, num=16)
            for rpur in rpur_range:
                final_aums = simulator.simulate_year(
                    rpur, num_simulations=SLIDER_CONFIGS["num_simulations"]["value"],
                )
                results[rpur] = [(aum / initial_aum - 1) * 100 for aum in final_aums]

            tab1, tab2 = st.tabs(["RPUR Analysis", "Win Rate Analysis"])

            with tab1:
                fig = create_bar_chart_figure(results, return_per_unit_risk_value)
                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                fig = create_win_rate_vs_return_chart(
                    simulator, return_per_unit_risk_value, win_rate_value=win_rate,
                )
                st.plotly_chart(fig, use_container_width=True)


app()
footer()
