"""update_it_task_schema

Revision ID: a4015339063f
Revises: 6331b03b6dc1
Create Date: 2026-04-15 19:54:36.590032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4015339063f'
down_revision: Union[str, Sequence[str], None] = '6331b03b6dc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
