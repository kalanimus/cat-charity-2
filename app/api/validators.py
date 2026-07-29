from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден.',
        )

    return project


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
    project_id: Optional[int] = None,
) -> None:
    project = await charity_project_crud.get_by_name(
        project_name,
        session,
    )

    if project is not None and project.id != project_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует.',
        )


def check_project_before_edit(
    project: CharityProject,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать.',
        )


def check_project_before_delete(
    project: CharityProject,
) -> None:
    if project.fully_invested or project.invested_amount > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Нельзя удалить проект, в который внесены средства.',
        )


def check_new_full_amount(
    project: CharityProject,
    new_full_amount: int,
) -> None:
    if new_full_amount < project.invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                'Требуемая сумма не может быть меньше '
                'уже инвестированной.'
            ),
        )