"""move_name_field_into_planbase_class

Revision ID: f085148de65d
Revises: ad29908c50ad
Create Date: 2024-02-29 12:18:32.513624

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f085148de65d"
down_revision: Union[str, None] = "ad29908c50ad"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "plan_proposition",
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        schema="hame",
    )
    op.add_column(
        "plan_regulation",
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("plan_regulation", "name", schema="hame")
    op.drop_column("plan_proposition", "name", schema="hame")
    # ### end Alembic commands ###
