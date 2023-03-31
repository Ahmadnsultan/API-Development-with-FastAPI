"""Create post table

Revision ID: 3e04511c8b8a
Revises: 
Create Date: 2023-03-31 11:06:23.146856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e04511c8b8a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
