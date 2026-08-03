from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status
from starlette.exceptions import HTTPException

from backend.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def _create_token(user_id, expires_delta: timedelta, token_type: str) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": token_type
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(user_id: int) -> str:
    expire_delta = timedelta(minutes=getattr(settings, "access_token_expire_minutes", 15))
    return _create_token(
        user_id,
        expire_delta,
        token_type="access"
    )


def create_refresh_token(user_id: int) -> str:
    return _create_token(
        user_id,
        timedelta(days=settings.refresh_token_expire_days),
        token_type="refresh"
    )

def decode_token(token: str, expected_type: str = "access") -> int:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if payload.get("type") != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return int(payload["sub"])
