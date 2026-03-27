"""add default to published

Revision ID: 3f9fb25e15be
Revises: 2304f33826fd
Create Date: 2026-03-18 18:23:31.337708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f9fb25e15be'
down_revision = '2304f33826fd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Set server default for 'published' column to true."""
    op.alter_column(
        "posts",
        "published",
        server_default=sa.text("true"),
        existing_type=sa.Boolean(),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Remove server default for 'published' column."""
    op.alter_column(
        "posts",
        "published",
        server_default=None,
        existing_type=sa.Boolean(),
        existing_nullable=False,
    )