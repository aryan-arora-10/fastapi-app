"""create users table

Revision ID: 2c76b38b8f8b
Revises: 1a3ef7d02da3
Create Date: 2024-02-12 16:08:46.885499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c76b38b8f8b'
down_revision: Union[str, None] = 'f4a76bd4a028'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('content',sa.String(),nullable=False),
    sa.Column('id',sa.Integer(), primary_key=True,nullable=False),
    sa.Column('email',sa.String(), nullable = False,unique = True),# unique prevents a user from registering twice
    sa.Column('password',sa.String(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()'))
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
