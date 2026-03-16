# app/docs/posts.py

from typing import Any, TypedDict


class PostOperationDocs(TypedDict):
    summary: str
    description: str


# ---------------------------
# GET /posts/{id}
# ---------------------------


# Extract common responses into separate constants:

POST_NOT_FOUND_RESPONSE = {
    404: {
        "description": "Post not found",
        "content": {
            "application/json": {"example": {"detail": {"message": "Post not found"}}}
        },
    }
}

FORBIDDEN_RESPONSE = {
    403: {
        "description": "Not authorized",
        "content": {
            "application/json": {
                "example": {"detail": {"message": "You do not have permission"}}
            }
        },
    }
}


GET_POST_DOCS: PostOperationDocs = {
    "summary": "Get a single post by ID",
    "description": "Fetch a post using its unique ID. Returns 404 if not found.",
}

GET_POST_RESPONSES: dict[int | str, dict[str, Any]] = {**POST_NOT_FOUND_RESPONSE}

# ---------------------------
# DELETE /posts/{id}
# ---------------------------

DELETE_POST_DOCS: PostOperationDocs = {
    "summary": "Delete a post",
    "description": (
        "Delete a post by its unique ID.\n\n"
        "- The post must exist\n"
        "- Only the post owner (or an admin) may delete it\n"
        "- Returns 204 on success"
    ),
}

DELETE_POST_RESPONSES: dict[int | str, dict[str, Any]] = {
    **POST_NOT_FOUND_RESPONSE,
    403: {
        "description": "Not authorized to delete this post",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "message": "You do not have permission to delete this post"
                    }
                }
            }
        },
    },
}

UPDATE_POST_DOCS: PostOperationDocs = {
    "summary": "Update a post",
    "description": "Update an existing post identified by its ID...",
}

UPDATE_POST_RESPONSES: dict[int | str, dict[str, Any]] = {
    204: {"description": "Post updated successfully"},
    **POST_NOT_FOUND_RESPONSE,
    422: {
        "description": "Validation error",
        "content": {
            "application/json": {
                "example": {"detail": {"message": "Error processing entry"}}
            }
        },
    },
}
