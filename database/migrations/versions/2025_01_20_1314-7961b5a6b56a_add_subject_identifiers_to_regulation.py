"""add subject identifiers to regulation

Revision ID: 7961b5a6b56a
Revises: 8cb0b42e7a5c
Create Date: 2025-01-20 13:14:02.864548

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7961b5a6b56a"
down_revision: Union[str, None] = "8cb0b42e7a5c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "plan_regulation",
        sa.Column(
            "subject_identifiers",
            sa.ARRAY(sa.TEXT()),
            server_default="{}",
            nullable=False,
        ),
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("plan_regulation", "subject_identifiers", schema="hame")
    # ### end Alembic commands ###
