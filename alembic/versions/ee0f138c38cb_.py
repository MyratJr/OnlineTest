"""empty message

Revision ID: ee0f138c38cb
Revises: 1d4ed43b598b
Create Date: 2023-12-14 12:14:58.297346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee0f138c38cb'
down_revision: Union[str, None] = '1d4ed43b598b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('registered_time', sa.Time(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'registered_time')
    # ### end Alembic commands ###
