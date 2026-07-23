"""
Market data collection module.

Defines MarketCollector, responsible solely for retrieving OHLCV
(Open, High, Low, Close, Volume) market data for a given ticker symbol.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)


class MarketDataError(Exception):
    """Raised when market data cannot be retrieved or is invalid."""


class MarketCollector:
    """
    Collects OHLCV market data for a ticker symbol.

    Single Responsibility: this class only retrieves and validates
    OHLCV data. It does not store, transform, or analyze it - those
    concerns belong to other modules (database, indicators, ai).

    The underlying data client is injected rather than imported
    directly inside methods, so the data source can be swapped
    (e.g. for unit testing, or a future non-yfinance provider) without
    modifying this class - Dependency Inversion Principle.
    """

    _REQUIRED_COLUMNS: tuple[str, ...] = (
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    )

    def __init__(self, yfinance_module: Any = yf) -> None:
        """
        Args:
            yfinance_module: module or object exposing a `Ticker(symbol)`
                interface compatible with yfinance.
        """
        self._yf = yfinance_module

    def get_stock(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """
        Retrieve OHLCV market data for a stock symbol.

        Args:
            symbol: Ticker symbol, e.g. "AAPL".
            period: yfinance-compatible period.

        Returns:
            pandas.DataFrame indexed by date containing
            Open, High, Low, Close and Volume.
        """

        self._validate_inputs(symbol, period)
        normalized_symbol = symbol.strip().upper()

        raw_data = self._fetch_raw_data(normalized_symbol, period)
        self._validate_data(raw_data, normalized_symbol, period)

        # Keep only OHLCV columns
        data = raw_data.loc[:, self._REQUIRED_COLUMNS].copy()

        # Remove timezone from DatetimeIndex
        if isinstance(data.index, pd.DatetimeIndex) and data.index.tz is not None:
            data.index = data.index.tz_localize(None)

        return data

    def _fetch_raw_data(self, symbol: str, period: str) -> pd.DataFrame:
        """Call the underlying data client and translate failures."""
        try:
            ticker = self._yf.Ticker(symbol)
            data = ticker.history(period=period)
        except Exception as exc:
            logger.error("Failed to fetch data for %s: %s", symbol, exc)
            raise MarketDataError(
                f"Failed to fetch data for symbol '{symbol}': {exc}"
            ) from exc

        return data

    def _validate_data(self, data: pd.DataFrame, symbol: str, period: str) -> None:
        """Ensure the returned data is usable OHLCV data."""

        if data is None or data.empty:
            raise MarketDataError(
                f"No data returned for symbol '{symbol}' with period '{period}'."
            )

        missing = [
            column
            for column in self._REQUIRED_COLUMNS
            if column not in data.columns
        ]

        if missing:
            raise MarketDataError(
                f"Data for '{symbol}' is missing required column(s): {missing}"
            )

    @staticmethod
    def _validate_inputs(symbol: str, period: str) -> None:
        """Validate raw inputs before making any external call."""

        if not symbol or not symbol.strip():
            raise ValueError("symbol must be a non-empty string")

        if not period or not period.strip():
            raise ValueError("period must be a non-empty string")