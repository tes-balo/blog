import secrets

from sqlalchemy import (
    TIMESTAMP,
    UUID,
    VARCHAR,
    Boolean,
    Column,
    Table,
    text,
)

from app.db.database import metadata


def generate_username() -> str:
    return f"user_{secrets.token_hex(6)}"


users = Table(
    "users",
    metadata,
    Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("uuidv7()"),
    ),
    Column("email", VARCHAR(50), nullable=False, unique=True, index=True),
    Column("first_name", VARCHAR(50), nullable=True),
    Column("last_name", VARCHAR(50), nullable=True),
    Column("phone_number", VARCHAR(20), nullable=True, unique=True),
    Column(
        "username",
        VARCHAR(20),
        nullable=False,
        unique=True,
        default=generate_username,
    ),
    Column("password", VARCHAR(255), nullable=False),
    Column("is_active", Boolean, nullable=False, server_default=text("true")),
    Column(
        "is_verified",
        Boolean,
        nullable=False,
        server_default=text("false"),
    ),
    Column("is_admin", Boolean, nullable=False, server_default=text("false")),
    Column(
        "created_at",
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    ),
    Column(
        "updated_at",
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ),
    Column(
        "last_login_at",
        TIMESTAMP(timezone=True),
        nullable=True,
    ),
    # update delete route later to do a soft delete rather than a hard one, make sure sql does update users set deleted_at = CURRENT_TIMESTAMP
    Column(
        "deleted_at",
        TIMESTAMP(timezone=True),
        nullable=True,
    ),
    # use later
    Column(
        "organization_id",
        UUID(as_uuid=True),
        nullable=True,  # can be null for now
    ),
)
