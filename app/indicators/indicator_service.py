"""
Indicator service.

Provides a high-level interface for enriching market data with
technical indicators.
"""

from __future__ import annotations

from collections.abc import Callable

import pandas as pd

from app.indicators.momentum import roc, rsi
from app.indicators.moving_averages import ema, sma, wma
from app.indicators.trend import (
    macd,
    macd_histogram,
    macd_signal,
)

IndicatorFunction = Callable[..., pd.Series]


class IndicatorService:
    """
    Service responsible for enriching market data
    with technical indicators.
    """

    @staticmethod
    def add_indicator(
        data: pd.DataFrame,
        name: str,
        indicator: IndicatorFunction,
        *args,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Return a copy of the DataFrame with one indicator added.
        """

        result = data.copy()
        result[name] = indicator(result, *args, **kwargs)

        return result

    def add_basic_indicators(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Add the default indicator set.
        """

        result = data.copy()

        indicators = [
            # Moving averages
            ("SMA20", sma, 20),
            ("SMA50", sma, 50),
            ("EMA20", ema, 20),
            ("EMA50", ema, 50),
            ("WMA20", wma, 20),

            # Momentum
            ("RSI14", rsi, 14),
            ("ROC12", roc, 12),

            # Trend
            ("MACD", macd),
            ("MACD_SIGNAL", macd_signal),
            ("MACD_HIST", macd_histogram),
        ]

        for indicator in indicators:
            name = indicator[0]
            function = indicator[1]
            args = indicator[2:]

            result[name] = function(result, *args)

        return result