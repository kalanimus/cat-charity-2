from fastapi import APIRouter

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead

from app.api.endpoints.donation import router as donation_router
from app.api.endpoints.charity_project import (
    router as charity_project_router,
)


main_router = APIRouter()

main_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['Авторизация'],
)

main_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Авторизация'],
)

main_router.include_router(donation_router)
main_router.include_router(charity_project_router)