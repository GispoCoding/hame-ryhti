"""remove_language_field_from_source_data_table

Revision ID: f90c256163dd
Revises: 194b9836f0a0
Create Date: 2024-02-22 11:45:58.388376

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f90c256163dd"
down_revision: Union[str, None] = "194b9836f0a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("source_data", "language", schema="hame")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "source_data",
        sa.Column(
            "language",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text('\'{"eng": "", "fin": "", "swe": ""}\'::jsonb'),
            autoincrement=False,
            nullable=False,
        ),
        schema="hame",
    )
    # ### end Alembic commands ###
