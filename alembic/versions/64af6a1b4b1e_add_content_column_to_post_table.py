"""add content column to post table

Revision ID: 64af6a1b4b1e
Revises: b134a063365f
Create Date: 2026-10-08 13:25:03.942388

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64af6a1b4b1e'
down_revision: Union[str, Sequence[str], None] = 'b134a063365f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""

    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    """Downgrade schema."""

    op.drop_column('posts', 'content')
    pass
