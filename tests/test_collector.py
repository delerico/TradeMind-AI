"""Tests for app.collector.market_collector.MarketCollector."""

import pandas as pd

from app.collector.market_collector import MarketCollector


def test_get_stock_returns_dataframe_with_ohlcv_columns() -> None:
    collector = MarketCollector()

    data = collector.get_stock("AAPL", period="1mo")

    assert isinstance(data, pd.DataFrame)
    assert not data.empty

    for column in ("Open", "High", "Low", "Close", "Volume"):
        assert column in data.columns