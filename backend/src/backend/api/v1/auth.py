from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from backend.dependencies.auth import UserServiceDep
from backend.models import User
from backend.repository.user_repo import UserRepository
from backend.schemas.auth import TokenResponse, LoginRequest
from backend.schemas.user import UserResponse, UserCreate
from backend.services.user_service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя"
)
async def register(
        data: UserCreate,
        service: UserServiceDep
):
    return await service.register(data)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Вход"
)
async def login(
        service: UserServiceDep,
        form_data: OAuth2PasswordRequestForm = Depends(),

):
    return await service.authenticate(form_data.username, form_data.password)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновление токенов"
)
async def refresh_tokens(
        token: str,
        service: UserServiceDep
):
    return await service.refresh(token)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Профиль текущего пользователя"
)
async def me(
        current_user: User = Depends(UserService.get_current_user)
):
    return current_user