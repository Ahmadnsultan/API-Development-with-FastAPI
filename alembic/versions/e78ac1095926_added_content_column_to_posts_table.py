"""Added Content Column to posts table

Revision ID: e78ac1095926
Revises: 3e04511c8b8a
Create Date: 2023-03-31 11:40:29.339775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e78ac1095926'
down_revision = '3e04511c8b8a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
