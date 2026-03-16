from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    model_config = ConfigDict(extra="forbid")


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class PostSchema(BaseModel):
    title: str
    # id: int
    content: str


class PostUpdate(Post):
    pass
