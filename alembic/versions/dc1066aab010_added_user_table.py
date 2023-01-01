"""added user table

Revision ID: dc1066aab010
Revises: 
Create Date: 2022-12-29 04:37:13.093757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "dc1066aab010"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(64), index=True, unique=True),
        sa.Column("email", sa.String(64), index=True, unique=True),
        sa.Column("password_hash", sa.String(128)),
    )


def downgrade() -> None:
    op.drop_table("user")
