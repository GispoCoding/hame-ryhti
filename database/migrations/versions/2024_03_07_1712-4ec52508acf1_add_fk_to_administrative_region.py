"""add fk to administrative region

Revision ID: 4ec52508acf1
Revises: ed7ceb2674df
Create Date: 2024-03-07 17:12:11.174295

"""
from typing import Sequence, Union

# import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4ec52508acf1"
down_revision: Union[str, None] = "ed7ceb2674df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "organisation",
        sa.Column("administrative_region_id", sa.UUID(), nullable=False),
        schema="hame",
    )
    op.create_foreign_key(
        "administrative_region_id_fkey",
        "organisation",
        "administrative_region",
        ["administrative_region_id"],
        ["id"],
        source_schema="hame",
        referent_schema="codes",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "administrative_region_id_fkey",
        "organisation",
        schema="hame",
        type_="foreignkey",
    )
    op.drop_column("organisation", "administrative_region_id", schema="hame")
    # ### end Alembic commands ###
