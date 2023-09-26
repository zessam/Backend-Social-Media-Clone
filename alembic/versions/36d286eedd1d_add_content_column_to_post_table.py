"""add content column to post table

Revision ID: 36d286eedd1d
Revises: bfb060282754
Create Date: 2023-09-26 04:19:43.240395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36d286eedd1d'
down_revision: Union[str, None] = 'bfb060282754'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
