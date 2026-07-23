"""
Moving Average Cross strategy.
"""

from __future__ import annotations

import pandas as pd

from app.strategies.base import Strategy


class MovingAverageCrossStrategy(Strategy):
    """
    Trading strategy based on moving average crossovers.
    """

    def __init__(
        self,
        fast_period: int = 20,
        slow_period: int = 50,
    ) -> None:
        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate buy/sell signals.

        Returns:
            DataFrame enriched with a Signal column.
        """

        result = data.copy()

        fast_ma = f"SMA{self.fast_period}"
        slow_ma = f"SMA{self.slow_period}"

        if fast_ma not in result.columns:
            raise ValueError(f"Missing column: {fast_ma}")

        if slow_ma not in result.columns:
            raise ValueError(f"Missing column: {slow_ma}")

        result["Signal"] = 0

        buy_signal = (
            (result[fast_ma] > result[slow_ma])
            & (result[fast_ma].shift(1) <= result[slow_ma].shift(1))
        )

        sell_signal = (
            (result[fast_ma] < result[slow_ma])
            & (result[fast_ma].shift(1) >= result[slow_ma].shift(1))
        )

        result.loc[buy_signal, "Signal"] = 1
        result.loc[sell_signal, "Signal"] = -1

        return result