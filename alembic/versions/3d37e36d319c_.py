"""empty message

Revision ID: 3d37e36d319c
Revises: 4fe9cf021255
Create Date: 2023-12-14 09:21:09.427216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d37e36d319c'
down_revision: Union[str, None] = '4fe9cf021255'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
