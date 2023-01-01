"""added post table

Revision ID: 6ec0f6078bae
Revises: dc1066aab010
Create Date: 2022-12-29 04:40:56.666449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6ec0f6078bae"
down_revision = "dc1066aab010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "post",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(64), index=True, unique=True),
        sa.Column("content", sa.String(256), index=True, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("post")
