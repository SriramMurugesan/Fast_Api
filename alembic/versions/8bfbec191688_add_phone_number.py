"""add phone number

Revision ID: 8bfbec191688
Revises: 60042146ef31
Create Date: 2025-03-09 14:11:36.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bfbec191688'
down_revision = '60042146ef31'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
