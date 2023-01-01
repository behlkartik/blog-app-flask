"""added timestamp to post

Revision ID: dc718748e5d1
Revises: 531b2c1d2606
Create Date: 2022-12-30 23:34:13.984209

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = "dc718748e5d1"
down_revision = "531b2c1d2606"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "post",
        sa.Column("timestamp", sa.DateTime, index=True, default=datetime.utcnow()),
    )


def downgrade() -> None:
    op.drop_column("post", "timestamp")
