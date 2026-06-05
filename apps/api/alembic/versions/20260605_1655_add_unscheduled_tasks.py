"""add unscheduled tasks to schedules

Revision ID: 20260605_1655
Revises: 20260604_2259
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260605_1655"
down_revision: str | None = "20260604_2259"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "schedules",
        sa.Column(
            "unscheduled_task_ids",
            sa.JSON(),
            server_default="[]",
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("schedules", "unscheduled_task_ids")
