"""add_detachment_date_field_to_source_data_table

Revision ID: 0a8a2fecda2a
Revises: f085148de65d
Create Date: 2024-03-07 09:14:40.622499

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# import geoalchemy2


# revision identifiers, used by Alembic.
revision: str = "0a8a2fecda2a"
down_revision: Union[str, None] = "4ec52508acf1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "source_data",
        sa.Column("detachment_date", sa.DateTime(), nullable=False),
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("source_data", "detachment_date", schema="hame")
    # ### end Alembic commands ###
