"""
Trend indicators.

This module contains pure functions that calculate
trend-based technical indicators.
"""

from __future__ import annotations

import pandas as pd


def macd(
    data: pd.DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
    column: str = "Close",
) -> pd.Series:
    """
    Calculate the MACD line.
    """

    fast_ema = data[column].ewm(
        span=fast_period,
        adjust=False,
    ).mean()

    slow_ema = data[column].ewm(
        span=slow_period,
        adjust=False,
    ).mean()

    return fast_ema - slow_ema


def macd_signal(
    data: pd.DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
    column: str = "Close",
) -> pd.Series:
    """
    Calculate the MACD signal line.
    """

    macd_line = macd(
        data=data,
        fast_period=fast_period,
        slow_period=slow_period,
        column=column,
    )

    return macd_line.ewm(
        span=signal_period,
        adjust=False,
    ).mean()


def macd_histogram(
    data: pd.DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
    column: str = "Close",
) -> pd.Series:
    """
    Calculate the MACD histogram.
    """

    macd_line = macd(
        data=data,
        fast_period=fast_period,
        slow_period=slow_period,
        column=column,
    )

    signal_line = macd_line.ewm(
        span=signal_period,
        adjust=False,
    ).mean()

    return macd_line - signal_line