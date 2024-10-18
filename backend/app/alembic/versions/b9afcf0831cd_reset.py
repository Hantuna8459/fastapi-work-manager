"""reset

Revision ID: b9afcf0831cd
Revises: 6d70331e2edf
Create Date: 2024-10-18 15:13:32.894829

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9afcf0831cd'
down_revision: Union[str, None] = '6d70331e2edf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
