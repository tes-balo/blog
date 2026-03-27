# # password hashing (hash/verify)

# token creation (access + refresh)

# token decoding


from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash

from app.api.dependencies import get_user
from app.core.config import settings
from app.schemas.fake_schemas import UserInDB


async def fake_hash_password(password: str) -> str:
    return f"fakehashed{password}"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

password_hash = PasswordHash.recommended()

DUMMY_HASH: str = password_hash.hash("dummypasword")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


async def authenticate_user(
    fake_db: dict[str, Any], username: str, password: str
) -> UserInDB | bool:
    user = await get_user(fake_db, username)
    print(user)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False

    if not verify_password(password, user.hashed_password):
        print("false")
        return False
    return user


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode: dict[str, Any] = data.copy()

    expire = datetime.now(UTC) + (
        expires_delta or timedelta(seconds=float(settings.jwt_expiration_seconds))
    )
    # print(to_encode)
    # breakpoint()
    to_encode.update({"sub": str(data["id"]), "exp": int(expire.timestamp())})

    return jwt.encode(
        payload=to_encode,
        key=settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
