"""document fields up to date

Revision ID: 93fbc9d51ec3
Revises: e5babb0f7594
Create Date: 2024-12-10 14:15:58.616137

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "93fbc9d51ec3"
down_revision: Union[str, None] = "e5babb0f7594"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "language",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), server_default="", nullable=False),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column(
            "description",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("level", sa.Integer(), server_default="1", nullable=False),
        sa.Column("parent_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column(
            "id",
            sa.UUID(as_uuid=False),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["codes.language.id"],
            name="language_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_language_level"),
        "language",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_language_parent_id"),
        "language",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_language_short_name"),
        "language",
        ["short_name"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_language_value"),
        "language",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.create_table(
        "personal_data_content",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), server_default="", nullable=False),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column(
            "description",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("level", sa.Integer(), server_default="1", nullable=False),
        sa.Column("parent_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column(
            "id",
            sa.UUID(as_uuid=False),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["codes.personal_data_content.id"],
            name="personal_data_content_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_personal_data_content_level"),
        "personal_data_content",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_personal_data_content_parent_id"),
        "personal_data_content",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_personal_data_content_short_name"),
        "personal_data_content",
        ["short_name"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_personal_data_content_value"),
        "personal_data_content",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.create_table(
        "retention_time",
        sa.Column("value", sa.String(), nullable=False),
        sa.Column("short_name", sa.String(), server_default="", nullable=False),
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column(
            "description",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("level", sa.Integer(), server_default="1", nullable=False),
        sa.Column("parent_id", sa.UUID(as_uuid=False), nullable=True),
        sa.Column(
            "id",
            sa.UUID(as_uuid=False),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "modified_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["codes.retention_time.id"],
            name="retention_time_parent_id_fkey",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_retention_time_level"),
        "retention_time",
        ["level"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_retention_time_parent_id"),
        "retention_time",
        ["parent_id"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_retention_time_short_name"),
        "retention_time",
        ["short_name"],
        unique=False,
        schema="codes",
    )
    op.create_index(
        op.f("ix_codes_retention_time_value"),
        "retention_time",
        ["value"],
        unique=True,
        schema="codes",
    )
    op.add_column(
        "document",
        sa.Column("personal_data_content_id", sa.UUID(as_uuid=False), nullable=False),
        schema="hame",
    )
    op.add_column(
        "document",
        sa.Column("retention_time_id", sa.UUID(as_uuid=False), nullable=False),
        schema="hame",
    )
    op.add_column(
        "document",
        sa.Column("language_id", sa.UUID(as_uuid=False), nullable=False),
        schema="hame",
    )
    op.add_column(
        "document",
        sa.Column("exported_at", sa.TIMESTAMP(timezone=True), nullable=True),
        schema="hame",
    )
    op.add_column(
        "document",
        sa.Column("exported_file_key", sa.UUID(as_uuid=False), nullable=True),
        schema="hame",
    )
    op.add_column(
        "document",
        sa.Column("arrival_date", sa.TIMESTAMP(timezone=True), nullable=True),
        schema="hame",
    )
    op.add_column(
        "document",
        sa.Column("confirmation_date", sa.TIMESTAMP(timezone=True), nullable=True),
        schema="hame",
    )
    op.add_column(
        "document",
        sa.Column("document_date", sa.TIMESTAMP(timezone=True), nullable=False),
        schema="hame",
    )
    op.drop_column("document", "name", schema="hame")
    op.add_column(
        "document",
        sa.Column(
            "name",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default='{"fin": "", "swe": "", "eng": ""}',
            nullable=False,
        ),
        schema="hame",
    )
    op.alter_column(
        "document",
        "decision_date",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=None,
        existing_nullable=True,
        schema="hame",
    )
    op.create_foreign_key(
        "language_id_fkey",
        "document",
        "language",
        ["language_id"],
        ["id"],
        source_schema="hame",
        referent_schema="codes",
    )
    op.create_foreign_key(
        "retention_time_id_fkey",
        "document",
        "retention_time",
        ["retention_time_id"],
        ["id"],
        source_schema="hame",
        referent_schema="codes",
    )
    op.create_foreign_key(
        "personal_data_content_id_fkey",
        "document",
        "personal_data_content",
        ["personal_data_content_id"],
        ["id"],
        source_schema="hame",
        referent_schema="codes",
    )
    op.drop_column("document", "language", schema="hame")
    op.drop_column("document", "personal_details", schema="hame")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "document",
        sa.Column(
            "personal_details",
            sa.VARCHAR(),
            autoincrement=False,
            nullable=False,
        ),
        schema="hame",
    )
    op.add_column(
        "document",
        sa.Column("language", sa.VARCHAR(), autoincrement=False, nullable=False),
        schema="hame",
    )
    op.drop_constraint(
        "personal_data_content_id_fkey",
        "document",
        schema="hame",
        type_="foreignkey",
    )
    op.drop_constraint(
        "retention_time_id_fkey", "document", schema="hame", type_="foreignkey"
    )
    op.drop_constraint(
        "language_id_fkey", "document", schema="hame", type_="foreignkey"
    )
    op.alter_column(
        "document",
        "decision_date",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        server_default=sa.text("now()"),
        existing_nullable=True,
        schema="hame",
    )
    op.alter_column(
        "document",
        "name",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        server_default=None,
        type_=sa.VARCHAR(),
        existing_nullable=False,
        schema="hame",
    )
    op.drop_column("document", "document_date", schema="hame")
    op.drop_column("document", "confirmation_date", schema="hame")
    op.drop_column("document", "arrival_date", schema="hame")
    op.drop_column("document", "exported_file_key", schema="hame")
    op.drop_column("document", "exported_at", schema="hame")
    op.drop_column("document", "language_id", schema="hame")
    op.drop_column("document", "retention_time_id", schema="hame")
    op.drop_column("document", "personal_data_content_id", schema="hame")
    op.drop_index(
        op.f("ix_codes_retention_time_value"),
        table_name="retention_time",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_retention_time_short_name"),
        table_name="retention_time",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_retention_time_parent_id"),
        table_name="retention_time",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_retention_time_level"),
        table_name="retention_time",
        schema="codes",
    )
    op.drop_table("retention_time", schema="codes")
    op.drop_index(
        op.f("ix_codes_personal_data_content_value"),
        table_name="personal_data_content",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_personal_data_content_short_name"),
        table_name="personal_data_content",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_personal_data_content_parent_id"),
        table_name="personal_data_content",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_personal_data_content_level"),
        table_name="personal_data_content",
        schema="codes",
    )
    op.drop_table("personal_data_content", schema="codes")
    op.drop_index(
        op.f("ix_codes_language_value"), table_name="language", schema="codes"
    )
    op.drop_index(
        op.f("ix_codes_language_short_name"),
        table_name="language",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_language_parent_id"),
        table_name="language",
        schema="codes",
    )
    op.drop_index(
        op.f("ix_codes_language_level"), table_name="language", schema="codes"
    )
    op.drop_table("language", schema="codes")
    # ### end Alembic commands ###