"""add_organisation_table

Revision ID: 57815edcbeeb
Revises: f90c256163dd
Create Date: 2024-02-22 14:42:09.725658

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "57815edcbeeb"
down_revision: Union[str, None] = "f90c256163dd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "organisation",
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("business_id", sa.String(), nullable=False),
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
    op.add_column(
        "plan", sa.Column("organisation_id", sa.UUID(), nullable=False), schema="hame"
    )
    op.create_foreign_key(
        "organisation_id_fkey",
        "plan",
        "organisation",
        ["organisation_id"],
        ["id"],
        source_schema="hame",
        referent_schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "organisation_id_fkey", "plan", schema="hame", type_="foreignkey"
    )
    op.drop_column("plan", "organisation_id", schema="hame")
    op.drop_table("organisation", schema="hame")
    # ### end Alembic commands ###