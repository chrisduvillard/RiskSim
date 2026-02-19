"""Tests for utils.risk_simulation module."""

import numpy as np
import pytest

from utils.risk_simulation import TradingSimulator, simulate_drawdown

# ---------------------------------------------------------------------------
# TradingSimulator
# ---------------------------------------------------------------------------

class TestTradingSimulator:
    """Tests for the TradingSimulator class."""

    def _make_sim(
        self,
        initial_aum: float = 100_000.0,
        win_rate: float = 0.5,
        trades_per_year: int = 20,
        risk_per_trade: float = 0.01,
    ) -> TradingSimulator:
        return TradingSimulator(initial_aum, win_rate, trades_per_year, risk_per_trade)

    def test_init_stores_attributes(self) -> None:
        sim = self._make_sim(200_000, 0.6, 30, 0.02)
        assert sim.initial_aum == 200_000
        assert sim.win_rate == 0.6
        assert sim.trades_per_year == 30
        assert sim.risk_per_trade == 0.02

    def test_simulate_trade_win(self) -> None:
        sim = self._make_sim(initial_aum=100_000, risk_per_trade=0.01)
        # Win with RPUR=2 -> risk 1000, gain 2000
        result = sim.simulate_trade(100_000, is_win=True, return_per_unit_risk=2.0)
        assert result == pytest.approx(102_000.0)

    def test_simulate_trade_loss(self) -> None:
        sim = self._make_sim(initial_aum=100_000, risk_per_trade=0.01)
        # Loss -> lose 1% of 100k = 1000
        result = sim.simulate_trade(100_000, is_win=False, return_per_unit_risk=2.0)
        assert result == pytest.approx(99_000.0)

    def test_simulate_trade_zero_risk(self) -> None:
        sim = self._make_sim(risk_per_trade=0.0)
        result = sim.simulate_trade(100_000, is_win=False, return_per_unit_risk=3.0)
        assert result == pytest.approx(100_000.0)

    def test_simulate_year_returns_correct_count(self) -> None:
        sim = self._make_sim()
        results = sim.simulate_year(return_per_unit_risk=2.0, num_simulations=50)
        assert len(results) == 50

    def test_simulate_year_all_results_positive(self) -> None:
        sim = self._make_sim(risk_per_trade=0.001)
        results = sim.simulate_year(return_per_unit_risk=2.0, num_simulations=100)
        assert all(r > 0 for r in results)

    def test_simulate_year_100pct_win_rate(self) -> None:
        """With 100% win rate and RPUR=1, every trade gains risk_per_trade."""
        sim = self._make_sim(
            initial_aum=100_000, win_rate=1.0,
            trades_per_year=10, risk_per_trade=0.01,
        )
        results = sim.simulate_year(return_per_unit_risk=1.0, num_simulations=5)
        # All simulations should produce the same result (compound growth)
        assert all(r > 100_000 for r in results)
        # With 100% win rate, all results should be identical
        assert len(set(round(r, 2) for r in results)) == 1

    def test_simulate_year_0pct_win_rate(self) -> None:
        """With 0% win rate, every trade loses risk_per_trade of current AUM."""
        sim = self._make_sim(
            initial_aum=100_000, win_rate=0.0,
            trades_per_year=10, risk_per_trade=0.01,
        )
        results = sim.simulate_year(return_per_unit_risk=1.0, num_simulations=5)
        # All simulations should produce the same result (compound decay)
        expected = 100_000 * (0.99 ** 10)
        for r in results:
            assert r == pytest.approx(expected, rel=1e-6)

    def test_simulate_year_statistical_mean(self) -> None:
        """With many simulations, mean return should be close to the expected value."""
        np.random.seed(42)
        sim = self._make_sim(
            initial_aum=100_000, win_rate=0.5,
            trades_per_year=20, risk_per_trade=0.01,
        )
        results = sim.simulate_year(return_per_unit_risk=3.0, num_simulations=5_000)
        mean_aum = np.mean(results)
        # With 50% WR and 3:1 RPUR, expected per-trade gain = 0.5*3*1% - 0.5*1% = 1%
        # Over 20 trades this compounds to roughly 100k * 1.01^20 ≈ 122k
        # Allow generous bounds since it's stochastic
        assert 110_000 < mean_aum < 135_000


# ---------------------------------------------------------------------------
# simulate_drawdown
# ---------------------------------------------------------------------------

class TestSimulateDrawdown:
    """Tests for the simulate_drawdown function."""

    def test_returns_float(self) -> None:
        result = simulate_drawdown(50.0, 20, 1.0, simulations=100)
        assert isinstance(result, float)

    def test_non_negative(self) -> None:
        result = simulate_drawdown(50.0, 20, 1.0, simulations=100)
        assert result >= 0.0

    def test_100pct_win_rate_zero_drawdown(self) -> None:
        """With 100% win rate there are never consecutive losses."""
        result = simulate_drawdown(100.0, 20, 1.0, simulations=100)
        assert result == 0.0

    def test_0pct_win_rate_max_drawdown(self) -> None:
        """With 0% win rate, every trade is a loss -> drawdown = trades * risk."""
        result = simulate_drawdown(0.0, 20, 2.0, simulations=100)
        assert result == pytest.approx(40.0)  # 20 * 2.0

    def test_drawdown_scales_with_risk(self) -> None:
        """Higher risk per trade should yield higher drawdown on average."""
        np.random.seed(42)
        dd_low = simulate_drawdown(50.0, 30, 0.5, simulations=1_000)
        np.random.seed(42)
        dd_high = simulate_drawdown(50.0, 30, 2.0, simulations=1_000)
        assert dd_high > dd_low

    def test_drawdown_scales_with_trades(self) -> None:
        """More trades increases the chance of longer losing streaks."""
        np.random.seed(42)
        dd_few = simulate_drawdown(50.0, 10, 1.0, simulations=2_000)
        np.random.seed(42)
        dd_many = simulate_drawdown(50.0, 100, 1.0, simulations=2_000)
        assert dd_many >= dd_few
