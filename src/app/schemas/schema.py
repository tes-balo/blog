from datetime import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    field_validator,
)


class PostBase(BaseModel):
    title: str
    content: str

    model_config = ConfigDict(extra="forbid")


class PostResponse(PostBase):
    id: int
    published: bool
    created_at: datetime
    updated_at: datetime | None = None
    # owner_id: UUID
    # owner_email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class PostCreate(PostBase):
    published: bool = True

    @field_validator("title", "content")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace")
        return v.strip()


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None
    updated_at: datetime | None = None

    @field_validator("title", "content")
    @classmethod
    def validate_optional_fields(cls, v: str | None) -> str | None:
        if v is None:
            return v  # allow omission

        if not v.strip():
            raise ValueError("Field cannot be empty or whitespace")

        return v.strip()


class UserBase(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class UserResponse(UserBase):
    id: UUID
    phone_number: str | None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None = None

    model_config = {"from_attributes": True}


class UserCreate(UserBase):
    username: str
    phone_number: str | None = None
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @field_validator("first_name", "last_name")
    @classmethod
    def clean_names(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip()

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("first_name", "last_name")
    @classmethod
    def normalize_names(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip().title()


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip().lower()

    @field_validator("username", "phone_number")
    @classmethod
    def validate_optional(cls, v: str | None) -> str | None:
        if v is None:
            return v

        if not v.strip():
            raise ValueError("Field cannot be empty")

        return v.strip()


# ✅ Create reusable helpers
# def normalize_email(v: str) -> str:
#     return v.strip().lower()

# def normalize_name(v: str) -> str:
#     return v.strip().title()

# def normalize_text(v: str) -> str:
#     return v.strip()
# Then use:
# @field_validator("email")
# def norm_email(cls, v):
#     return normalize_email(v)
