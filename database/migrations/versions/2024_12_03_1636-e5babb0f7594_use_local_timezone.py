"""use local timezone

Revision ID: e5babb0f7594
Revises: 626124880789
Create Date: 2024-12-03 16:36:04.054913

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "e5babb0f7594"
down_revision: Union[str, None] = "e9a045c08304"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "administrative_region",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "administrative_region",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "category_of_publicity",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "category_of_publicity",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "lifecycle_status",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "lifecycle_status",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "name_of_plan_case_decision",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "name_of_plan_case_decision",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "plan_theme",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "plan_theme",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "plan_type",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "plan_type",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_additional_information",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_additional_information",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_decision_maker",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_decision_maker",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_document",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_document",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_interaction_event",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_interaction_event",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_plan_regulation",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_plan_regulation",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_plan_regulation_group",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_plan_regulation_group",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_processing_event",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_processing_event",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_source_data",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_source_data",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_underground",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_underground",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_verbal_plan_regulation",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_verbal_plan_regulation",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "document",
        "decision_date",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "document",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "document",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "land_use_area",
        "exported_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "land_use_area",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "land_use_area",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "land_use_point",
        "exported_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "land_use_point",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "land_use_point",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "lifecycle_date",
        "starting_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "lifecycle_date",
        "ending_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "lifecycle_date",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "lifecycle_date",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "line",
        "exported_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "line",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "line",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "organisation",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "organisation",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "other_area",
        "exported_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "other_area",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "other_area",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "other_point",
        "exported_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "other_point",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "other_point",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan",
        "validated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "plan",
        "exported_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "plan",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_proposition",
        "exported_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "plan_proposition",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_proposition",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_regulation",
        "exported_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "plan_regulation",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_regulation",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_regulation_group",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_regulation_group",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "source_data",
        "detachment_date",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        schema="hame",
    )
    op.alter_column(
        "source_data",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "source_data",
        "modified_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "source_data",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "source_data",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "source_data",
        "detachment_date",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        schema="hame",
    )
    op.alter_column(
        "plan_regulation_group",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_regulation_group",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_regulation",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_regulation",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_regulation",
        "exported_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "plan_proposition",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_proposition",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan_proposition",
        "exported_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "plan",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "plan",
        "exported_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "plan",
        "validated_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "other_point",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "other_point",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "other_point",
        "exported_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "other_area",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "other_area",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "other_area",
        "exported_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "organisation",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "organisation",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "line",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "line",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "line",
        "exported_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "lifecycle_date",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "lifecycle_date",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "lifecycle_date",
        "ending_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "lifecycle_date",
        "starting_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "land_use_point",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "land_use_point",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "land_use_point",
        "exported_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "land_use_area",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "land_use_area",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "land_use_area",
        "exported_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "document",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "document",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "document",
        "decision_date",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        existing_server_default=sa.text("now()"),
        schema="hame",
    )
    op.alter_column(
        "type_of_verbal_plan_regulation",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_verbal_plan_regulation",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_underground",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_underground",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_source_data",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_source_data",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_processing_event",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_processing_event",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_plan_regulation_group",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_plan_regulation_group",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_plan_regulation",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_plan_regulation",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_interaction_event",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_interaction_event",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_document",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_document",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_decision_maker",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_decision_maker",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_additional_information",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "type_of_additional_information",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "plan_type",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "plan_type",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "plan_theme",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "plan_theme",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "name_of_plan_case_decision",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "name_of_plan_case_decision",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "lifecycle_status",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "lifecycle_status",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "category_of_publicity",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "category_of_publicity",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "administrative_region",
        "modified_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    op.alter_column(
        "administrative_region",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
        schema="codes",
    )
    # ### end Alembic commands ###
