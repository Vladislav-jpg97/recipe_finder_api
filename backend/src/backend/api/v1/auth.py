from fastapi import APIRouter
from sqlalchemy.util import await_fallback
from starlette import status

from backend.dependencies.auth import UserServiceDep
from backend.repository.user_repo import UserRepository
from backend.schemas.auth import TokenResponse, LoginRequest, RefreshRequest
from backend.schemas.user import UserResponse, UserCreate

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
        data: LoginRequest,
        service: UserServiceDep
):
    return await service.authenticate(data.email, data.password)


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
    summary=""
)
async def me(
        user_repo: UserRepository,
        service: UserServiceDep,
        token: str
):
    return await service.get_current_user(user_repo, token)
