"""triggers, update regulation lifecycle after plan

Revision ID: 4e3c0868ea98
Revises: 385ba899bb2e
Create Date: 2024-11-27 14:50:27.178556

"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from alembic_utils.pg_function import PGFunction
from sqlalchemy import text as sql_text

# revision identifiers, used by Alembic.
revision: str = "4e3c0868ea98"
down_revision: Union[str, None] = "385ba899bb2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    hame_trgfunc_plan_plan_regulation_update_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_plan_regulation_update_lifecycle_status()",
        definition="RETURNS TRIGGER AS $$\n            BEGIN\n                UPDATE hame.plan_regulation rt\n                SET lifecycle_status_id = NEW.lifecycle_status_id\n                WHERE\n                    EXISTS (\n                        SELECT 1\n                        FROM hame.plan_regulation_group prg\n                        WHERE\n                            prg.id = rt.plan_regulation_group_id\n                            AND prg.plan_id = NEW.id\n                    )\n                    AND lifecycle_status_id = OLD.lifecycle_status_id\n                ;\n                RETURN NEW;\n            END;\n            $$ language 'plpgsql'",
    )
    op.replace_entity(hame_trgfunc_plan_plan_regulation_update_lifecycle_status)

    hame_trgfunc_plan_plan_proposition_update_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_plan_proposition_update_lifecycle_status()",
        definition="RETURNS TRIGGER AS $$\n            BEGIN\n                UPDATE hame.plan_proposition rt\n                SET lifecycle_status_id = NEW.lifecycle_status_id\n                WHERE\n                    EXISTS (\n                        SELECT 1\n                        FROM hame.plan_regulation_group prg\n                        WHERE\n                            prg.id = rt.plan_regulation_group_id\n                            AND prg.plan_id = NEW.id\n                    )\n                    AND lifecycle_status_id = OLD.lifecycle_status_id\n                ;\n                RETURN NEW;\n            END;\n            $$ language 'plpgsql'",
    )
    op.replace_entity(hame_trgfunc_plan_plan_proposition_update_lifecycle_status)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    hame_trgfunc_plan_plan_proposition_update_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_plan_proposition_update_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            BEGIN\n                UPDATE hame.plan_proposition\n                SET lifecycle_status_id = NEW.lifecycle_status_id\n                WHERE\n                    lifecycle_status_id = OLD.lifecycle_status_id\n                    AND EXISTS ( -- Only update in case of general regulation group\n                        SELECT 1\n                        FROM\n                            hame.plan_regulation_group prg\n                            JOIN codes.type_of_plan_regulation_group tprg\n                                ON prg.type_of_plan_regulation_group_id = tprg.id\n                        WHERE\n                            prg.plan_id = NEW.id\n                            AND prg.id = plan_regulation_group_id\n                            AND tprg.value = 'generalRegulations'\n                    );\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.replace_entity(hame_trgfunc_plan_plan_proposition_update_lifecycle_status)
    hame_trgfunc_plan_plan_regulation_update_lifecycle_status = PGFunction(
        schema="hame",
        signature="trgfunc_plan_plan_regulation_update_lifecycle_status()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\n            BEGIN\n                UPDATE hame.plan_regulation\n                SET lifecycle_status_id = NEW.lifecycle_status_id\n                WHERE\n                    lifecycle_status_id = OLD.lifecycle_status_id\n                    AND EXISTS ( -- Only update in case of general regulation group\n                        SELECT 1\n                        FROM\n                            hame.plan_regulation_group prg\n                            JOIN codes.type_of_plan_regulation_group tprg\n                                ON prg.type_of_plan_regulation_group_id = tprg.id\n                        WHERE\n                            prg.plan_id = NEW.id\n                            AND prg.id = plan_regulation_group_id\n                            AND tprg.value = 'generalRegulations'\n                    );\n                RETURN NEW;\n            END;\n            $function$",
    )
    op.replace_entity(hame_trgfunc_plan_plan_regulation_update_lifecycle_status)
    # ### end Alembic commands ###