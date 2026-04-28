"""add flexible tasks and dependencies

Revision ID: 20260428_1212
Revises: 20260426_0952
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260428_1212"
down_revision: str | None = "20260426_0952"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def timestamp_columns() -> tuple[sa.Column[object], sa.Column[object]]:
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
        "tasks",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("estimated_minutes", sa.Integer(), nullable=False),
        sa.Column("remaining_minutes", sa.Integer(), nullable=False),
        sa.Column("actual_minutes", sa.Integer(), nullable=False),
        sa.Column("earliest_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("minimum_session_minutes", sa.Integer(), nullable=False),
        sa.Column("maximum_session_minutes", sa.Integer(), nullable=False),
        sa.Column("preferred_session_minutes", sa.Integer(), nullable=False),
        sa.Column("splittable", sa.Boolean(), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False),
        sa.Column("difficulty", sa.String(length=20), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_tasks_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tasks")),
    )
    op.create_index(op.f("ix_tasks_deadline"), "tasks", ["deadline"])
    op.create_index(op.f("ix_tasks_user_id"), "tasks", ["user_id"])

    op.create_table(
        "task_dependencies",
        sa.Column("prerequisite_id", sa.Uuid(), nullable=False),
        sa.Column("dependent_id", sa.Uuid(), nullable=False),
        *timestamp_columns(),
        sa.ForeignKeyConstraint(
            ["dependent_id"],
            ["tasks.id"],
            name=op.f("fk_task_dependencies_dependent_id_tasks"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["prerequisite_id"],
            ["tasks.id"],
            name=op.f("fk_task_dependencies_prerequisite_id_tasks"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "prerequisite_id",
            "dependent_id",
            name=op.f("pk_task_dependencies"),
        ),
    )


def downgrade() -> None:
    op.drop_table("task_dependencies")
    op.drop_index(op.f("ix_tasks_user_id"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_deadline"), table_name="tasks")
    op.drop_table("tasks")
