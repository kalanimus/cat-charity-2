from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate,
    check_new_full_amount,
    check_project_before_delete,
    check_project_before_edit,
    check_project_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import (
    close_investment_object,
    invest,
)


router = APIRouter(
    prefix='/charity_project',
    tags=['Проекты'],
)

SessionDep = Annotated[
    AsyncSession,
    Depends(get_async_session),
]
SuperUser = Annotated[
    User,
    Depends(current_superuser),
]


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    summary='Получить все проекты',
)
async def get_all_projects(
    session: SessionDep,
):
    """Возвращает список всех благотворительных проектов."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    summary='Создать проект',
)
async def create_project(
    project: CharityProjectCreate,
    session: SessionDep,
    _: SuperUser,
):
    """Создаёт проект и инвестирует свободные пожертвования."""
    await check_name_duplicate(project.name, session)

    db_project = await charity_project_crud.create(
        project,
        session,
    )

    donations = await donation_crud.get_uninvested_donations(
        session
    )

    return await invest(
        db_project,
        donations,
        session,
    )


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Изменить проект',
)
async def update_project(
    project_id: int,
    project: CharityProjectUpdate,
    session: SessionDep,
    _: SuperUser,
):
    """Изменяет существующий открытый проект."""
    db_project = await check_project_exists(
        project_id,
        session,
    )
    check_project_before_edit(db_project)

    if project.name is not None:
        await check_name_duplicate(
            project.name,
            session,
            project_id,
        )

    if project.full_amount is not None:
        check_new_full_amount(
            db_project,
            project.full_amount,
        )

    db_project = await charity_project_crud.update(
        db_project,
        project,
        session,
    )

    if db_project.full_amount == db_project.invested_amount:
        close_investment_object(db_project)

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    await session.refresh(db_project)
    return db_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    summary='Удалить проект',
)
async def delete_project(
    project_id: int,
    session: SessionDep,
    _: SuperUser,
):
    """Удаляет проект, в который ещё не вложены средства."""
    db_project = await check_project_exists(
        project_id,
        session,
    )
    check_project_before_delete(db_project)

    db_project = await charity_project_crud.remove(
        db_project,
        session,
    )

    try:
        await session.commit()
    except Exception:
        await session.rollback()
        raise

    return db_project