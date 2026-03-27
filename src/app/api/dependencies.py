# get_current_user,
# get_current_active_user,
# get_admin_user,
# get_verified_user,
# from db.py import get_db

# get_post_or_404
# get_user_404
# verify post owner
# get_pagination params
# can_edit_user
# require_roles["admin, "moderator]

# rate-limiting hooks


from typing import Any

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.schemas.fake_schemas import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_user(db: dict[str, Any], username: str) -> UserInDB:
    if username not in db:
        print(username, "get_user")
        raise HTTPException(status_code=404, detail="user not found in db")
    user_dict: dict[str, Any] = db[username]
    return UserInDB(**user_dict)


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     # token =
#     # user = create_access_token(token)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     print(user, "get_curr")
#     return user

# # api/dependencies.py
# from app.core.security import verify_token  # or decode_token
# from app.db.fake_db import fake_users_db


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     payload = verify_token(token)  # just decodes/validates
#     user = fake_users_db.get(payload.get("sub"))
#     return user


# async def get_current_active_user(current_user=Depends(get_current_user)):
#     if not current_user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
#         )
#     return current_user


# from fastapi import Header, HTTPException, status
# from app.core.security import decode_access_token, get_user_from_db  # your existing functions

# async def get_current_user(
#     authorization: str | None = Header(default=None)
# ):
#     if not authorization:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Missing Authorization header",
#         )

#     scheme, _, token = authorization.partition(" ")
#     if scheme.lower() != "bearer" or not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication scheme",
#         )

#     try:
#         payload = decode_access_token(token)
#     except Exception as e:  # you can catch your JWT library's specific exceptions
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token",
#         ) from e

#     user = get_user_from_db(payload["sub"])
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found",
#         )

#     return user
