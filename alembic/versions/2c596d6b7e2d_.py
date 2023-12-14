"""empty message

Revision ID: 2c596d6b7e2d
Revises: ee0f138c38cb
Create Date: 2023-12-14 13:14:47.098177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c596d6b7e2d'
down_revision: Union[str, None] = 'ee0f138c38cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
