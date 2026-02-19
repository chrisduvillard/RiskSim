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

