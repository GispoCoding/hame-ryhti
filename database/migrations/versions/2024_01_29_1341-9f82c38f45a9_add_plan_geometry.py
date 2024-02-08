"""add plan geometry

Revision ID: 9f82c38f45a9
Revises: 6592d88a81df
Create Date: 2024-01-29 13:41:44.839255

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9f82c38f45a9"
down_revision: Union[str, None] = "6592d88a81df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "plan",
        sa.Column(
            "geom",
            geoalchemy2.types.Geometry(
                geometry_type="POLYGON",
                srid=3067,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                nullable=False,
            ),
            nullable=False,
        ),
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("plan", "geom", schema="hame")
    # ### end Alembic commands ###