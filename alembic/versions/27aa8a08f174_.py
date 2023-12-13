"""empty message

Revision ID: 27aa8a08f174
Revises: 707ed33da3a0
Create Date: 2023-12-13 13:26:54.763184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27aa8a08f174'
down_revision: Union[str, None] = '707ed33da3a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
