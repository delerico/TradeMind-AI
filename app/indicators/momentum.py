"""
Momentum indicators.

This module contains pure functions that calculate
momentum-based technical indicators.
"""

from __future__ import annotations

import pandas as pd


def rsi(
    data: pd.DataFrame,
    period: int = 14,
    column: str = "Close",
) -> pd.Series:
    """
    Calculate the Relative Strength Index (RSI).
    """

    delta = data[column].diff()

    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    average_gain = gains.rolling(period).mean()
    average_loss = losses.rolling(period).mean()

    rs = average_gain / average_loss

    return 100 - (100 / (1 + rs))


def roc(
    data: pd.DataFrame,
    period: int = 12,
    column: str = "Close",
) -> pd.Series:
    """
    Calculate the Rate of Change (ROC).
    """

    return data[column].pct_change(periods=period) * 100