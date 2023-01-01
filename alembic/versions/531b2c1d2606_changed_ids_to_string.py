"""changed ids to string

Revision ID: 531b2c1d2606
Revises: 6ec0f6078bae
Create Date: 2022-12-29 16:13:25.468598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "531b2c1d2606"
down_revision = "6ec0f6078bae"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint("post_user_id_fkey", "post", type_="foreignkey")
    op.alter_column("user", "id", type_=sa.String(64))
    op.alter_column("post", "id", type_=sa.String(64))
    op.alter_column("post", "user_id", type_=sa.String(64))
    op.create_foreign_key("user_id", "post", "user", ["user_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint("user_id", "post", type_="foreignkey")
    op.alter_column("user", "id", type_=sa.Integer)
    op.alter_column("post", "id", type_=sa.Integer)
    op.alter_column("post", "user_id", type_=sa.Integer)
    op.create_foreign_key("user_id", "post", "user", ["user_id"], ["id"])
