"""Initial migration

Revision ID: 6592d88a81df
Revises:
Create Date: 2024-01-16 15:31:01.312021

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6592d88a81df"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "lifecycle_status",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("value", sa.String(), nullable=False),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": ""}',
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("value"),
        schema="codes",
    )
    op.create_table(
        "plan",
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": ""}',
            nullable=False,
        ),
        sa.Column("approved_at", sa.DateTime(), nullable=True),
        sa.Column("lifecycle_status_id", sa.Integer(), nullable=False),
        sa.Column(
            "id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("exported_at", sa.DateTime(), nullable=True),
        sa.Column("valid_from", sa.DateTime(), nullable=True),
        sa.Column("valid_to", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["lifecycle_status_id"],
            ["codes.lifecycle_status.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("plan", schema="hame")
    op.drop_table("lifecycle_status", schema="codes")
    # ### end Alembic commands ###
