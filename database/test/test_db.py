import os

import psycopg2

from .conftest import assert_database_is_alright, hame_count


def test_database_creation(main_db_params_with_root_user, hame_database_created):
    conn = psycopg2.connect(**main_db_params_with_root_user)
    try:
        with conn.cursor() as cur:
            assert_database_is_alright(cur)

            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_name='alembic_version'"
            )
            assert cur.fetchall() == [("alembic_version",)]

            cur.execute("SELECT version_num FROM alembic_version")
            assert cur.fetchall() == [(hame_database_created,)]

    finally:
        conn.close()


def test_database_all_migrations(main_db_params_with_root_user, hame_database_migrated):
    conn = psycopg2.connect(**main_db_params_with_root_user)
    try:
        with conn.cursor() as cur:
            assert_database_is_alright(cur)

            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_name='alembic_version'"
            )
            assert cur.fetchall() == [("alembic_version",)]

            cur.execute("SELECT version_num FROM alembic_version")
            assert cur.fetchall() == [(hame_database_migrated,)]

    finally:
        conn.close()


def test_database_migrations_up_to_date(autogenerated_migration):
    assert not autogenerated_migration.is_file()


def test_database_cancel_all_migrations(
    main_db_params_with_root_user, hame_database_migrated_down
):
    conn = psycopg2.connect(**main_db_params_with_root_user)
    try:
        with conn.cursor() as cur:
            # initial database must be empty
            assert_database_is_alright(
                cur,
                expected_hame_count=0,
                expected_codes_count=0,
                expected_matview_count=0,
            )

            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_name='alembic_version'"
            )
            assert cur.fetchall() == [("alembic_version",)]

            cur.execute("SELECT version_num FROM alembic_version")
            assert cur.fetchall() == []

    finally:
        conn.close()


def test_database_upgrade(main_db_params_with_root_user, hame_database_upgraded):
    conn = psycopg2.connect(**main_db_params_with_root_user)
    try:
        with conn.cursor() as cur:
            # we added an extra table to the hame scheme
            assert_database_is_alright(cur, expected_hame_count=hame_count + 1)

            cur.execute("SELECT version_num FROM alembic_version")
            assert cur.fetchall() == [(hame_database_upgraded,)]

            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_name='test_table'"
            )
            assert cur.fetchall() == [
                ("test_table",),
            ]

    finally:
        conn.close()


def test_database_downgrade(main_db_params_with_root_user, hame_database_downgraded):
    conn = psycopg2.connect(**main_db_params_with_root_user)
    try:
        with conn.cursor() as cur:
            assert_database_is_alright(cur)

            cur.execute("SELECT version_num FROM alembic_version")
            assert cur.fetchall() == [(hame_database_downgraded,)]

            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_name='test_table'"
            )
            assert cur.fetchall() == []

    finally:
        conn.close()
