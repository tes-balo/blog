from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestFormStrict

from app.core.config import settings
from app.core.security import authenticate_user, create_access_token
from app.db.fake_db import fake_users_db
from app.schemas.auth import TokenResponse
from app.schemas.fake_schemas import UserInDB

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_router = router


@router.post("/sign-in")
async def sign_in(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
) -> dict[str, Any]:
    result = await authenticate_user(
        fake_users_db, form_data.username, form_data.password
    )
    if not result or not isinstance(result, UserInDB):
        raise HTTPException(
            status_code=404,
        )
    token = create_access_token(
        result.model_dump(),
        expires_delta=timedelta(settings.jwt_expiration_seconds),
    )
    # print(result, "dump")

    token_data = TokenResponse(
        access_token=token, expires_in=settings.jwt_expiration_seconds
    )
    return token_data.model_dump()


# @router.get("/users")
# async def get_post(current_user = Depends(get_current_user))
