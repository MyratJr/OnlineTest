"""empty message

Revision ID: 707ed33da3a0
Revises: 7c0a922f8d0b
Create Date: 2023-12-13 13:04:53.400719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '707ed33da3a0'
down_revision: Union[str, None] = '7c0a922f8d0b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
