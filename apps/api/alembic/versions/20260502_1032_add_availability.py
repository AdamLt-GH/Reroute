"""add availability windows

Revision ID: 20260502_1032
Revises: 20260428_2229
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260502_1032"
down_revision: str | None = "20260428_2229"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "availability_windows",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("day_of_week", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=True),
        sa.Column("effective_until", sa.Date(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
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
        sa.CheckConstraint(
            "day_of_week >= 0 AND day_of_week <= 6",
            name=op.f("ck_availability_windows_valid_weekday"),
        ),
        sa.CheckConstraint(
            "start_time < end_time",
            name=op.f("ck_availability_windows_valid_time_range"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_availability_windows_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_availability_windows"),
        ),
    )
    op.create_index(
        op.f("ix_availability_windows_user_id"),
        "availability_windows",
        ["user_id"],
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_availability_windows_user_id"),
        table_name="availability_windows",
    )
    op.drop_table("availability_windows")
