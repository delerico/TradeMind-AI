"""
MACD trading strategy.
"""

from __future__ import annotations

import pandas as pd

from app.strategies.base import Strategy


class MACDStrategy(Strategy):
    """
    Trading strategy based on MACD crossovers.
    """

    def generate(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Generate buy/sell signals using MACD.
        """

        result = data.copy()

        required_columns = ["MACD", "MACD_SIGNAL"]

        for column in required_columns:
            if column not in result.columns:
                raise ValueError(f"Missing column: {column}")

        result["Signal"] = 0

        buy_signal = (
            (result["MACD"] > result["MACD_SIGNAL"])
            & (result["MACD"].shift(1) <= result["MACD_SIGNAL"].shift(1))
        )

        sell_signal = (
            (result["MACD"] < result["MACD_SIGNAL"])
            & (result["MACD"].shift(1) >= result["MACD_SIGNAL"].shift(1))
        )

        result.loc[buy_signal, "Signal"] = 1
        result.loc[sell_signal, "Signal"] = -1

        return result