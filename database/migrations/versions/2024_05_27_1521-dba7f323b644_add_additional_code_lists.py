"""add_additional_code_lists

Revision ID: dba7f323b644
Revises: 1d702fe0daf2
Create Date: 2024-05-27 15:21:28.291526

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "dba7f323b644"
down_revision: Union[str, None] = "1d702fe0daf2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "category_of_publicity",
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
        sa.Column("parent_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column(
            "id",
            sa.UUID(as_uuid=False),
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
            ["codes.category_of_publicity.id"],
            name="category_of_publicity_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_category_of_publicity_level"),
        "category_of_publicity",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_category_of_publicity_parent_id"),
        "category_of_publicity",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_category_of_publicity_short_name"),
        "category_of_publicity",
        ["short_name"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_category_of_publicity_value"),
        "category_of_publicity",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.create_table(
        "name_of_plan_case_decision",
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
        sa.Column("parent_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column(
            "id",
            sa.UUID(as_uuid=False),
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
            ["codes.name_of_plan_case_decision.id"],
            name="name_of_plan_case_decision_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_name_of_plan_case_decision_level"),
        "name_of_plan_case_decision",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_name_of_plan_case_decision_parent_id"),
        "name_of_plan_case_decision",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_name_of_plan_case_decision_short_name"),
        "name_of_plan_case_decision",
        ["short_name"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_name_of_plan_case_decision_value"),
        "name_of_plan_case_decision",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.create_table(
        "type_of_interaction_event",
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
        sa.Column("parent_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column(
            "id",
            sa.UUID(as_uuid=False),
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
            ["codes.type_of_interaction_event.id"],
            name="type_of_interaction_event_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_interaction_event_level"),
        "type_of_interaction_event",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_interaction_event_parent_id"),
        "type_of_interaction_event",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_interaction_event_short_name"),
        "type_of_interaction_event",
        ["short_name"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_interaction_event_value"),
        "type_of_interaction_event",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.create_table(
        "type_of_processing_event",
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
        sa.Column("parent_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column(
            "id",
            sa.UUID(as_uuid=False),
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
            ["codes.type_of_processing_event.id"],
            name="type_of_processing_event_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_processing_event_level"),
        "type_of_processing_event",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_processing_event_parent_id"),
        "type_of_processing_event",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_processing_event_short_name"),
        "type_of_processing_event",
        ["short_name"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_processing_event_value"),
        "type_of_processing_event",
        ["value"],
        unique=True,
        schema="codes",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_codes_type_of_processing_event_value"),
        table_name="type_of_processing_event",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_processing_event_short_name"),
        table_name="type_of_processing_event",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_processing_event_parent_id"),
        table_name="type_of_processing_event",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_processing_event_level"),
        table_name="type_of_processing_event",
        schema="codes",
    )
    op.drop_table("type_of_processing_event", schema="codes")
    op.drop_index(
        op.f("ix_codes_type_of_interaction_event_value"),
        table_name="type_of_interaction_event",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_interaction_event_short_name"),
        table_name="type_of_interaction_event",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_interaction_event_parent_id"),
        table_name="type_of_interaction_event",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_interaction_event_level"),
        table_name="type_of_interaction_event",
        schema="codes",
    )
    op.drop_table("type_of_interaction_event", schema="codes")
    op.drop_index(
        op.f("ix_codes_name_of_plan_case_decision_value"),
        table_name="name_of_plan_case_decision",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_name_of_plan_case_decision_short_name"),
        table_name="name_of_plan_case_decision",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_name_of_plan_case_decision_parent_id"),
        table_name="name_of_plan_case_decision",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_name_of_plan_case_decision_level"),
        table_name="name_of_plan_case_decision",
        schema="codes",
    )
    op.drop_table("name_of_plan_case_decision", schema="codes")
    op.drop_index(
        op.f("ix_codes_category_of_publicity_value"),
        table_name="category_of_publicity",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_category_of_publicity_short_name"),
        table_name="category_of_publicity",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_category_of_publicity_parent_id"),
        table_name="category_of_publicity",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_category_of_publicity_level"),
        table_name="category_of_publicity",
        schema="codes",
    )
    op.drop_table("category_of_publicity", schema="codes")
    # ### end Alembic commands ###
