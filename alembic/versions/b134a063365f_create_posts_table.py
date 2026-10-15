"""create posts table

Revision ID: b134a063365f
Revises: 
Create Date: 2026-10-08 12:35:42.793899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from sqlalchemy import INTEGER, TIMESTAMP, func, String


# revision identifiers, used by Alembic.
revision: str = 'b134a063365f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""

    op.create_table(
        "posts",
        sa.Column("id", INTEGER, primary_key=True),
        sa.Column("title", String(50), nullable=False),
        # sa.Column("description", String(200)),
        # sa.Column("timestamp", TIMESTAMP, server_default=func.now()),
    )



def downgrade():
    """Downgrade schema."""

    op.drop_table('posts')


