"""trigger updates related to regulation group changes

Revision ID: 5d619f6fd959
Revises: cdc4bdaddb13
Create Date: 2024-11-22 14:54:00.356133

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from alembic_utils.pg_function import PGFunction
from sqlalchemy import text as sql_text

# revision identifiers, used by Alembic.
revision: str = "5d619f6fd959"
down_revision: Union[str, None] = "cdc4bdaddb13"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    hame_trgfunc_plan_plan_regulation_update_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_plan_regulation_update_lifecycle_status()",
        definition="RETURNS TRIGGER AS $$\n            BEGIN\n                UPDATE hame.plan_regulation\n                SET lifecycle_status_id = NEW.lifecycle_status_id\n                WHERE\n                    lifecycle_status_id = OLD.lifecycle_status_id\n                    AND EXISTS ( -- Only update in case of general regulation group\n                        SELECT 1\n                        FROM\n                            hame.plan_regulation_group prg\n                            JOIN codes.type_of_plan_regulation_group tprg\n                                ON prg.type_of_plan_regulation_group_id = tprg.id\n                        WHERE\n                            prg.plan_id = NEW.id\n                            AND prg.id = plan_regulation_group_id\n                            AND tprg.value = 'generalRegulations'\n                    );\n                RETURN NEW;\n            END;\n            $$ language 'plpgsql'",
    )
    op.replace_entity(hame_trgfunc_plan_plan_regulation_update_lifecycle_status)

    hame_trgfunc_plan_plan_proposition_update_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_plan_proposition_update_lifecycle_status()",
        definition="RETURNS TRIGGER AS $$\n            BEGIN\n                UPDATE hame.plan_proposition\n                SET lifecycle_status_id = NEW.lifecycle_status_id\n                WHERE\n                    lifecycle_status_id = OLD.lifecycle_status_id\n                    AND EXISTS ( -- Only update in case of general regulation group\n                        SELECT 1\n                        FROM\n                            hame.plan_regulation_group prg\n                            JOIN codes.type_of_plan_regulation_group tprg\n                                ON prg.type_of_plan_regulation_group_id = tprg.id\n                        WHERE\n                            prg.plan_id = NEW.id\n                            AND prg.id = plan_regulation_group_id\n                            AND tprg.value = 'generalRegulations'\n                    );\n                RETURN NEW;\n            END;\n            $$ language 'plpgsql'",
    )
    op.replace_entity(hame_trgfunc_plan_plan_proposition_update_lifecycle_status)

    hame_trgfunc_plan_regulation_plan_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_plan_new_lifecycle_status()",
        definition="RETURNS TRIGGER AS $$\n            BEGIN\n                NEW.lifecycle_status_id = (\n                    SELECT p.lifecycle_status_id\n                    FROM\n                        hame.plan p\n                        JOIN hame.plan_regulation_group prg\n                            ON p.id = prg.plan_id\n                    WHERE prg.id = NEW.plan_regulation_group_id\n                );\n                RETURN NEW;\n            END;\n            $$ language 'plpgsql'",
    )
    op.replace_entity(hame_trgfunc_plan_regulation_plan_new_lifecycle_status)

    hame_trgfunc_plan_proposition_plan_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_plan_new_lifecycle_status()",
        definition="RETURNS TRIGGER AS $$\n            BEGIN\n                NEW.lifecycle_status_id = (\n                    SELECT p.lifecycle_status_id\n                    FROM\n                        hame.plan p\n                        JOIN hame.plan_regulation_group prg\n                            ON p.id = prg.plan_id\n                    WHERE prg.id = NEW.plan_regulation_group_id\n                );\n                RETURN NEW;\n            END;\n            $$ language 'plpgsql'",
    )
    op.replace_entity(hame_trgfunc_plan_proposition_plan_new_lifecycle_status)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    hame_trgfunc_plan_proposition_plan_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_proposition_plan_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n        DECLARE status_id UUID := (\n            SELECT lifecycle_status_id\n            FROM hame.plan\n            WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n            LIMIT 1\n            );\n        BEGIN\n            IF status_id IS NOT NULL THEN\n                NEW.lifecycle_status_id = status_id;\n            END IF;\n            RETURN NEW;\n        END;\n        $function$",
    )
    op.replace_entity(hame_trgfunc_plan_proposition_plan_new_lifecycle_status)
    hame_trgfunc_plan_regulation_plan_new_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_regulation_plan_new_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n        DECLARE status_id UUID := (\n            SELECT lifecycle_status_id\n            FROM hame.plan\n            WHERE plan_regulation_group_id = NEW.plan_regulation_group_id\n            LIMIT 1\n            );\n        BEGIN\n            IF status_id IS NOT NULL THEN\n                NEW.lifecycle_status_id = status_id;\n            END IF;\n            RETURN NEW;\n        END;\n        $function$",
    )
    op.replace_entity(hame_trgfunc_plan_regulation_plan_new_lifecycle_status)
    hame_trgfunc_plan_plan_proposition_update_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_plan_proposition_update_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n        BEGIN\n            UPDATE hame.plan_proposition\n            SET lifecycle_status_id = NEW.lifecycle_status_id\n            WHERE (plan_regulation_group_id = NEW.plan_regulation_group_id\n            AND lifecycle_status_id = OLD.lifecycle_status_id);\n            RETURN NEW;\n        END;\n        $function$",
    )
    op.replace_entity(hame_trgfunc_plan_plan_proposition_update_lifecycle_status)
    hame_trgfunc_plan_plan_regulation_update_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_plan_regulation_update_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n        BEGIN\n            UPDATE hame.plan_regulation\n            SET lifecycle_status_id = NEW.lifecycle_status_id\n            WHERE (plan_regulation_group_id = NEW.plan_regulation_group_id\n            AND lifecycle_status_id = OLD.lifecycle_status_id);\n            RETURN NEW;\n        END;\n        $function$",
    )
    op.replace_entity(hame_trgfunc_plan_plan_regulation_update_lifecycle_status)
    # ### end Alembic commands ###