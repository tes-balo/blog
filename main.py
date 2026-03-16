import sys
from contextlib import asynccontextmanager

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Request, status
from psycopg2.extensions import (
    connection,
    cursor as CursorType,  # noqa: N812
)
from psycopg2.extras import RealDictCursor

from docs.posts import (
    DELETE_POST_DOCS,
    DELETE_POST_RESPONSES,
    GET_POST_DOCS,
    GET_POST_RESPONSES,
    UPDATE_POST_DOCS,
    UPDATE_POST_RESPONSES,
)
from schemas.schema import Post, PostUpdate


def get_db(request: Request) -> connection:
    return request.app.state.conn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    try:
        app.state.conn = psycopg2.connect(
            host="127.0.0.1",  # WSL → Windows
            database="blogs",
            user="postgres",
            password="5248",
            cursor_factory=RealDictCursor,
        )
        print("✅ Database connection successful")
    except Exception as e:
        print("❌ DB connection failed")
        print("Error:", e)
        sys.exit(1)  # stop the app if DB connection fails

    yield  # control goes to FastAPI routes

    # Shutdown code
    app.state.conn.close()
    print("Database connection closed")


# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

my_posts: list[dict[str, str | int]] = [
    {
        "title": "title of posts",
        "content": "content of posts",
        "id": 1,
    },
    {
        "title": "my favorite foods",
        "content": "I really like pizza",
        "id": 2,
    },
]

# install faker for testing


@app.get("/")
async def root(request: Request):
    return {"url": str(request.url), "method": request.method}


@app.get(
    "/posts/{id}",
    # response_model=PostSchema,
    **GET_POST_DOCS,
    responses=GET_POST_RESPONSES,
    status_code=200,
)
async def get_post_by_id(id: int, conn: connection = Depends(get_db)):
    # cursor.execute()
    # for post in my_posts:
    #     if post["id"] is not id:
    #         raise HTTPException(status_code=404,
    #             detail= {"data": "user not found"}
    #         )
    #     if post["id"] == id:
    #         return post

    #     pytho
    cursor = conn.cursor()
    cursor.execute("""select * from posts where id = %s """, (id,))
    post = cursor.fetchone()
    print(post)

    # post = next((p for p in my_posts if p["id"] == id), None)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"data": "Post not found"}
        )
    print(post)
    return post


@app.get("/posts")
async def get_posts(conn: connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("""select * from posts""")

    return cursor.fetchall()


@app.get("/posts/latest")
async def get_latest_post():
    return my_posts[len(my_posts) - 1]


# refactor and embed a 201 status code, shift utility
# function to utils.py or helpers.py (ask gpt to be sure)
# use tags as well (ask gpt their uses)
@app.post(
    "/posts",
)
async def create_post(
    post_payload: Post,
    conn: connection = Depends(get_db),
):
    # post_dict = post_payload.model_dump()
    # post_dict["id"] = randrange(1, 100000)
    # my_posts.append(post_dict)
    cursor: CursorType = app.state.conn.cursor()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """insert into posts (id, title, content, published, created_at) values (%s, %s, %s, %s, %s) returning *""",
            (
                post_payload.id,
                post_payload.title,
                post_payload.content,
                post_payload.published,
                post_payload.created_at,
            ),
        )
        conn.commit()
        return cursor.fetchone()

    except Exception as error:
        print(f"Unable to create post {error}")
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database error") from error

    # print(my_posts)
    # return {"data": post_payload}

    post = cursor.fetchall()
    print(post)
    return post


@app.delete(
    "/posts/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    **DELETE_POST_DOCS,
    responses=DELETE_POST_RESPONSES,
)
async def delete_post(id: int, conn: connection = Depends(get_db)):
    # for index, post in enumerate(my_posts):
    #     if post["id"] == id:
    #         del my_posts[index]
    #         return
    # try:
    cursor = conn.cursor()
    cursor.execute("""delete from posts where id = %s returning *""", (id,))
    post = cursor.fetchone()
    conn.commit()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail={"data": "Post not found"}
        )


# update post without updating all its members


@app.put(
    "/posts/{id}",
    **UPDATE_POST_DOCS,
    responses=UPDATE_POST_RESPONSES,
    status_code=status.HTTP_200_OK,
)  # todo: implement update posts by generating sql dynamically via a for k, v loop
async def update_post(id: int, payload: PostUpdate, conn: connection = Depends(get_db)):
    cursor = conn.cursor()
    try:
        cursor.execute(
            """ update posts set id = %s, content = %s, published = %s, title = %s, created_at = %s where id = %s""",
            (
                payload.id,
                payload.content,
                payload.published,
                payload.title,
                payload.created_at,
                id,
            ),
        )

        # updated_post = cursor.fetchone()
        if cursor.rowcount is None:
            raise HTTPException(status_code=404, detail={"data": "Post not found"})
        conn.commit()
    # for _, post in enumerate(my_posts):
    #     if post["id"] == id:
    #         post.update(payload.model_dump())
    #         return

    except HTTPException:
        raise

    except Exception:
        conn.rollback()
        raise


# refactor to update necessary fields only, dont replace entire dict
