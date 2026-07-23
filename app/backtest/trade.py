"""
Trade model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Trade:
    """
    Represents a completed trade.
    """

    symbol: str

    entry_date: datetime
    exit_date: datetime

    entry_price: float
    exit_price: float

    quantity: float

    profit: float
    return_pct: float