"""added tags table for tag to category relation

Revision ID: eef1a87f787e
Revises: a5f747dd1521
Create Date: 2023-01-01 01:27:42.760483

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = "eef1a87f787e"
down_revision = "a5f747dd1521"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tags",
        sa.Column(
            "tag_id",
            sa.String(64),
            sa.ForeignKey("tag.id"),
            primary_key=True,
            default=str(uuid4()),
        ),
        sa.Column(
            "category_id",
            sa.String(64),
            sa.ForeignKey("category.id"),
            primary_key=True,
            default=str(uuid4()),
        ),
    )


def downgrade() -> None:
    op.drop_table("tags")
