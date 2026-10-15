"""add foreign-key to posts table

Revision ID: 1dc9f84e44f1
Revises: a5241bc2857a
Create Date: 2026-10-08 16:07:13.416685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1dc9f84e44f1'
down_revision: Union[str, Sequence[str], None] = 'a5241bc2857a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""

    op.add_column(
                    'posts', 
                    sa.Column('owner_id', sa.Integer(), nullable=False)
                )
    
    op.create_foreign_key(
                            'post_users_fk', 
                            source_table="posts", 
                            referent_table="users", 
                            local_cols=['owner_id'], 
                            remote_cols=['id'], 
                            ondelete="CASCADE"
                        )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
