"""
Backtest results.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.backtest.trade import Trade


@dataclass(slots=True)
class BacktestResult:
    """
    Stores the outcome of a backtest.
    """

    initial_capital: float
    final_capital: float

    trades: list[Trade] = field(default_factory=list)

    @property
    def total_return(self) -> float:
        return (
            (self.final_capital - self.initial_capital)
            / self.initial_capital
        ) * 100

    @property
    def total_trades(self) -> int:
        return len(self.trades)

    @property
    def winning_trades(self) -> int:
        return sum(
            trade.profit > 0
            for trade in self.trades
        )

    @property
    def losing_trades(self) -> int:
        return sum(
            trade.profit < 0
            for trade in self.trades
        )

    @property
    def win_rate(self) -> float:
        if not self.trades:
            return 0.0

        return (
            self.winning_trades
            / self.total_trades
        ) * 100