"""
Backtesting engine.
"""

from __future__ import annotations

import pandas as pd

from app.backtest.results import BacktestResult
from app.backtest.trade import Trade
from app.strategies.base import Strategy


class BacktestEngine:
    """
    Simple long-only backtesting engine.
    """

    def __init__(
        self,
        initial_capital: float = 10_000,
    ) -> None:

        self.initial_capital = initial_capital

    def run(
        self,
        strategy: Strategy,
        data: pd.DataFrame,
        symbol: str,
    ) -> BacktestResult:
        """
        Execute a strategy over historical data.
        """

        df = strategy.generate(data)

        capital = self.initial_capital

        trades: list[Trade] = []

        in_position = False

        entry_price = 0.0
        entry_date = None

        quantity = 0.0

        for index, row in df.iterrows():

            signal = row["Signal"]

            price = row["Close"]

            if signal == 1 and not in_position:

                quantity = capital / price

                entry_price = price
                entry_date = index

                in_position = True

            elif signal == -1 and in_position:

                exit_price = price
                exit_date = index

                profit = (exit_price - entry_price) * quantity

                return_pct = (
                    (exit_price - entry_price)
                    / entry_price
                ) * 100

                capital += profit

                trades.append(
                    Trade(
                        symbol=symbol,
                        entry_date=entry_date,
                        exit_date=exit_date,
                        entry_price=entry_price,
                        exit_price=exit_price,
                        quantity=quantity,
                        profit=profit,
                        return_pct=return_pct,
                    )
                )

                in_position = False

        return BacktestResult(
            initial_capital=self.initial_capital,
            final_capital=capital,
            trades=trades,
        )