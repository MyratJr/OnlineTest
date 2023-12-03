"""hello bababru

Revision ID: 9f96895a85f7
Revises: aadf0aed8127
Create Date: 2023-11-25 11:49:18.969759

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f96895a85f7'
down_revision: Union[str, None] = 'aadf0aed8127'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'login_code')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('login_code', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
