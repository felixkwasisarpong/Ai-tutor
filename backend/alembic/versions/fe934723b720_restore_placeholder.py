"""restore placeholder for missing migration

Revision ID: fe934723b720
Revises: 
Create Date: 2026-01-20 00:00:00.000000
"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "fe934723b720"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # No-op placeholder to restore missing migration.
    pass


def downgrade() -> None:
    # No-op placeholder to restore missing migration.
    pass
