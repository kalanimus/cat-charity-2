from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate


class CRUDDonation(
    CRUDBase[
        Donation,
        DonationCreate,
        DonationCreate,
    ]
):
    async def create_with_user(
        self,
        obj_in: DonationCreate,
        session: AsyncSession,
        user: User,
    ) -> Donation:
        obj_in_data = obj_in.model_dump()
        obj_in_data['user_id'] = user.id

        db_donation = Donation(**obj_in_data)
        session.add(db_donation)
        await session.flush()
        return db_donation

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ) -> list[Donation]:
        db_donations = await session.execute(
            select(Donation)
            .where(Donation.user_id == user.id)
            .order_by(
                Donation.create_date,
                Donation.id,
            )
        )
        return list(db_donations.scalars().all())

    async def get_uninvested_donations(
        self,
        session: AsyncSession,
    ) -> list[Donation]:
        db_donations = await session.execute(
            select(Donation)
            .where(Donation.fully_invested.is_(False))
            .order_by(
                Donation.create_date,
                Donation.id,
            )
        )
        return list(db_donations.scalars().all())


donation_crud = CRUDDonation(Donation)