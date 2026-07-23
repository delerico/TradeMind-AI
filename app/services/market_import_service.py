from __future__ import annotations

from app.collector.market_collector import MarketCollector
from app.database.market_repository import MarketDataRepository
from app.database.models import MarketData


class MarketImportService:
    """
    Service responsible for importing market data into the database.
    """

    def __init__(
        self,
        collector: MarketCollector,
        repository: MarketDataRepository,
    ) -> None:
        self._collector = collector
        self._repository = repository

    def import_symbol(self, symbol: str, period: str = "1mo") -> int:
        """
        Download market data and import only new records.

        Returns:
            Number of imported records.
        """

        data = self._collector.get_stock(symbol, period)
        existing_dates = self._repository.get_existing_dates(symbol)

        records: list[MarketData] = []

        for date, row in data.iterrows():

            date = date.to_pydatetime()

            if date in existing_dates:
                continue

            records.append(
                MarketData(
                    symbol=symbol.upper(),
                    date=date,
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=int(row["Volume"]),
                )
            )

        self._repository.save_all(records)

        return len(records)