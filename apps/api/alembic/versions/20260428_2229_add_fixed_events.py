"""add fixed events

Revision ID: 20260428_2229
Revises: 20260428_1724
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20260428_2229"
down_revision: str | None = "20260428_1724"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "fixed_events",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("location", sa.String(length=300), nullable=True),
        sa.Column("travel_before_minutes", sa.Integer(), nullable=False),
        sa.Column("travel_after_minutes", sa.Integer(), nullable=False),
        sa.Column("recurrence_rule", sa.String(length=500), nullable=True),
        sa.Column("locked", sa.Boolean(), nullable=False),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_fixed_events_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_fixed_events")),
    )
    op.create_index(
        op.f("ix_fixed_events_start_at"),
        "fixed_events",
        ["start_at"],
    )
    op.create_index(
        op.f("ix_fixed_events_user_id"),
        "fixed_events",
        ["user_id"],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_fixed_events_user_id"), table_name="fixed_events")
    op.drop_index(op.f("ix_fixed_events_start_at"), table_name="fixed_events")
    op.drop_table("fixed_events")
