from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class InvestmentBase(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    full_amount: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint('full_amount > 0'),
        nullable=False,
    )
    invested_amount: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    fully_invested: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )
    close_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )