from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationFullInfoDB,
)
from app.services.investment import invest


router = APIRouter(
    prefix='/donation',
    tags=['Пожертвования'],
)

SessionDep = Annotated[
    AsyncSession,
    Depends(get_async_session),
]
CurrentUser = Annotated[
    User,
    Depends(current_user),
]
SuperUser = Annotated[
    User,
    Depends(current_superuser),
]


@router.get(
    '/',
    response_model=list[DonationFullInfoDB],
    summary='Получить все пожертвования',
)
async def get_all_donations(
    session: SessionDep,
    _: SuperUser,
):
    """Возвращает полный список пожертвований суперпользователю."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    summary='Получить свои пожертвования',
)
async def get_my_donations(
    session: SessionDep,
    user: CurrentUser,
):
    """Возвращает пожертвования текущего пользователя."""
    return await donation_crud.get_by_user(user, session)


@router.post(
    '/',
    response_model=DonationDB,
    summary='Создать пожертвование',
)
async def create_donation(
    donation: DonationCreate,
    session: SessionDep,
    user: CurrentUser,
):
    """Создаёт пожертвование и распределяет его по проектам."""
    db_donation = await donation_crud.create_with_user(
        donation,
        session,
        user,
    )

    open_projects = await charity_project_crud.get_open_projects(
        session
    )

    return await invest(
        db_donation,
        open_projects,
        session,
    )