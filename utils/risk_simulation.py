import numpy as np


class TradingSimulator:
    """Simulate trading strategies and their impact on AUM (Assets Under Management).

    Attributes:
        initial_aum: Initial assets under management.
        win_rate: Probability of a trade being a win (0-1).
        trades_per_year: Number of trades made per year.
        risk_per_trade: Fraction of current AUM risked per trade (0-1).
    """

    def __init__(
        self,
        initial_aum: float,
        win_rate: float,
        trades_per_year: int,
        risk_per_trade: float,
    ) -> None:
        self.initial_aum = initial_aum
        self.win_rate = win_rate
        self.trades_per_year = trades_per_year
        self.risk_per_trade = risk_per_trade

    def simulate_trade(
        self, current_aum: float, is_win: bool, return_per_unit_risk: float,
    ) -> float:
        """Simulate the outcome of a single trade.

        Returns:
            Updated AUM after the trade.
        """
        risk_amount = self.risk_per_trade * current_aum
        if is_win:
            return current_aum + risk_amount * return_per_unit_risk
        return current_aum - risk_amount

    def simulate_year(
        self, return_per_unit_risk: float, num_simulations: int = 10_000,
    ) -> list[float]:
        """Simulate trading outcomes over a year for multiple simulations.

        Returns:
            List of final AUM values, one per simulation.
        """
        n_wins = int(self.win_rate * self.trades_per_year)
        n_losses = self.trades_per_year - n_wins

        results: list[float] = []
        for _ in range(num_simulations):
            current_aum = self.initial_aum
            outcomes = np.array([True] * n_wins + [False] * n_losses)
            np.random.shuffle(outcomes)
            for is_win in outcomes:
                current_aum = self.simulate_trade(
                    current_aum, bool(is_win), return_per_unit_risk,
                )
            results.append(current_aum)
        return results


def simulate_drawdown(
    win_rate: float,
    num_trades_per_year: int,
    risk_per_trade: float,
    simulations: int = 1_000,
) -> float:
    """Estimate the average maximum consecutive-loss drawdown via Monte Carlo.

    Args:
        win_rate: Win rate as a percentage (0-100).
        num_trades_per_year: Number of trades per year.
        risk_per_trade: Risk per trade as a percentage.
        simulations: Number of simulations to run.

    Returns:
        Average maximum drawdown (in percentage units).
    """
    p_win = win_rate / 100.0

    def _max_consecutive_losses(trades: np.ndarray) -> int:
        max_streak = 0
        current_streak = 0
        for trade in trades:
            if trade == 0:
                current_streak += 1
                if current_streak > max_streak:
                    max_streak = current_streak
            else:
                current_streak = 0
        return max_streak

    drawdowns: list[float] = []
    for _ in range(simulations):
        trades = np.random.choice(
            [1, 0], size=num_trades_per_year, p=[p_win, 1 - p_win],
        )
        drawdowns.append(_max_consecutive_losses(trades) * risk_per_trade)

    return float(np.mean(drawdowns))
