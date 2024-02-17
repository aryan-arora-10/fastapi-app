"""create posts table

Revision ID: f4a76bd4a028
Revises: 
Create Date: 2024-02-12 12:24:23.839202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4a76bd4a028'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts'
        , sa.Column('id',sa.Integer(),nullable=False,primary_key=True)
        , sa.Column('titile',sa.String(),nullable=False)
        )
    pass

def downgrade() -> None:
    op.drop_table('posts')
    pass
