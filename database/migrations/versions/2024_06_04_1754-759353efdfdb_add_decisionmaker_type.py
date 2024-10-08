"""add decisionmaker type

Revision ID: 759353efdfdb
Revises: c84f695b3d22
Create Date: 2024-06-04 17:54:58.513232

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "759353efdfdb"
down_revision: Union[str, None] = "c84f695b3d22"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "type_of_decision_maker",
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
            ["codes.type_of_decision_maker.id"],
            name="type_of_decision_maker_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_decision_maker_level"),
        "type_of_decision_maker",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_decision_maker_parent_id"),
        "type_of_decision_maker",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_decision_maker_short_name"),
        "type_of_decision_maker",
        ["short_name"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_type_of_decision_maker_value"),
        "type_of_decision_maker",
        ["value"],
        unique=True,
        schema="codes",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_codes_type_of_decision_maker_value"),
        table_name="type_of_decision_maker",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_decision_maker_short_name"),
        table_name="type_of_decision_maker",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_decision_maker_parent_id"),
        table_name="type_of_decision_maker",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_type_of_decision_maker_level"),
        table_name="type_of_decision_maker",
        schema="codes",
    )
    op.drop_table("type_of_decision_maker", schema="codes")
    # ### end Alembic commands ###
