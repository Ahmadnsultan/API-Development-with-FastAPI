"""create a relationship

Revision ID: 5ca668c1bd1e
Revises: 8babac564381
Create Date: 2023-03-31 13:53:38.227757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ca668c1bd1e'
down_revision = '8babac564381'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id',sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table="posts", referent_table="users",
                          local_cols=["user_id"], remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', 'posts')
    op.drop_column('posts', 'user_id')
    pass
