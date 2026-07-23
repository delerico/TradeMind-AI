from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Integer, Numeric, String, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class MarketData(Base):
    """
    Represents a single OHLCV market data record.
    """

    __tablename__ = "market_data"

    __table_args__ = (
        UniqueConstraint("symbol", "date", name="uq_symbol_date"),
        Index("ix_symbol_date", "symbol", "date"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    symbol: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    open: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    high: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    low: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    close: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    volume: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"MarketData("
            f"symbol='{self.symbol}', "
            f"date='{self.date}', "
            f"close={self.close})"
        )