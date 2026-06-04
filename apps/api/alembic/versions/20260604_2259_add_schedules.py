"""add schedules and blocks

Revision ID: 20260604_2259
Revises: 20260502_1032
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260604_2259"
down_revision: str | None = "20260502_1032"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def timestamps() -> tuple[sa.Column[object], sa.Column[object]]:
    return (
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
    )


def upgrade() -> None:
    op.create_table(
        "schedules",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("horizon_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("horizon_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("source", sa.String(length=30), nullable=False),
        sa.Column("parent_schedule_id", sa.Uuid(), nullable=True),
        sa.Column("id", sa.Uuid(), nullable=False),
        *timestamps(),
        sa.ForeignKeyConstraint(
            ["parent_schedule_id"],
            ["schedules.id"],
            name=op.f("fk_schedules_parent_schedule_id_schedules"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_schedules_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_schedules")),
    )
    op.create_index(op.f("ix_schedules_user_id"), "schedules", ["user_id"])

    op.create_table(
        "schedule_blocks",
        sa.Column("schedule_id", sa.Uuid(), nullable=False),
        sa.Column("task_id", sa.Uuid(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("locked", sa.Boolean(), nullable=False),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        *timestamps(),
        sa.ForeignKeyConstraint(
            ["schedule_id"],
            ["schedules.id"],
            name=op.f("fk_schedule_blocks_schedule_id_schedules"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            name=op.f("fk_schedule_blocks_task_id_tasks"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_schedule_blocks")),
    )
    op.create_index(
        op.f("ix_schedule_blocks_schedule_id"),
        "schedule_blocks",
        ["schedule_id"],
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_schedule_blocks_schedule_id"),
        table_name="schedule_blocks",
    )
    op.drop_table("schedule_blocks")
    op.drop_index(op.f("ix_schedules_user_id"), table_name="schedules")
    op.drop_table("schedules")
