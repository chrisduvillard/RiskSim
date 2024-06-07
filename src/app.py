from config.slider_configs import SLIDER_CONFIGS
import numpy as np
import plotly.graph_objects as go
import plotly.express as plotly_express
import streamlit as st
from risk_simulation import TradingSimulator
from style import footer, metric_box
import sys
import os
# Add the root directory to the PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Now import the module

# Settings for Streamlit page appearance
st.set_page_config(layout="wide")

# App theme settings as 'Light' by default
st.markdown("""
    <style>
    body {
        color: #111;
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)


def create_bar_chart_figure(results, medians, return_per_unit_risk_value):
    """
    Create a bar chart figure representing the average percentage return 
    over different levels of return per unit risk (RPUR).

    Args:
        results (dict): A dictionary with RPUR values as keys and list of returns as values.
        medians (dict): A dictionary with RPUR values as keys and median returns as values.
        return_per_unit_risk_value (float): The RPUR value to highlight in the chart.

    Returns:
        go.Figure: A Plotly figure object.
    """
    # Sort results based on the average return
    sorted_results = sorted(results.items(), key=lambda x: np.mean(x[1]))
    min_result = min(np.mean(data) for _, data in sorted_results)
    max_result = max(np.mean(data) for _, data in sorted_results)

    # Calculate the range and tick intervals for the y-axis
    y_range = max_result - min_result
    y_tick_interval = y_range / 10
    y_ticks = np.arange(min_result, max_result + y_tick_interval, y_tick_interval)
    y_tick_labels = [f'{tick:.2f}%' for tick in y_ticks]

    # Normalize the data for color scaling
    normalized_data = [(np.mean(data) - min_result) / (max_result - min_result) for _, data in sorted_results]
    colorscale = plotly_express.colors.sequential.Viridis
    colors = [colorscale[int(norm_val * (len(colorscale) - 1))] for norm_val in normalized_data]

    # Create the bar chart
    fig = go.Figure()
    for i, (rpur, data) in enumerate(sorted_results):
        avg_result = np.mean(data)
        fig.add_trace(go.Bar(
            x=[f'RPR {rpur:.2f}'],
            y=[avg_result],
            marker_color=colors[i],
            hoverinfo='text',
            hovertext=f'RPUR: {rpur:.2f}<br>Avg Return: {avg_result:.2f}%',
            text=[f'{avg_result:.2f}%'],
            textposition='outside',
            textfont=dict(size=12, color="black")
        ))

    # Update the layout of the chart
    fig.update_layout(
        title='Average Percentage Return Over Different Levels of Return Per Unit Risk',
        yaxis=dict(
            title='Average Percentage Return (%)',
            tickvals=y_ticks,
            ticktext=y_tick_labels,
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGrey'
        ),
        xaxis=dict(tickangle=-45, automargin=True),
        showlegend=False,
        height=600,
        font=dict(family="Helvetica, sans-serif", size=12, color="#333")
    )

    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    # Add an annotation for the selected RPUR value
    avg_return_for_annotation = np.mean(results[return_per_unit_risk_value])
    annotation_y = avg_return_for_annotation + y_range * 0.05
    fig.add_annotation(
        x=f'RPR {return_per_unit_risk_value:.2f}',
        y=annotation_y,
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
        opacity=0.9
    )

    return fig


def create_win_rate_vs_return_chart(simulator, return_per_unit_risk, num_simulations=10_000, win_rate_value=None):
    """
    Create a bar chart figure representing the average percentage return 
    versus win rate for a given return per unit risk (RPUR).

    Args:
        simulator (TradingSimulator): An instance of TradingSimulator.
        return_per_unit_risk (float): The RPUR value to simulate.
        num_simulations (int): The number of simulations to run.
        win_rate_value (float, optional): The win rate value to highlight in the chart.

    Returns:
        go.Figure: A Plotly figure object.
    """
    # Define the range of win rates to simulate
    win_rates = np.arange(SLIDER_CONFIGS['win_rate']['min_value'], SLIDER_CONFIGS['win_rate']['max_value'] + 1, 2)
    avg_returns = []

    # Simulate the average returns for each win rate
    for win_rate in win_rates:
        simulator.win_rate = win_rate / 100
        final_aums = simulator.simulate_year(return_per_unit_risk, num_simulations)
        percentage_returns = [(aum / simulator.initial_aum - 1) * 100 for aum in final_aums]
        avg_returns.append(np.mean(percentage_returns))

    min_return, max_return = min(avg_returns), max(avg_returns)
    normalized_data = [(ret - min_return) / (max_return - min_return) for ret in avg_returns]
    colorscale = plotly_express.colors.sequential.Viridis
    colors = [colorscale[int(norm_val * (len(colorscale) - 1))] for norm_val in normalized_data]

    # Create the bar chart
    fig = go.Figure()
    for i, (rate, ret) in enumerate(zip(win_rates, avg_returns)):
        text_position = 'inside' if ret < 0 else 'outside'
        text_color = 'white' if ret < 0 else 'black'
        fig.add_trace(go.Bar(
            x=[f"{rate}%"],
            y=[ret],
            text=[f"{ret:.2f}%"],
            textposition=text_position,
            marker_color=colors[i],
            textfont=dict(color=text_color, size=12),
            hoverinfo='text',
            hovertext=f"Win Rate: {rate}%<br>Return: {ret:.2f}%"
        ))

    y_range = max_return - min_return
    y_ticks = np.arange(np.floor(min_return / 10) * 10, np.ceil(max_return / 10) * 10 + 10, 10)
    y_tick_labels = [f'{tick}%' for tick in y_ticks]

    # Update the layout of the chart
    fig.update_layout(
        title='Average Percentage Return vs. Win Rate',
        xaxis=dict(
            title='Win Rate (%)',
            tickvals=win_rates,
            ticktext=[f'{tick}%' for tick in win_rates]
        ),
        yaxis=dict(
            title='Average Percentage Return (%)',
            tickvals=y_ticks,
            ticktext=y_tick_labels,
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGrey',
            range=[np.floor(min_return / 10) * 10, np.ceil(max_return / 10) * 10]
        ),
        showlegend=False,
        font=dict(family="Helvetica, sans-serif", size=12, color="#333"),
        height=600
    )

    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    # Add an annotation for the selected win rate value
    if win_rate_value is not None:
        avg_return_for_annotation = np.interp(win_rate_value, win_rates, avg_returns)
        annotation_y = avg_return_for_annotation + y_range * 0.05
        fig.add_annotation(
            x=f"{win_rate_value}",
            y=annotation_y,
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
            opacity=0.9
        )

    return fig


def simulate_trades(win_rate, num_trades_per_year, risk_per_trade, simulations=1000):
    win_rate = win_rate / 100

    def max_drawdown(trades):
        max_dd = 0
        current_dd = 0
        for trade in trades:
            if trade == 0:  # Losing trade
                current_dd += 1
                max_dd = max(max_dd, current_dd)
            else:  # Winning trade
                current_dd = 0
        return max_dd * risk_per_trade

    drawdowns = []

    for _ in range(simulations):
        # Generate trades: 1 for win, 0 for loss
        trades = np.random.choice([1, 0], size=num_trades_per_year, p=[win_rate, 1 - win_rate])
        # Shuffle the trades
        np.random.shuffle(trades)
        # Calculate maximum drawdown for this scenario
        drawdowns.append(max_drawdown(trades))

    # Calculate average drawdown
    average_drawdown = np.mean(drawdowns)

    return average_drawdown


def app():
    """
    The main function to run the Streamlit application for the risk management simulator.
    """
    st.markdown("""
        <h1 style="color: #1c2e4a;">🎲 Risk-Return Analysis</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align: center; padding: 22px;">
            <h4 style="color: #5D6D7E;">Stay Alive Long Enough to Get Lucky</h4>
            <p style="font-style: italic; color: #5D6D7E;">Jason Shapiro</p>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.header("Simulation Parameters️ ⚙️")
    st.sidebar.markdown(
        "<small><em>Adjust the parameters to simulate different risk management scenarios.</em></small>",
        unsafe_allow_html=True
    )

    # Sidebar sliders for simulation parameters
    nb_trades_per_year = st.sidebar.slider("Number of Trades per Year", **SLIDER_CONFIGS["trades_per_year"])
    win_rate = st.sidebar.slider("Avg Win Rate (%)", **SLIDER_CONFIGS["win_rate"])
    risk_per_trade = st.sidebar.slider("Risk per Trade (%)", **SLIDER_CONFIGS["risk_per_trade"])
    return_per_unit_risk_value = st.sidebar.slider("Avg Return Per Unit Risk", **SLIDER_CONFIGS["return_per_unit_risk"])
    st.sidebar.markdown(
        "<small><em>RPUR: Return per Unit of Risk. This is the expected return for each unit of risk taken.</em></small>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<small><em>The max drawdown is the largest loss you could experience if all your losing trades occurred consecutively.</em></small>",
        unsafe_allow_html=True
    )

    initial_aum = 100_000.0
    simulator = TradingSimulator(initial_aum, win_rate / 100, nb_trades_per_year, risk_per_trade / 100)

    # Calculate the maximum drawdown
    max_drawdown = nb_trades_per_year * (1 - win_rate / 100) * risk_per_trade
    average_drawdown = simulate_trades(win_rate, nb_trades_per_year, risk_per_trade, simulations=10_000)

    # Display the simulation parameters as metrics
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.markdown(metric_box("# of Trades/Year", f"{nb_trades_per_year}"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_box("Win Rate", f"{win_rate}%"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_box("Risk per Trade", f"{risk_per_trade}%"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_box("Avg Return/Risk", f"{return_per_unit_risk_value}x"), unsafe_allow_html=True)
    with col5:
        st.markdown(metric_box("Expected Drawdown", f"{round(average_drawdown,1)}%"), unsafe_allow_html=True)
    with col6:
        st.markdown(metric_box("Max Drawdown", f"{round(max_drawdown,1)}%"), unsafe_allow_html=True)

    # Add some additional spacing after the metrics
    st.write("")

    # Run the simulation when the button is clicked
    if st.sidebar.button("Run Simulation"):
        with st.spinner("Running simulations..."):
            results = {}
            medians = {}
            rpur_range = np.linspace(0.5, 8.0, num=16)
            for rpur in rpur_range:
                final_aums = simulator.simulate_year(rpur, num_simulations=SLIDER_CONFIGS["num_simulations"]["value"])
                percentage_returns = [(aum / initial_aum - 1) * 100 for aum in final_aums]
                results[rpur] = percentage_returns
                medians[rpur] = np.median(percentage_returns)

            # Create tabs for different analyses
            tab1, tab2 = st.tabs(["RPUR Analysis", "Win Rate Analysis"])

            with tab1:
                bar_chart_fig = create_bar_chart_figure(results, medians, return_per_unit_risk_value)
                st.plotly_chart(bar_chart_fig, use_container_width=True)

            with tab2:
                win_rate_vs_return_fig = create_win_rate_vs_return_chart(simulator, return_per_unit_risk_value, win_rate_value=win_rate)
                st.plotly_chart(win_rate_vs_return_fig, use_container_width=True)


if __name__ == "__main__":
    app()
    footer()
