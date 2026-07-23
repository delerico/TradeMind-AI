"""
Repository for MarketData persistence.

Encapsulates all database access for MarketData entities.
"""

from __future__ import annotations

import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.models import MarketData

logger = logging.getLogger(__name__)


class MarketDataRepository:
    """
    Repository responsible for MarketData persistence.
    """

    def __init__(self, session: Session) -> None:
        """
        Initialize the repository.

        Args:
            session: Active SQLAlchemy session.
        """
        self._session = session

    def save(self, record: MarketData) -> None:
        """
        Save a single MarketData record.
        """
        try:
            self._session.add(record)
            self._session.flush()
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            logger.exception("Failed to save MarketData record.")
            raise

    def save_all(self, records: list[MarketData]) -> None:
        """
        Save multiple MarketData records in a single transaction.
        """
        if not records:
            return

        try:
            self._session.add_all(records)
            self._session.flush()
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            logger.exception(
                "Failed to save %d MarketData records.",
                len(records),
            )
            raise

    def get_by_symbol(self, symbol: str) -> list[MarketData]:
        """
        Return all records for a symbol ordered by date.
        """
        symbol = symbol.strip().upper()

        statement = (
            select(MarketData)
            .where(MarketData.symbol == symbol)
            .order_by(MarketData.date.asc())
        )

        return list(self._session.execute(statement).scalars().all())

    def get_existing_dates(self, symbol: str) -> set[datetime]:
        """
        Return all existing dates for a symbol.
        """
        symbol = symbol.strip().upper()

        statement = select(MarketData.date).where(
            MarketData.symbol == symbol
        )

        return set(self._session.execute(statement).scalars().all())

    def exists(self, symbol: str, date: datetime) -> bool:
        """
        Check whether a record already exists.
        """
        symbol = symbol.strip().upper()

        statement = select(MarketData.id).where(
            MarketData.symbol == symbol,
            MarketData.date == date,
        )

        return self._session.execute(statement).first() is not None

    def get_latest(self, symbol: str) -> MarketData | None:
        """
        Return the most recent MarketData record for a symbol.
        """
        symbol = symbol.strip().upper()

        statement = (
            select(MarketData)
            .where(MarketData.symbol == symbol)
            .order_by(MarketData.date.desc())
            .limit(1)
        )

        return self._session.execute(statement).scalar_one_or_none()

    def delete(self, record: MarketData) -> None:
        """
        Delete a MarketData record.
        """
        try:
            self._session.delete(record)
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            logger.exception("Failed to delete MarketData record.")
            raise