"""add_geometry_validation_triggers

Revision ID: 1d702fe0daf2
Revises: 4f8bcdc437a8
Create Date: 2024-05-23 16:20:37.037611

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from sqlalchemy import text as sql_text

# revision identifiers, used by Alembic.
revision: str = "1d702fe0daf2"
down_revision: Union[str, None] = "0da11d97b6cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    hame_trgfunc_validate_polygon_geometry = PGFunction(
        schema="hame",
        signature="trgfunc_validate_polygon_geometry()",
        definition="RETURNS TRIGGER AS $$\n    BEGIN\n        IF NOT ST_IsValid(NEW.geom) THEN\n            RAISE EXCEPTION 'Invalid geometry. Must follow OGC rules.';\n        END IF;\n        RETURN NEW;\n    END;\n    $$ language 'plpgsql'",
    )
    op.create_entity(hame_trgfunc_validate_polygon_geometry)

    hame_trgfunc_line_validate_geometry = PGFunction(
        schema="hame",
        signature="trgfunc_line_validate_geometry()",
        definition="RETURNS TRIGGER AS $$\n    BEGIN\n        IF NOT ST_IsSimple(NEW.geom) THEN\n            RAISE EXCEPTION 'Invalid geometry. Must not intersect itself.';\n        END IF;\n        RETURN NEW;\n    END;\n    $$ language 'plpgsql'",
    )
    op.create_entity(hame_trgfunc_line_validate_geometry)

    hame_trgfunc_other_area_insert_intersecting_geometries = PGFunction(
        schema="hame",
        signature="trgfunc_other_area_insert_intersecting_geometries()",
        definition="RETURNS TRIGGER AS $$\n    BEGIN\n        -- Check if the new entry has id of a plan_regulation_group\n        -- which has id of a plan_regulation that has intended_use_id\n        -- that equals to 'paakayttotarkoitus'\n        IF EXISTS (\n            SELECT 1\n            FROM hame.plan_regulation_group prg\n            JOIN hame.plan_regulation pr ON pr.plan_regulation_group_id = prg.id\n            JOIN codes.type_of_additional_information tai ON tai.id = pr.intended_use_id\n            WHERE tai.value = 'paakayttotarkoitus'\n            AND prg.id = NEW.plan_regulation_group_id\n        ) THEN\n            -- check if there already is an entry in other_area table with the same\n            -- plan_regulation_group that the new geometry intersects\n            IF EXISTS (\n                SELECT 1\n                FROM hame.other_area oa\n                WHERE oa.plan_regulation_group_id = NEW.plan_regulation_group_id\n                AND ST_Intersects(oa.geom, NEW.geom)\n            ) THEN\n                RAISE EXCEPTION 'New entry intersects with existing entry, both with\n                intended_use of paakayttotarkoitus';\n            END IF;\n        END IF;\n\n        RETURN NEW;\n    END;\n    $$ language 'plpgsql'",
    )
    op.create_entity(hame_trgfunc_other_area_insert_intersecting_geometries)

    hame_land_use_area_trg_land_use_area_validate_polygon_geometry = PGTrigger(
        schema="hame",
        signature="trg_land_use_area_validate_polygon_geometry",
        on_entity="hame.land_use_area",
        is_constraint=False,
        definition="BEFORE INSERT OR UPDATE ON land_use_area\n        FOR EACH ROW\n        EXECUTE FUNCTION hame.trgfunc_validate_polygon_geometry()",
    )
    op.create_entity(hame_land_use_area_trg_land_use_area_validate_polygon_geometry)

    hame_other_area_trg_other_area_validate_polygon_geometry = PGTrigger(
        schema="hame",
        signature="trg_other_area_validate_polygon_geometry",
        on_entity="hame.other_area",
        is_constraint=False,
        definition="BEFORE INSERT OR UPDATE ON other_area\n        FOR EACH ROW\n        EXECUTE FUNCTION hame.trgfunc_validate_polygon_geometry()",
    )
    op.create_entity(hame_other_area_trg_other_area_validate_polygon_geometry)

    hame_plan_trg_plan_validate_polygon_geometry = PGTrigger(
        schema="hame",
        signature="trg_plan_validate_polygon_geometry",
        on_entity="hame.plan",
        is_constraint=False,
        definition="BEFORE INSERT OR UPDATE ON plan\n        FOR EACH ROW\n        EXECUTE FUNCTION hame.trgfunc_validate_polygon_geometry()",
    )
    op.create_entity(hame_plan_trg_plan_validate_polygon_geometry)

    hame_line_trg_line_validate_geometry = PGTrigger(
        schema="hame",
        signature="trg_line_validate_geometry",
        on_entity="hame.line",
        is_constraint=False,
        definition="BEFORE INSERT OR UPDATE ON line\n    FOR EACH ROW\n    EXECUTE FUNCTION hame.trgfunc_line_validate_geometry()",
    )
    op.create_entity(hame_line_trg_line_validate_geometry)

    hame_other_area_trg_other_area_insert_intersecting_geometries = PGTrigger(
        schema="hame",
        signature="trg_other_area_insert_intersecting_geometries",
        on_entity="hame.other_area",
        is_constraint=False,
        definition="BEFORE INSERT ON other_area\n    FOR EACH ROW\n    EXECUTE FUNCTION hame.trgfunc_other_area_insert_intersecting_geometries()",
    )
    op.create_entity(hame_other_area_trg_other_area_insert_intersecting_geometries)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    hame_other_area_trg_other_area_insert_intersecting_geometries = PGTrigger(
        schema="hame",
        signature="trg_other_area_insert_intersecting_geometries",
        on_entity="hame.other_area",
        is_constraint=False,
        definition="BEFORE INSERT ON other_area\n    FOR EACH ROW\n    EXECUTE FUNCTION hame.trgfunc_other_area_insert_intersecting_geometries()",
    )
    op.drop_entity(hame_other_area_trg_other_area_insert_intersecting_geometries)

    hame_line_trg_line_validate_geometry = PGTrigger(
        schema="hame",
        signature="trg_line_validate_geometry",
        on_entity="hame.line",
        is_constraint=False,
        definition="BEFORE INSERT OR UPDATE ON line\n    FOR EACH ROW\n    EXECUTE FUNCTION hame.trgfunc_line_validate_geometry()",
    )
    op.drop_entity(hame_line_trg_line_validate_geometry)

    hame_plan_trg_plan_validate_polygon_geometry = PGTrigger(
        schema="hame",
        signature="trg_plan_validate_polygon_geometry",
        on_entity="hame.plan",
        is_constraint=False,
        definition="BEFORE INSERT OR UPDATE ON plan\n        FOR EACH ROW\n        EXECUTE FUNCTION hame.trgfunc_validate_polygon_geometry()",
    )
    op.drop_entity(hame_plan_trg_plan_validate_polygon_geometry)

    hame_other_area_trg_other_area_validate_polygon_geometry = PGTrigger(
        schema="hame",
        signature="trg_other_area_validate_polygon_geometry",
        on_entity="hame.other_area",
        is_constraint=False,
        definition="BEFORE INSERT OR UPDATE ON other_area\n        FOR EACH ROW\n        EXECUTE FUNCTION hame.trgfunc_validate_polygon_geometry()",
    )
    op.drop_entity(hame_other_area_trg_other_area_validate_polygon_geometry)

    hame_land_use_area_trg_land_use_area_validate_polygon_geometry = PGTrigger(
        schema="hame",
        signature="trg_land_use_area_validate_polygon_geometry",
        on_entity="hame.land_use_area",
        is_constraint=False,
        definition="BEFORE INSERT OR UPDATE ON land_use_area\n        FOR EACH ROW\n        EXECUTE FUNCTION hame.trgfunc_validate_polygon_geometry()",
    )
    op.drop_entity(hame_land_use_area_trg_land_use_area_validate_polygon_geometry)

    hame_trgfunc_other_area_insert_intersecting_geometries = PGFunction(
        schema="hame",
        signature="trgfunc_other_area_insert_intersecting_geometries()",
        definition="RETURNS TRIGGER AS $$\n    BEGIN\n        -- Check if the new entry has id of a plan_regulation_group\n        -- which has id of a plan_regulation that has intended_use_id\n        -- that equals to 'paakayttotarkoitus'\n        IF EXISTS (\n            SELECT 1\n            FROM hame.plan_regulation_group prg\n            JOIN hame.plan_regulation pr ON pr.plan_regulation_group_id = prg.id\n            JOIN codes.type_of_additional_information tai ON tai.id = pr.intended_use_id\n            WHERE tai.value = 'paakayttotarkoitus'\n            AND prg.id = NEW.plan_regulation_group_id\n        ) THEN\n            -- check if there already is an entry in other_area table with the same\n            -- plan_regulation_group that the new geometry intersects\n            IF EXISTS (\n                SELECT 1\n                FROM hame.other_area oa\n                WHERE oa.plan_regulation_group_id = NEW.plan_regulation_group_id\n                AND ST_Intersects(oa.geom, NEW.geom)\n            ) THEN\n                RAISE EXCEPTION 'New entry intersects with existing entry, both with\n                intended_use of paakayttotarkoitus';\n            END IF;\n        END IF;\n\n        RETURN NEW;\n    END;\n    $$ language 'plpgsql'",
    )
    op.drop_entity(hame_trgfunc_other_area_insert_intersecting_geometries)

    hame_trgfunc_line_validate_geometry = PGFunction(
        schema="hame",
        signature="trgfunc_line_validate_geometry()",
        definition="RETURNS TRIGGER AS $$\n    BEGIN\n        IF NOT ST_IsSimple(NEW.geom) THEN\n            RAISE EXCEPTION 'Invalid geometry. Must not intersect itself.';\n        END IF;\n        RETURN NEW;\n    END;\n    $$ language 'plpgsql'",
    )
    op.drop_entity(hame_trgfunc_line_validate_geometry)

    hame_trgfunc_validate_polygon_geometry = PGFunction(
        schema="hame",
        signature="trgfunc_validate_polygon_geometry()",
        definition="RETURNS TRIGGER AS $$\n    BEGIN\n        IF NOT ST_IsValid(NEW.geom) THEN\n            RAISE EXCEPTION 'Invalid geometry. Must follow OGC rules.';\n        END IF;\n        RETURN NEW;\n    END;\n    $$ language 'plpgsql'",
    )
    op.drop_entity(hame_trgfunc_validate_polygon_geometry)

    # ### end Alembic commands ###
