"""empty message

Revision ID: 3b0db25dcefe
Revises: 6202551751be
Create Date: 2023-12-09 09:51:03.297718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b0db25dcefe'
down_revision: Union[str, None] = '6202551751be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('login_code', sa.Column('expired_time', sa.Time(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('login_code', 'expired_time')
    # ### end Alembic commands ###
