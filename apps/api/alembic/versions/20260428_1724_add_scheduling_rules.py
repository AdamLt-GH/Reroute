"""add scheduling constraints and preferences

Revision ID: 20260428_1724
Revises: 20260428_1212
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260428_1724"
down_revision: str | None = "20260428_1212"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def common_columns() -> tuple[sa.Column[object], ...]:
    return (
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("kind", sa.String(length=50), nullable=False),
        sa.Column("settings", sa.JSON(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
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
    )


def upgrade() -> None:
    op.create_table(
        "scheduling_constraints",
        *common_columns(),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_scheduling_constraints_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_scheduling_constraints"),
        ),
    )
    op.create_index(
        op.f("ix_scheduling_constraints_user_id"),
        "scheduling_constraints",
        ["user_id"],
    )

    op.create_table(
        "scheduling_preferences",
        *common_columns(),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_scheduling_preferences_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id",
            name=op.f("pk_scheduling_preferences"),
        ),
    )
    op.create_index(
        op.f("ix_scheduling_preferences_user_id"),
        "scheduling_preferences",
        ["user_id"],
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_scheduling_preferences_user_id"),
        table_name="scheduling_preferences",
    )
    op.drop_table("scheduling_preferences")
    op.drop_index(
        op.f("ix_scheduling_constraints_user_id"),
        table_name="scheduling_constraints",
    )
    op.drop_table("scheduling_constraints")
