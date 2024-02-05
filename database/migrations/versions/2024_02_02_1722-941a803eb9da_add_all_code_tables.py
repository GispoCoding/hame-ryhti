"""add all code tables

Revision ID: 941a803eb9da
Revises: 13819c34faf2
Create Date: 2024-02-02 17:22:49.169952

"""
from typing import Sequence, Union

# import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "941a803eb9da"
down_revision: Union[str, None] = "13819c34faf2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "plan_type",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), nullable=False),
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
        sa.Column("level", sa.Integer(), server_default="0", nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["parent_id"], ["codes.plan_type.id"], name="plan_type_parent_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_plan_type_level"),
        "plan_type",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_plan_type_parent_id"),
        "plan_type",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_plan_type_short_name"),
        "plan_type",
        ["short_name"],
        unique=True,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_plan_type_value"),
        "plan_type",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.create_table(
        "type_of_additional_information",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), nullable=False),
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
        sa.Column("level", sa.Integer(), server_default="0", nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["codes.type_of_additional_information.id"],
            name="type_of_additional_information_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_additional_information_level"),
        "type_of_additional_information",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_additional_information_parent_id"),
        "type_of_additional_information",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_additional_information_short_name"),
        "type_of_additional_information",
        ["short_name"],
        unique=True,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_additional_information_value"),
        "type_of_additional_information",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.create_table(
        "type_of_plan_regulation",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), nullable=False),
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
        sa.Column("level", sa.Integer(), server_default="0", nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["codes.type_of_plan_regulation.id"],
            name="type_of_plan_regulation_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_plan_regulation_level"),
        "type_of_plan_regulation",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_plan_regulation_parent_id"),
        "type_of_plan_regulation",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_plan_regulation_short_name"),
        "type_of_plan_regulation",
        ["short_name"],
        unique=True,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_plan_regulation_value"),
        "type_of_plan_regulation",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.create_table(
        "type_of_source_data",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), nullable=False),
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
        sa.Column("level", sa.Integer(), server_default="0", nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["codes.type_of_source_data.id"],
            name="type_of_source_data_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_source_data_level"),
        "type_of_source_data",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_source_data_parent_id"),
        "type_of_source_data",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_source_data_short_name"),
        "type_of_source_data",
        ["short_name"],
        unique=True,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_source_data_value"),
        "type_of_source_data",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.create_table(
        "type_of_underground",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), nullable=False),
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
        sa.Column("level", sa.Integer(), server_default="0", nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["codes.type_of_underground.id"],
            name="type_of_underground_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_underground_level"),
        "type_of_underground",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_underground_parent_id"),
        "type_of_underground",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_underground_short_name"),
        "type_of_underground",
        ["short_name"],
        unique=True,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_underground_value"),
        "type_of_underground",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.create_table(
        "type_of_verbal_plan_regulation",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), nullable=False),
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
        sa.Column("level", sa.Integer(), server_default="0", nullable=False),
        sa.Column("parent_id", sa.UUID(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["codes.type_of_verbal_plan_regulation.id"],
            name="type_of_verbal_plan_regulation_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_verbal_plan_regulation_level"),
        "type_of_verbal_plan_regulation",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_verbal_plan_regulation_parent_id"),
        "type_of_verbal_plan_regulation",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_verbal_plan_regulation_short_name"),
        "type_of_verbal_plan_regulation",
        ["short_name"],
        unique=True,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_verbal_plan_regulation_value"),
        "type_of_verbal_plan_regulation",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.add_column(
        "lifecycle_status",
        sa.Column("status", sa.String(), nullable=False),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_lifecycle_status_level"),
        "lifecycle_status",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_lifecycle_status_parent_id"),
        "lifecycle_status",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_codes_lifecycle_status_parent_id"),
        table_name="lifecycle_status",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_lifecycle_status_level"),
        table_name="lifecycle_status",
        schema="codes",
    )
    op.drop_column("lifecycle_status", "status", schema="codes")
    op.drop_index(
        op.f("ix_codes_type_of_verbal_plan_regulation_value"),
        table_name="type_of_verbal_plan_regulation",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_verbal_plan_regulation_short_name"),
        table_name="type_of_verbal_plan_regulation",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_verbal_plan_regulation_parent_id"),
        table_name="type_of_verbal_plan_regulation",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_verbal_plan_regulation_level"),
        table_name="type_of_verbal_plan_regulation",
        schema="codes",
    )
    op.drop_table("type_of_verbal_plan_regulation", schema="codes")
    op.drop_index(
        op.f("ix_codes_type_of_underground_value"),
        table_name="type_of_underground",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_underground_short_name"),
        table_name="type_of_underground",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_underground_parent_id"),
        table_name="type_of_underground",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_underground_level"),
        table_name="type_of_underground",
        schema="codes",
    )
    op.drop_table("type_of_underground", schema="codes")
    op.drop_index(
        op.f("ix_codes_type_of_source_data_value"),
        table_name="type_of_source_data",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_source_data_short_name"),
        table_name="type_of_source_data",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_source_data_parent_id"),
        table_name="type_of_source_data",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_source_data_level"),
        table_name="type_of_source_data",
        schema="codes",
    )
    op.drop_table("type_of_source_data", schema="codes")
    op.drop_index(
        op.f("ix_codes_type_of_plan_regulation_value"),
        table_name="type_of_plan_regulation",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_plan_regulation_short_name"),
        table_name="type_of_plan_regulation",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_plan_regulation_parent_id"),
        table_name="type_of_plan_regulation",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_plan_regulation_level"),
        table_name="type_of_plan_regulation",
        schema="codes",
    )
    op.drop_table("type_of_plan_regulation", schema="codes")
    op.drop_index(
        op.f("ix_codes_type_of_additional_information_value"),
        table_name="type_of_additional_information",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_additional_information_short_name"),
        table_name="type_of_additional_information",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_additional_information_parent_id"),
        table_name="type_of_additional_information",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_additional_information_level"),
        table_name="type_of_additional_information",
        schema="codes",
    )
    op.drop_table("type_of_additional_information", schema="codes")
    op.drop_index(
        op.f("ix_codes_plan_type_value"), table_name="plan_type", schema="codes"
    )
    op.drop_index(
        op.f("ix_codes_plan_type_short_name"), table_name="plan_type", schema="codes"
    )
    op.drop_index(
        op.f("ix_codes_plan_type_parent_id"), table_name="plan_type", schema="codes"
    )
    op.drop_index(
        op.f("ix_codes_plan_type_level"), table_name="plan_type", schema="codes"
    )
    op.drop_table("plan_type", schema="codes")
    # ### end Alembic commands ###
