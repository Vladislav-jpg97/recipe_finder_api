from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from backend.core.security import hash_password, verify_password, create_access_token, create_refresh_token, \
    decode_token
from backend.core.cache import CacheService
from backend.core.config import settings
from backend.dependencies.auth import UserRepoDep
from backend.models import User
from backend.repository.user_repo import UserRepository
from backend.schemas.auth import TokenResponse
from backend.schemas.user import UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class UserService:
    def __init__(
            self,
            session: AsyncSession,
            user_repo: UserRepository,
            cache_service: CacheService
    ):
        self.session = session
        self.user_repo = user_repo
        self.cache_service = cache_service

    async def register(self, data: UserCreate) -> User:
        existing_email = await self.user_repo.get_by_email(data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        existing_name = await self.user_repo.get_by_username(data.username)
        if existing_name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this username already exists"
            )

        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hash_password(data.password),
        )
        await self.user_repo.create(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def authenticate(self, email: str, password: str) -> TokenResponse:
        user = await self.user_repo.get_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=401,
                detail="Inactive user"
            )

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        redis_key = f"refresh:{refresh_token}"
        expire_seconds = settings.refresh_token_expire_days * 86400
        await self.cache_service.set(redis_key, str(user.id), ttl=expire_seconds)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        redis_key = f"refresh:{refresh_token}"

        # 1. Проверяем наличие в Redis
        user_id = await self.cache_service.get(redis_key)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        # 2. Проверяем JWT payload
        payload_user_id = decode_token(refresh_token, expected_type="refresh")
        if str(payload_user_id) != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        # 3. Ротация: удаляем старый токен из Redis
        await self.cache_service.delete(redis_key)

        # 4. Генерируем новую пару
        new_access_token = create_access_token(int(user_id))
        new_refresh_token = create_refresh_token(int(user_id))

        # 5. Сохраняем новый refresh_token в Redis
        new_redis_key = f"refresh:{new_refresh_token}"
        expire_seconds = settings.refresh_token_expire_days * 86400
        await self.cache_service.set(new_redis_key, str(user_id), ttl=expire_seconds)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )

    async def logout(self, refresh_token: str) -> dict:
        redis_key = f"refresh:{refresh_token}"
        await self.cache_service.delete(redis_key)
        return {"message": "Logged out"}

    @staticmethod
    async def get_current_user(
            user_repo: UserRepoDep,
            token: str = Depends(oauth2_scheme),
    ) -> User:
        user_id = decode_token(token, expected_type="access")
        user = await user_repo.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        return user