import random
import numpy as np


class TradingSimulator:
    """
    A class to simulate trading strategies and their impact on AUM (Assets Under Management).

    Attributes:
        initial_aum (float): Initial assets under management.
        win_rate (float): Probability of a trade being a win.
        trades_per_year (int): Number of trades made per year.
        risk_per_trade (float): Fraction of current AUM risked per trade.
    """

    def __init__(self, initial_aum, win_rate, trades_per_year, risk_per_trade):
        """
        Initializes the TradingSimulator with the given parameters.

        Args:
            initial_aum (float): Initial assets under management.
            win_rate (float): Probability of a trade being a win.
            trades_per_year (int): Number of trades made per year.
            risk_per_trade (float): Fraction of current AUM risked per trade.
        """
        self.initial_aum = initial_aum
        self.win_rate = win_rate
        self.trades_per_year = trades_per_year
        self.risk_per_trade = risk_per_trade

    def simulate_trade(self, current_aum, is_win, return_per_unit_risk):
        """
        Simulates the outcome of a single trade.

        Args:
            current_aum (float): Current assets under management.
            is_win (bool): Whether the trade is a win or loss.
            return_per_unit_risk (float): Return per unit risk taken.

        Returns:
            float: Updated assets under management after the trade.
        """
        risk_per_trade = self.risk_per_trade * current_aum
        return current_aum + (risk_per_trade * return_per_unit_risk if is_win else -risk_per_trade)

    def simulate_year(self, return_per_unit_risk, num_simulations=10000):
        """
        Simulates the trading outcomes over a year for a given number of simulations.

        Args:
            return_per_unit_risk (float): Return per unit risk taken.
            num_simulations (int): Number of simulations to run. Defaults to 10000.

        Returns:
            list: A list containing the final AUM for each simulation.
        """
        results = []
        for _ in range(num_simulations):
            current_aum = self.initial_aum
            # Create a list of trade outcomes based on win rate
            trade_outcomes = [True] * int(self.win_rate * self.trades_per_year) + \
                             [False] * (self.trades_per_year - int(self.win_rate * self.trades_per_year))
            random.shuffle(trade_outcomes)
            # Simulate each trade
            for is_win in trade_outcomes:
                current_aum = self.simulate_trade(current_aum, is_win, return_per_unit_risk)
            results.append(current_aum)
        return results

    def average_trade_progression(self, return_per_unit_risk, num_simulations=10000):
        """
        Calculates the average progression of AUM over a year across multiple simulations.

        Args:
            return_per_unit_risk (float): Return per unit risk taken.
            num_simulations (int): Number of simulations to run. Defaults to 10000.

        Returns:
            numpy.ndarray: An array containing the average AUM at each trade step.
        """
        trades_per_year = int(self.trades_per_year)
        all_aum_series = np.zeros((num_simulations, trades_per_year + 1))
        for i in range(num_simulations):
            current_aum = self.initial_aum
            # Create a list of trade outcomes based on win rate
            trade_outcomes = [True] * int(self.win_rate * trades_per_year) + \
                             [False] * (trades_per_year - int(self.win_rate * trades_per_year))
            np.random.shuffle(trade_outcomes)
            aum_series = [current_aum]
            # Simulate each trade and record AUM progression
            for is_win in trade_outcomes:
                current_aum = self.simulate_trade(current_aum, is_win, return_per_unit_risk)
                aum_series.append(current_aum)
            all_aum_series[i] = aum_series
        return np.mean(all_aum_series, axis=0)


def simulate_portfolio_risk(num_assets, correlation, num_simulations=200):
    """
    Simulates the risk of a portfolio given the number of assets and their correlation.

    Args:
        num_assets (int): Number of assets in the portfolio.
        correlation (float): Correlation between the assets.
        num_simulations (int): Number of simulations to run. Defaults to 200.

    Returns:
        float: The average portfolio risk across the simulations.
    """
    risks = []
    for _ in range(num_simulations):
        # Generate random returns for each asset
        asset_returns = np.random.normal(0, 1, (num_assets, 252))
        # Create a covariance matrix based on the correlation
        cov_matrix = np.full((num_assets, num_assets), correlation)
        np.fill_diagonal(cov_matrix, 1)
        # Generate correlated returns using Cholesky decomposition
        L = np.linalg.cholesky(cov_matrix)
        correlated_returns = np.dot(L, asset_returns)
        # Calculate the portfolio return and risk
        portfolio_return = np.mean(correlated_returns, axis=0)
        portfolio_risk = np.std(portfolio_return)
        risks.append(portfolio_risk)
    return np.mean(risks)
