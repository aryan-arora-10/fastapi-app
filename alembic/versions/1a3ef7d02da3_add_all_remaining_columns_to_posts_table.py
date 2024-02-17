"""add all remaining columns to posts table

Revision ID: 1a3ef7d02da3
Revises: f4a76bd4a028
Create Date: 2024-02-12 15:53:54.427885

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1a3ef7d02da3'
down_revision: Union[str, None] = '2c76b38b8f8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    op.add_column('posts',sa.Column('content',sa.String,nullable=False))
    op.add_column('posts',sa.Column('published',sa.Boolean, server_default='TRUE',nullable=False) )
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))
    op.add_column('posts',sa.Column('owner_id',sa.Integer,sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False))

    pass





def downgrade() -> None:
    op.drop_column('posts','content') 
    op.drop_column('posts','published') 
    op.drop_column('posts','created_at') 
    op.drop_column('posts','owner_id') 
    
    pass
