from datetime import datetime
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import InvestmentBase


def close_investment_object(
    obj: InvestmentBase,
) -> None:
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def invest(
    target: InvestmentBase,
    sources: Sequence[InvestmentBase],
    session: AsyncSession,
) -> InvestmentBase:
    for source in sources:
        target_free_amount = (
            target.full_amount - target.invested_amount
        )
        source_free_amount = (
            source.full_amount - source.invested_amount
        )

        invested_amount = min(
            target_free_amount,
            source_free_amount,
        )

        target.invested_amount += invested_amount
        source.invested_amount += invested_amount

        if source.invested_amount == source.full_amount:
            close_investment_object(source)

        if target.invested_amount == target.full_amount:
            close_investment_object(target)
            break

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    await session.refresh(target)
    return target