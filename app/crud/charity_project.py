from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)


class CRUDCharityProject(
    CRUDBase[
        CharityProject,
        CharityProjectCreate,
        CharityProjectUpdate,
    ]
):
    async def get_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[CharityProject]:
        db_project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )
        return db_project.scalars().first()

    async def get_open_projects(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        db_projects = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
            .order_by(
                CharityProject.create_date,
                CharityProject.id,
            )
        )
        return list(db_projects.scalars().all())


charity_project_crud = CRUDCharityProject(CharityProject)