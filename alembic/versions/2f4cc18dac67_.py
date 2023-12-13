"""empty message

Revision ID: 2f4cc18dac67
Revises: 27aa8a08f174
Create Date: 2023-12-13 13:31:10.716510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f4cc18dac67'
down_revision: Union[str, None] = '27aa8a08f174'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
