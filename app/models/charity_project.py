from sqlalchemy import CheckConstraint, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import InvestmentBase


class CharityProject(InvestmentBase):
    __tablename__ = 'charityproject'

    name: Mapped[str] = mapped_column(
        String(100),
        CheckConstraint('length(name) BETWEEN 5 AND 100'),
        unique=True,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        CheckConstraint('length(description) >= 10'),
        nullable=False,
    )