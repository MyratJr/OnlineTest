"""empty message

Revision ID: ee2e4ed59705
Revises: 2c596d6b7e2d
Create Date: 2023-12-23 12:43:06.385866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee2e4ed59705'
down_revision: Union[str, None] = '2c596d6b7e2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('name', sa.String(), server_default='user', nullable=False))
    op.add_column('admin', sa.Column('surname', sa.String(), server_default='userow', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admin', 'surname')
    op.drop_column('admin', 'name')
    # ### end Alembic commands ###
