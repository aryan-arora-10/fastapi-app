""" fixing title field posts table

Revision ID: f2ad7123ae3d
Revises: 3d325a1dd68c
Create Date: 2024-02-13 16:27:04.114497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2ad7123ae3d'
down_revision: Union[str, None] = '3d325a1dd68c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('posts','titile')
    op.add_column('posts',sa.Column('title',sa.String,nullable=False))


def downgrade() -> None:
    pass
