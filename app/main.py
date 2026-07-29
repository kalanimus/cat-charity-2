from fastapi import FastAPI

from app.api.router import main_router
from app.core.config import settings


tags_metadata = [
    {
        'name': 'Авторизация',
        'description': (
            'Регистрация пользователей, получение и удаление JWT.'
        ),
    },
    {
        'name': 'Проекты',
        'description': (
            'Просмотр и управление благотворительными проектами.'
        ),
    },
    {
        'name': 'Пожертвования',
        'description': (
            'Создание и просмотр пожертвований.'
        ),
    },
]

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    openapi_tags=tags_metadata,
)

app.include_router(main_router)