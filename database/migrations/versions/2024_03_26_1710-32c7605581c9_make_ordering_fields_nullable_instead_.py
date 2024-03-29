"""make ordering fields nullable instead of autoincrement

Revision ID: 32c7605581c9
Revises: 749c61b91749
Create Date: 2024-03-26 17:10:05.686612

"""
from typing import Sequence, Union

# import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "32c7605581c9"
down_revision: Union[str, None] = "c8cbaef12e3e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "land_use_area",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=True,
        schema="hame",
    )
    op.alter_column(
        "land_use_point",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=True,
        schema="hame",
    )
    op.alter_column(
        "line",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=True,
        schema="hame",
    )
    op.alter_column(
        "other_area",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=True,
        schema="hame",
    )
    op.alter_column(
        "other_point",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=True,
        schema="hame",
    )
    op.alter_column(
        "plan_proposition",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=True,
        schema="hame",
    )
    op.alter_column(
        "plan_regulation",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=True,
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "plan_regulation",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=False,
        schema="hame",
    )
    op.alter_column(
        "plan_proposition",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=False,
        schema="hame",
    )
    op.alter_column(
        "other_point",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=False,
        schema="hame",
    )
    op.alter_column(
        "other_area",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=False,
        schema="hame",
    )
    op.alter_column(
        "line",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=False,
        schema="hame",
    )
    op.alter_column(
        "land_use_point",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=False,
        schema="hame",
    )
    op.alter_column(
        "land_use_area",
        "ordering",
        existing_type=sa.INTEGER(),
        nullable=False,
        schema="hame",
    )
    # ### end Alembic commands ###
