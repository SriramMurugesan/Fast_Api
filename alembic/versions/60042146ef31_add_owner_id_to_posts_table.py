"""Add owner_id to posts table

Revision ID: 60042146ef31
Revises: 
Create Date: 2025-03-04 17:41:46.420472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from app import models, schemas


# revision identifiers, used by Alembic.
revision: str = '60042146ef31'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add owner_id column as nullable first
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=True))
    
    # Get first user's id or create a default user if none exists
    connection = op.get_bind()
    result = connection.execute(sa.text("SELECT id FROM users ORDER BY id LIMIT 1"))
    default_user_id = result.scalar()
    if default_user_id is None:
        result = connection.execute(
            sa.text("INSERT INTO users (email, password) VALUES ('default@example.com', 'default_password') RETURNING id")
        )
        default_user_id = result.scalar()
    
    # Update existing posts to use the default user
    op.execute(f"UPDATE posts SET owner_id = {default_user_id} WHERE owner_id IS NULL")
    
    # Now make the column non-nullable
    op.alter_column('posts', 'owner_id', nullable=False)
    
    # Add the foreign key constraint
    op.create_foreign_key(None, 'posts', 'users', ['owner_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
