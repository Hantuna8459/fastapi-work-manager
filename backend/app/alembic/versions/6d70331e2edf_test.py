"""test

Revision ID: 6d70331e2edf
Revises: 15105e2f2de3
Create Date: 2024-10-12 00:01:48.349917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d70331e2edf'
down_revision: Union[str, None] = '15105e2f2de3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
