""" rm  content col from users

Revision ID: 3d325a1dd68c
Revises: 9dd8f2890eb3
Create Date: 2024-02-13 16:18:38.489647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d325a1dd68c'
down_revision: Union[str, None] = '9dd8f2890eb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users','content') 


def downgrade() -> None:
    pass
