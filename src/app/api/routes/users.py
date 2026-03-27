from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.database import get_db
from app.db.tables.users import users
from app.docs.posts import DELETE_POST_DOCS, DELETE_POST_RESPONSES
from app.schemas.schema import UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])
users_router = router

# Admin user create
# @router.post("/", response_model=UserResponse)
# async def create_user()


@router.get("/", response_model=list[UserResponse])
async def get_users(conn: AsyncConnection = Depends(get_db)) -> list[UserResponse]:
    stmt = select(users)
    result = await conn.execute(stmt)
    db_users = result.mappings().all()

    return [UserResponse.model_validate(db_user) for db_user in db_users]


@router.get("/{id}", response_model=UserResponse)
async def get_user_by_id(
    id: UUID, conn: AsyncConnection = Depends(get_db)
) -> UserResponse:
    stmt = select(users).where(users.c.id == id)
    result = await conn.execute(stmt)
    db_user = result.mappings().fetchone()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found"},
        )

    return UserResponse.model_validate(db_user)


@router.patch("/{id}", response_model=UserResponse)
async def update_user(
    id: UUID, payload: UserUpdate, conn: AsyncConnection = Depends(get_db)
) -> UserResponse:
    update_data: dict[str, object] = payload.model_dump(
        exclude_unset=True, exclude_none=True
    )

    for field in ["id", "created_at"]:
        update_data.pop(field, None)

    result = await conn.execute(
        update(users).where(users.c.id == id).values(**update_data).returning(users)
    )
    db_user = result.mappings().fetchone()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found"},
        )

    await conn.commit()
    return UserResponse.model_validate(db_user)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    **DELETE_POST_DOCS,
    responses=DELETE_POST_RESPONSES,
)
async def delete_post(id: UUID, conn: AsyncConnection = Depends(get_db)) -> None:
    stmt = delete(users).where(users.c.id == id).returning(users)
    result = await conn.execute(stmt)

    db_user = result.mappings().one_or_none()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"message": "User not found"}
        )
    await conn.commit()


# @router
