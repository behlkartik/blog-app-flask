"""added category, tags table and relationships

Revision ID: a5f747dd1521
Revises: dc718748e5d1
Create Date: 2022-12-31 23:17:30.793030

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = "a5f747dd1521"
down_revision = "dc718748e5d1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tag",
        sa.Column("id", sa.String(64), primary_key=True, default=str(uuid4())),
        sa.Column("name", sa.String(64), unique=True, index=True),
        sa.Column("post_id", sa.String(64), sa.ForeignKey("post.id"), nullable=False),
    )
    op.create_table(
        "category",
        sa.Column("id", sa.String(64), primary_key=True, default=str(uuid4())),
        sa.Column("name", sa.String(64), unique=True, index=True),
    )
    op.add_column(
        "post",
        sa.Column(
            "category_id", sa.String(64), sa.ForeignKey("category.id"), nullable=False
        ),
    )


def downgrade() -> None:
    op.drop_constraint("post_category_id_fkey", "post", type_="foreignkey")
    op.drop_table("tag")
    op.drop_table("category")
