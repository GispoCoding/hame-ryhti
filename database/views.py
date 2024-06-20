from alembic_utils.pg_view import PGView
from triggers import plan_object_tables


def generate_plan_object_views():
    view_list = []
    for table in plan_object_tables:
        view_name = f"{table}_view"
        view_name = PGView(
            schema="hame",
            signature=f"{table}_view",
            definition=f"""
            SELECT {table}.id,
            {table}.geom,
            prg.name AS otsikko,
            {table}.ordering AS kohdenumero,
            {table}.description AS kuvaus,
            prg.short_name AS kirjaintunnus,
            jsonb_agg(jsonb_build_object('Kaavamääräyslaji', jsonb_build_object('Lajinimi', topr.name,
            'Sanallinen määräys', tovpr.name, 'Numeerinen arvo', pr.numeric_value, 'Mittayksikkö', pr.unit,
            'Määräyksen sisällön kuvaus', pr.text_value, 'Aihetunniste', pr.name, 'Käyttötarkoitus', toai_kt.name,
            'Olemassaolo', toai_oo.name, 'Tyyppi', toai_t.name, 'Eri tahojen tarpeisiin varaus', toai_ettv.name,
            'Merkittävyys', toai_m.name, 'Kehittäminen', toai_k.name, 'Häiriön torjuntatarve', toai_htt.name,
            'Rakentamisen ohjaus', toai_ro.name))) AS "kaavamääräykset"
            FROM hame.{table}
            LEFT JOIN hame.plan_regulation_group prg ON {table}.plan_regulation_group_id = prg.id
            JOIN hame.plan_regulation pr ON prg.id = pr.plan_regulation_group_id
            LEFT JOIN codes.type_of_additional_information toai_kt
            ON toai_kt.id = pr.intended_use_id AND toai_kt.parent_id = '56ab60f0-ce20-4efa-a597-16019eb104ae'::uuid
            LEFT JOIN codes.type_of_additional_information toai_oo
            ON toai_oo.id = pr.existence_id AND toai_oo.parent_id = '80c86df0-568c-4a91-a3a5-7d181e33dbcc'::uuid
            LEFT JOIN codes.type_of_additional_information toai_t
            ON toai_t.id = pr.regulation_type_additional_information_id AND toai_t.parent_id = '94ad30a5-9239-4e69-8aac-907e29384ef1'::uuid
            LEFT JOIN codes.type_of_additional_information toai_ettv
            ON toai_ettv.id = pr.reservation_id AND toai_ettv.parent_id = 'd4c03c5b-08f1-40f7-9d92-11ac48018a10'::uuid
            LEFT JOIN codes.type_of_additional_information toai_m
            ON toai_m.id = pr.significance_id AND toai_m.parent_id = '1d411331-9b17-41fd-8250-db0fac531f28'::uuid
            LEFT JOIN codes.type_of_additional_information toai_k
            ON toai_k.id = pr.development_id AND toai_k.parent_id = '65fcd4f5-2064-4712-a70c-f2070f572170'::uuid
            LEFT JOIN codes.type_of_additional_information toai_htt
            ON toai_htt.id = pr.disturbance_prevention_id AND toai_htt.parent_id = '2d8f12cb-8fba-48c7-9658-e43b5450e3c5'::uuid
            LEFT JOIN codes.type_of_additional_information toai_ro
            ON toai_ro.id = pr.construction_control_id AND toai_ro.parent_id = 'fb7b0208-4ebe-4d8f-9b65-6685ad207179'::uuid
            LEFT JOIN codes.type_of_plan_regulation topr ON pr.type_of_plan_regulation_id = topr.id
            LEFT JOIN codes.plan_theme pt ON pr.plan_theme_id = pt.id
            LEFT JOIN codes.type_of_verbal_plan_regulation tovpr
            ON pr.type_of_verbal_plan_regulation_id = tovpr.id
            GROUP BY {table}.id, prg.name, prg.short_name;
            """,  # Noqa: E501
        )
        view_list.append(view_name)
    return view_list
