from sqlalchemy import (
    TIMESTAMP,
    UUID,
    Boolean,
    Column,
    String,
    Table,
    text,
)

from app.db.database import metadata

posts = Table(
    "posts",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuidv7()"),
    ),
    Column("title", String, nullable=False),
    Column("content", String, nullable=False),
    Column("published", Boolean, nullable=False, server_default=text("true")),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
    ),
)
