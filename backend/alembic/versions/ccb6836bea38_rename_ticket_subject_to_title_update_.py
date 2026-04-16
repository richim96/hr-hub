"""rename ticket subject to title, update ticket status enum

Revision ID: ccb6836bea38
Revises: 94d4aa4feeb6
Create Date: 2026-04-16 10:55:37.798327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccb6836bea38'
down_revision: Union[str, Sequence[str], None] = '94d4aa4feeb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop any leftover temp table from a previous failed attempt.
    op.execute("DROP TABLE IF EXISTS _alembic_tmp_ticket")

    # Step 1: add Title as nullable so existing rows pass the NOT NULL check.
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Title', sa.String(), nullable=True))

    # Step 2: backfill Title from Subject for all existing rows.
    op.execute('UPDATE ticket SET "Title" = "Subject"')

    # Step 3: make Title NOT NULL and drop Subject.
    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.alter_column('Title', nullable=False)
        batch_op.drop_column('Subject')


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS _alembic_tmp_ticket")

    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Subject', sa.VARCHAR(), nullable=True))

    op.execute('UPDATE ticket SET "Subject" = "Title"')

    with op.batch_alter_table('ticket', schema=None) as batch_op:
        batch_op.alter_column('Subject', nullable=False)
        batch_op.drop_column('Title')
