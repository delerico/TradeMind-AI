"""
Database engine and session management.

Defines the SQLAlchemy engine, session factory, and declarative base
used throughout the application.
"""

from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------

PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

_DB_DIR: Path = PROJECT_ROOT / "data"
_DB_DIR.mkdir(parents=True, exist_ok=True)

_DB_PATH: Path = _DB_DIR / "trademind.db"

SQLALCHEMY_DATABASE_URL: str = f"sqlite:///{_DB_PATH}"

# ---------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------

engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# ---------------------------------------------------------------------
# Session factory
# ---------------------------------------------------------------------

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# ---------------------------------------------------------------------
# Declarative base
# ---------------------------------------------------------------------

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Yield a SQLAlchemy session.

    Yields:
        Session: Active database session.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()