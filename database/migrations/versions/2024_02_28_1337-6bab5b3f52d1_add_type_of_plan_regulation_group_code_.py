"""add type of plan regulation group code table

Revision ID: 6bab5b3f52d1
Revises: ad29908c50ad
Create Date: 2024-02-28 13:37:39.733685

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6bab5b3f52d1"
down_revision: Union[str, None] = "f085148de65d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "type_of_plan_regulation_group",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), server_default="", nullable=False),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column(
            "description",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("level", sa.Integer(), server_default="1", nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=True),
        sa.Column(
            "id",
            sa.UUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["codes.type_of_plan_regulation_group.id"],
            name="type_of_plan_regulation_group_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_plan_regulation_group_level"),
        "type_of_plan_regulation_group",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_plan_regulation_group_parent_id"),
        "type_of_plan_regulation_group",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_plan_regulation_group_short_name"),
        "type_of_plan_regulation_group",
        ["short_name"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_plan_regulation_group_value"),
        "type_of_plan_regulation_group",
        ["value"],
        unique=True,
        schema="codes",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_codes_type_of_plan_regulation_group_value"),
        table_name="type_of_plan_regulation_group",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_plan_regulation_group_short_name"),
        table_name="type_of_plan_regulation_group",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_plan_regulation_group_parent_id"),
        table_name="type_of_plan_regulation_group",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_plan_regulation_group_level"),
        table_name="type_of_plan_regulation_group",
        schema="codes",
    )
    op.drop_table("type_of_plan_regulation_group", schema="codes")
    # ### end Alembic commands ###
