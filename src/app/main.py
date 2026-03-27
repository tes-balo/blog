from fastapi import FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from app.api.api import router
from app.core.metadata import api_metadata
from app.core.middleware.cors import CORSMiddleware, cors_config
from app.core.middleware.logging_config import LoggingMiddleware
from app.core.middleware.security_headers import SecurityHeadersMiddleware
from app.exceptions import global_exception_handler, http_exception_handler

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


app = FastAPI(**api_metadata)

app.include_router(router)
# install faker for testing
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(CORSMiddleware, **cors_config)

# Register exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)


@app.get("/")
async def root(request: Request) -> dict[str, str]:
    return {"url": str(request.url), "method": request.method}


# @app.post("/login")
# async def login(form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()]):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     user = UserInDB(**user_dict)
#     hashed_password = await fake_hash_password(form_data.password)
#     if hashed_password != user.hashed_password:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     print(user_dict["username"])

#     return {"access_token": user_dict["username"]}


# @app.get("/user")
# # async def get_usr(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user
