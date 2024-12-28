from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    modified_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))


db_url = "sqlite+aiosqlite:///db.sqlite"
engine = create_async_engine(db_url, echo=True)
SessionAsync = async_sessionmaker(engine, expire_on_commit=False)

