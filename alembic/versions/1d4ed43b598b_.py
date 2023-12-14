"""empty message

Revision ID: 1d4ed43b598b
Revises: 3d37e36d319c
Create Date: 2023-12-14 09:51:02.172127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d4ed43b598b'
down_revision: Union[str, None] = '3d37e36d319c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
