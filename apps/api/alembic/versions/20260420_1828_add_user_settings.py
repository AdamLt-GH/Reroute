"""add user scheduling settings

Revision ID: 20260420_1828
Revises: 20260420_1249
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260420_1828"
down_revision: str | None = "20260420_1249"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user_settings",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("preferred_day_start", sa.Time(), nullable=False),
        sa.Column("preferred_day_end", sa.Time(), nullable=False),
        sa.Column("maximum_daily_work_minutes", sa.Integer(), nullable=False),
        sa.Column("schedule_change_weight", sa.Float(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_user_settings_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_user_settings")),
    )


def downgrade() -> None:
    op.drop_table("user_settings")
