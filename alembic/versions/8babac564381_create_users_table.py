"""Create Users table

Revision ID: 8babac564381
Revises: e78ac1095926
Create Date: 2023-03-31 13:22:02.176059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8babac564381'
down_revision = 'e78ac1095926'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
