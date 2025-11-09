from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


class Container(Base):
    __tablename__ = "container"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String())
    cpu_usage: Mapped[int] = mapped_column(Integer())
    memory_usage: Mapped[int] = mapped_column(Integer())
    ip_addresses: Mapped[list[str]] = mapped_column(ARRAY(String))
