from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from backend.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from backend.models import User
from backend.repository.user_repo import UserRepository
from backend.schemas.auth import TokenResponse
from backend.schemas.user import UserCreate


class UserService:
    def __init__(self, session: AsyncSession, user_repo: UserRepository):
        self.session = session
        self.user_repo = user_repo

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
            password=hash_password(data.password),
        )
        await self.user_repo.create(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


    async def authenticate(self,email: str, password: str):
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

        return TokenResponse(access_token=access_token, refresh_token=refresh_token,token_type="argon2")

