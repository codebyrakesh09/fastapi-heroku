"""add last few columns to posts table 

Revision ID: 86419082ef80
Revises: 1dc9f84e44f1
Create Date: 2026-10-08 16:31:35.643871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86419082ef80'
down_revision: Union[str, Sequence[str], None] = '1dc9f84e44f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))

    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

    pass
