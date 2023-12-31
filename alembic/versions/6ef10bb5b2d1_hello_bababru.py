"""hello bababru

Revision ID: 6ef10bb5b2d1
Revises: aa1b81adb240
Create Date: 2023-11-25 11:57:34.189802

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ef10bb5b2d1'
down_revision: Union[str, None] = 'aa1b81adb240'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('name', sa.String(), nullable=False))
    op.add_column('students', sa.Column('surname', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'surname')
    op.drop_column('students', 'name')
    # ### end Alembic commands ###
