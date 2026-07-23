"""
Moving average indicators.

This module provides pure functions for calculating moving averages.
Each function returns a pandas Series and never modifies the input
DataFrame.
"""

from __future__ import annotations

import pandas as pd


def sma(
    data: pd.DataFrame,
    period: int,
    column: str = "Close",
) -> pd.Series:
    """
    Calculate the Simple Moving Average (SMA).

    Args:
        data: DataFrame containing market data.
        period: Rolling window size.
        column: Column on which to calculate the SMA.

    Returns:
        A pandas Series containing the SMA values.
    """
    return data[column].rolling(window=period).mean()


def ema(
    data: pd.DataFrame,
    period: int,
    column: str = "Close",
) -> pd.Series:
    """
    Calculate the Exponential Moving Average (EMA).

    Args:
        data: DataFrame containing market data.
        period: EMA period.
        column: Column on which to calculate the EMA.

    Returns:
        A pandas Series containing the EMA values.
    """
    return data[column].ewm(
        span=period,
        adjust=False,
    ).mean()


def wma(
    data: pd.DataFrame,
    period: int,
    column: str = "Close",
) -> pd.Series:
    """
    Calculate the Weighted Moving Average (WMA).

    Args:
        data: DataFrame containing market data.
        period: Rolling window size.
        column: Column on which to calculate the WMA.

    Returns:
        A pandas Series containing the WMA values.
    """
    weights = pd.Series(range(1, period + 1), dtype=float)

    return data[column].rolling(period).apply(
        lambda values: (values * weights).sum() / weights.sum(),
        raw=True,
    )