"""add_plan_regulation_group_table

Revision ID: c882368ce708
Revises: 84c37bffeca0
Create Date: 2024-02-05 18:07:16.739686

"""
from typing import Sequence, Union

# import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c882368ce708"
down_revision: Union[str, None] = "84c37bffeca0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "plan_regulation_group",
        sa.Column("short_name", sa.String(), nullable=False),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
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
        sa.PrimaryKeyConstraint("id"),
        schema="hame",
    )
    op.create_index(
        op.f("ix_hame_plan_regulation_group_short_name"),
        "plan_regulation_group",
        ["short_name"],
        unique=True,
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_hame_plan_regulation_group_short_name"),
        table_name="plan_regulation_group",
        schema="hame",
    )
    op.drop_table("plan_regulation_group", schema="hame")
    # ### end Alembic commands ###