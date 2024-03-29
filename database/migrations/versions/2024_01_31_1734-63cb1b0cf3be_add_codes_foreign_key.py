"""add codes foreign key

Revision ID: 63cb1b0cf3be
Revises: 5310a8b157f0
Create Date: 2024-01-31 17:34:58.842914

"""
from typing import Sequence, Union

# import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "63cb1b0cf3be"
down_revision: Union[str, None] = "5310a8b157f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "plan",
        sa.Column("lifecycle_status_id", sa.UUID(), nullable=False),
        schema="hame",
    )
    op.create_foreign_key(
        "plan_lifecycle_status_id_fkey",
        "plan",
        "lifecycle_status",
        ["lifecycle_status_id"],
        ["id"],
        source_schema="hame",
        referent_schema="codes",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "plan_lifecycle_status_id_fkey", "plan", schema="hame", type_="foreignkey"
    )
    op.drop_column("plan", "lifecycle_status_id", schema="hame")
    # ### end Alembic commands ###
