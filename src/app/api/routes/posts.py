from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.database import get_db
from app.db.tables.posts import posts
from app.docs.posts import (
    DELETE_POST_DOCS,
    DELETE_POST_RESPONSES,
    GET_POST_DOCS,
    GET_POST_RESPONSES,
    UPDATE_POST_DOCS,
)
from app.schemas.schema import (
    PostCreate,
    PostResponse,
    PostUpdate,
)

router = APIRouter(prefix="/posts", tags=["Blog Posts"])
posts_router = router


@router.get(
    "/posts/{id}",
    response_model=PostResponse,
    **GET_POST_DOCS,
    responses=GET_POST_RESPONSES,
    status_code=200,
)
async def get_post_by_id(
    id: int, conn: AsyncConnection = Depends(get_db)
) -> PostResponse:
    stmt = select(posts).where(posts.c.id == id)
    result = await conn.execute(stmt)
    # print(post)
    db_post = result.mappings().first()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"data": "Post not found"},
        )
    print(db_post)
    return PostResponse.model_validate(db_post)


@router.get("/posts", response_model=list[PostResponse])
async def get_posts(
    conn: AsyncConnection = Depends(get_db),
    # current_user = Depends(get_current_user),
) -> list[PostResponse]:
    stmt = select(posts)
    result = await conn.execute(stmt)
    db_posts = result.mappings().all()

    return [PostResponse.model_validate(db_post) for db_post in db_posts]


# @router.get("/posts/latest")
# async def get_latest_post():
#     return my_posts[len(my_posts) - 1]


# refactor and embed a 201 status code, shift utility
# function to utils.py or helpers.py (ask gpt to be sure)
# use tags as well (ask gpt their uses)
@router.post("/posts", response_model=PostResponse)
async def create_post(
    post_payload: PostCreate,
    conn: AsyncConnection = Depends(get_db),
    # current_user = Depends(get_current_active_user),
) -> PostResponse:
    try:
        stmt = insert(posts).values(**post_payload.model_dump()).returning(posts)
        result = await conn.execute(stmt)
        db_post = result.mappings().one()
        await conn.commit()
        return PostResponse.model_validate(db_post)

    except Exception as error:
        print(f"Unable to create post {error}")
        await conn.rollback()
        raise HTTPException(status_code=500, detail="Database error") from error


@router.delete(
    "/posts/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    **DELETE_POST_DOCS,
    responses=DELETE_POST_RESPONSES,
)
async def delete_post(id: int, conn: AsyncConnection = Depends(get_db)) -> None:
    stmt = delete(posts).where(posts.c.id == id).returning(posts)
    result = await conn.execute(stmt)
    db_post = result.mappings().one_or_none()
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"data": "Post not found"},
        )

    await conn.commit()


# update post without updating all its members


@router.patch(
    "/posts/{id}",
    **UPDATE_POST_DOCS,
    # responses=UPDATE_POST_RESPONSES,
    status_code=status.HTTP_200_OK,
)  # todo: implement update posts by generating sql dynamically via a for k, v loop
async def update_post(
    id: int,
    payload: PostUpdate,
    conn: AsyncConnection = Depends(get_db),
) -> PostResponse:
    print("entry")
    try:
        update_data: dict[str, object] = payload.model_dump(
            exclude_unset=True, exclude_none=True
        )

        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="At least one updatable field must be provided",
            )

        for field in ["id", "created_at"]:
            update_data.pop(field, None)
        print(payload.model_dump())
        stmt = (
            update(posts).where(posts.c.id == id).values(**update_data).returning(posts)
        )

        result = await conn.execute(stmt)
        db_post = result.mappings().one_or_none()
        # print(updated_post)
        if db_post is None:
            raise HTTPException(status_code=404, detail={"data": "Post not found"})
        await conn.commit()

        return PostResponse.model_validate(db_post)

    except HTTPException:
        raise

    except Exception:
        await conn.rollback()
        raise
