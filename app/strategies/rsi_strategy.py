"""
RSI trading strategy.
"""

from __future__ import annotations

import pandas as pd

from app.strategies.base import Strategy


class RSIStrategy(Strategy):
    """
    Trading strategy based on RSI overbought/oversold levels.
    """

    def __init__(
        self,
        period: int = 14,
        oversold: float = 30,
        overbought: float = 70,
    ) -> None:
        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def generate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate buy/sell signals using RSI.
        """

        result = data.copy()

        rsi_column = f"RSI{self.period}"

        if rsi_column not in result.columns:
            raise ValueError(f"Missing column: {rsi_column}")

        result["Signal"] = 0

        buy_signal = (
            (result[rsi_column] > self.oversold)
            & (result[rsi_column].shift(1) <= self.oversold)
        )

        sell_signal = (
            (result[rsi_column] < self.overbought)
            & (result[rsi_column].shift(1) >= self.overbought)
        )

        result.loc[buy_signal, "Signal"] = 1
        result.loc[sell_signal, "Signal"] = -1

        return result