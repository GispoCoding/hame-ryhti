import os
import time
import timeit
from datetime import datetime
from pathlib import Path
from typing import Iterable

import psycopg2
import pytest
import sqlalchemy
from alembic import command
from alembic.config import Config
from alembic.operations import ops
from alembic.script import ScriptDirectory
from dotenv import load_dotenv
from geoalchemy2.shape import from_shape
from shapely.geometry import MultiLineString, MultiPoint, shape
from sqlalchemy.dialects.postgresql import Range
from sqlalchemy.orm import Session, sessionmaker

from database import codes, models
from database.base import PROJECT_SRID
from database.db_helper import DatabaseHelper
from lambdas.db_manager import db_manager

hame_count: int = 13  # adjust me when adding tables
codes_count: int = 16  # adjust me when adding tables
matview_count: int = 0  # adjust me when adding views

USE_DOCKER = (
    "1"  # Use "" if you don't want pytest-docker to start and destroy the containers
)
SCHEMA_FILES_PATH = Path(".")


@pytest.fixture(scope="session", autouse=True)
def set_env():
    dotenv_file = Path(__file__).parent.parent / ".env"
    assert dotenv_file.exists()
    load_dotenv(str(dotenv_file))


@pytest.fixture(scope="session")
def root_db_params():
    return {
        "dbname": os.environ.get("DB_MAINTENANCE_NAME", ""),
        "user": os.environ.get("SU_USER", ""),
        "host": os.environ.get("DB_INSTANCE_ADDRESS", ""),
        "password": os.environ.get("SU_USER_PW", ""),
        "port": os.environ.get("DB_INSTANCE_PORT", ""),
    }


@pytest.fixture(scope="session")
def main_db_params():
    return {
        "dbname": os.environ.get("DB_MAIN_NAME", ""),
        "user": os.environ.get("RW_USER", ""),
        "host": os.environ.get("DB_INSTANCE_ADDRESS", ""),
        "password": os.environ.get("RW_USER_PW", ""),
        "port": os.environ.get("DB_INSTANCE_PORT", ""),
    }


@pytest.fixture(scope="session")
def main_db_params_with_root_user():
    return {
        "dbname": os.environ.get("DB_MAIN_NAME", ""),
        "user": os.environ.get("SU_USER", ""),
        "host": os.environ.get("DB_INSTANCE_ADDRESS", ""),
        "password": os.environ.get("SU_USER_PW", ""),
        "port": os.environ.get("DB_INSTANCE_PORT", ""),
    }


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    compose_file = Path(__file__).parent.parent / "docker-compose.dev.yml"
    assert compose_file.exists()
    return str(compose_file)


if os.environ.get("MANAGE_DOCKER", USE_DOCKER):

    @pytest.fixture(scope="session", autouse=True)
    def wait_for_services(docker_services, main_db_params, root_db_params):
        def is_responsive(params):
            succeeds = False
            try:
                with psycopg2.connect(**root_db_params):
                    succeeds = True
            except psycopg2.OperationalError:
                pass
            return succeeds

        wait_until_responsive(
            timeout=20, pause=0.5, check=lambda: is_responsive(root_db_params)
        )
        drop_hame_db(main_db_params, root_db_params)

else:

    @pytest.fixture(scope="session", autouse=True)
    def wait_for_services(main_db_params, root_db_params):
        wait_until_responsive(
            timeout=20, pause=0.5, check=lambda: is_responsive(root_db_params)
        )
        drop_hame_db(main_db_params, root_db_params)


@pytest.fixture(scope="session")
def alembic_cfg():
    return Config(Path(SCHEMA_FILES_PATH, "alembic.ini"))


@pytest.fixture(scope="session")
def current_head_version_id(alembic_cfg):
    script_dir = ScriptDirectory.from_config(alembic_cfg)
    return script_dir.get_current_head()


@pytest.fixture(scope="module")
def hame_database_created(root_db_params, main_db_params, current_head_version_id):
    event = {"event_type": 1}
    response = db_manager.handler(event, None)
    assert response["statusCode"] == 200, response["body"]
    yield current_head_version_id

    drop_hame_db(main_db_params, root_db_params)


@pytest.fixture()
def hame_database_migrated(root_db_params, main_db_params, current_head_version_id):
    event = {"event_type": 3}
    response = db_manager.handler(event, None)
    assert response["statusCode"] == 200, response["body"]
    yield current_head_version_id

    drop_hame_db(main_db_params, root_db_params)


@pytest.fixture()
def hame_database_migrated_down(hame_database_migrated):
    event = {"event_type": 3, "version": "base"}
    response = db_manager.handler(event, None)
    assert response["statusCode"] == 200, response["body"]
    yield "base"


def process_revision_directives_remove_empty(context, revision, directives):
    # remove migration if it is empty
    script = directives[0]
    if script.upgrade_ops.is_empty():
        directives[:] = []


def process_revision_directives_add_table(context, revision, directives):
    # try adding a new table
    directives[0] = ops.MigrationScript(
        "abcdef12345",
        ops.UpgradeOps(
            ops=[
                ops.CreateTableOp(
                    "test_table",
                    [
                        sqlalchemy.Column("id", sqlalchemy.Integer(), primary_key=True),
                        sqlalchemy.Column(
                            "name", sqlalchemy.String(50), nullable=False
                        ),
                    ],
                    schema="hame",
                )
            ],
        ),
        ops.DowngradeOps(
            ops=[ops.DropTableOp("test_table", schema="hame")],
        ),
    )


@pytest.fixture()
def autogenerated_migration(
    alembic_cfg, hame_database_migrated, current_head_version_id
):
    revision = command.revision(
        alembic_cfg,
        message="Test migration",
        head=current_head_version_id,
        autogenerate=True,
        process_revision_directives=process_revision_directives_remove_empty,
    )
    path = Path(revision.path) if revision else None
    yield path
    if path:
        path.unlink()


@pytest.fixture()
def new_migration(alembic_cfg, hame_database_migrated, current_head_version_id):
    revision = command.revision(
        alembic_cfg,
        message="Test migration",
        head=current_head_version_id,
        autogenerate=True,
        process_revision_directives=process_revision_directives_add_table,
    )
    path = Path(revision.path)
    assert path.is_file()
    new_head_version_id = revision.revision
    yield new_head_version_id
    path.unlink()


@pytest.fixture()
def hame_database_upgraded(new_migration):
    event = {"event_type": 3}
    response = db_manager.handler(event, None)
    assert response["statusCode"] == 200, response["body"]
    yield new_migration


@pytest.fixture()
def hame_database_downgraded(hame_database_upgraded, current_head_version_id):
    event = {"event_type": 3, "version": current_head_version_id}
    response = db_manager.handler(event, None)
    assert response["statusCode"] == 200, response["body"]
    yield current_head_version_id


def drop_hame_db(main_db_params, root_db_params):
    conn = psycopg2.connect(**root_db_params)
    try:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute(
                f"DROP DATABASE IF EXISTS {main_db_params['dbname']} WITH (FORCE)"
            )
            for user in os.environ.get("DB_USERS").split(","):
                cur.execute(f"DROP ROLE IF EXISTS {user}")
    finally:
        conn.close()


def wait_until_responsive(check, timeout, pause, clock=timeit.default_timer):
    """
    Wait until a service is responsive.
    Taken from docker_services.wait_until_responsive
    """

    ref = clock()
    now = ref
    while (now - ref) < timeout:
        if check():
            return
        time.sleep(pause)
        now = clock()

    raise Exception("Timeout reached while waiting on service!")


def is_responsive(params):
    succeeds = False
    try:
        with psycopg2.connect(**params):
            succeeds = True
    except psycopg2.OperationalError:
        pass
    return succeeds


def assert_database_is_alright(
    cur: psycopg2.extensions.cursor,
    expected_hame_count: int = hame_count,
    expected_codes_count: int = codes_count,
    expected_matview_count: int = matview_count,
):
    """
    Checks that the database has the right amount of tables with the right
    permissions.
    """
    # Check schemas
    cur.execute(
        "SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('hame', 'codes') ORDER BY schema_name DESC"  # noqa
    )
    assert cur.fetchall() == [("hame",), ("codes",)]

    # Check users
    hame_users = os.environ.get("DB_USERS", "").split(",")
    cur.execute("SELECT rolname FROM pg_roles")
    assert set(hame_users).issubset({row[0] for row in cur.fetchall()})

    # Check schema permissions
    for user in hame_users:
        cur.execute(f"SELECT has_schema_privilege('{user}', 'hame', 'usage')")
        assert cur.fetchall() == [(True,)]
        cur.execute(f"SELECT has_schema_privilege('{user}', 'codes', 'usage')")
        assert cur.fetchall() == [(True,)]

    # Check hame tables
    cur.execute("SELECT tablename, tableowner FROM pg_tables WHERE schemaname='hame';")
    hame_tables = cur.fetchall()
    assert len(hame_tables) == expected_hame_count

    for table in hame_tables:
        table_name = table[0]
        owner = table[1]

        # Check table owner and read permissions
        assert owner == os.environ.get("SU_USER", "")
        cur.execute(
            f"SELECT grantee, privilege_type FROM information_schema.role_table_grants WHERE table_schema = 'hame' AND table_name='{table_name}';"  # noqa
        )
        grants = cur.fetchall()
        assert (os.environ.get("R_USER"), "SELECT") in grants
        assert (os.environ.get("R_USER"), "INSERT") not in grants
        assert (os.environ.get("R_USER"), "UPDATE") not in grants
        assert (os.environ.get("R_USER"), "DELETE") not in grants
        assert (os.environ.get("RW_USER"), "SELECT") in grants
        assert (os.environ.get("RW_USER"), "INSERT") in grants
        assert (os.environ.get("RW_USER"), "UPDATE") in grants
        assert (os.environ.get("RW_USER"), "DELETE") in grants
        assert (os.environ.get("ADMIN_USER"), "SELECT") in grants
        assert (os.environ.get("ADMIN_USER"), "INSERT") in grants
        assert (os.environ.get("ADMIN_USER"), "UPDATE") in grants
        assert (os.environ.get("ADMIN_USER"), "DELETE") in grants

        # Check indexes
        cur.execute(
            f"SELECT * FROM pg_indexes WHERE schemaname = 'hame' AND tablename = '{table_name}';"  # noqa
        )
        indexes = cur.fetchall()
        cur.execute(
            f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'hame' AND table_name = '{table_name}';"  # noqa
        )
        columns = cur.fetchall()
        if ("id",) in columns:
            assert (
                "hame",
                table_name,
                f"{table_name}_pkey",
                None,
                f"CREATE UNIQUE INDEX {table_name}_pkey ON hame.{table_name} USING btree (id)",  # noqa
            ) in indexes
        if ("geom",) in columns:
            assert (
                "hame",
                table_name,
                f"idx_{table_name}_geom",
                None,
                f"CREATE INDEX idx_{table_name}_geom ON hame.{table_name} USING gist (geom)",  # noqa
            ) in indexes
        if ("ordering",) in columns:
            assert (
                "hame",
                table_name,
                f"ix_hame_{table_name}_ordering",
                None,
                f"CREATE INDEX ix_hame_{table_name}_ordering ON hame.{table_name} USING btree (ordering)",  # noqa
            ) in indexes

    # Check code tables
    cur.execute("SELECT tablename, tableowner FROM pg_tables WHERE schemaname='codes';")
    code_tables = cur.fetchall()
    assert len(code_tables) == expected_codes_count

    for table in code_tables:
        table_name = table[0]
        owner = table[1]

        # Check table owner and read permissions
        assert owner == os.environ.get("SU_USER", "")
        cur.execute(
            f"SELECT grantee, privilege_type FROM information_schema.role_table_grants WHERE table_schema = 'codes' AND table_name='{table_name}';"  # noqa
        )
        grants = cur.fetchall()
        assert (os.environ.get("R_USER"), "SELECT") in grants
        assert (os.environ.get("R_USER"), "INSERT") not in grants
        assert (os.environ.get("R_USER"), "UPDATE") not in grants
        assert (os.environ.get("R_USER"), "DELETE") not in grants
        assert (os.environ.get("RW_USER"), "SELECT") in grants
        assert (os.environ.get("RW_USER"), "INSERT") not in grants
        assert (os.environ.get("RW_USER"), "UPDATE") not in grants
        assert (os.environ.get("RW_USER"), "DELETE") not in grants
        assert (os.environ.get("ADMIN_USER"), "SELECT") in grants
        assert (os.environ.get("ADMIN_USER"), "INSERT") in grants
        assert (os.environ.get("ADMIN_USER"), "UPDATE") in grants
        assert (os.environ.get("ADMIN_USER"), "DELETE") in grants

        # Check code indexes
        cur.execute(
            f"SELECT * FROM pg_indexes WHERE schemaname = 'codes' AND tablename = '{table_name}';"  # noqa
        )
        indexes = cur.fetchall()
        assert (
            "codes",
            table_name,
            f"{table_name}_pkey",
            None,
            f"CREATE UNIQUE INDEX {table_name}_pkey ON codes.{table_name} USING btree (id)",  # noqa
        ) in indexes
        assert (
            "codes",
            table_name,
            f"ix_codes_{table_name}_level",
            None,
            f"CREATE INDEX ix_codes_{table_name}_level ON codes.{table_name} USING btree (level)",  # noqa
        ) in indexes
        assert (
            "codes",
            table_name,
            f"ix_codes_{table_name}_parent_id",
            None,
            f"CREATE INDEX ix_codes_{table_name}_parent_id ON codes.{table_name} USING btree (parent_id)",  # noqa
        ) in indexes
        assert (
            "codes",
            table_name,
            f"ix_codes_{table_name}_short_name",
            None,
            f"CREATE INDEX ix_codes_{table_name}_short_name ON codes.{table_name} USING btree (short_name)",  # noqa
        ) in indexes
        assert (
            "codes",
            table_name,
            f"ix_codes_{table_name}_value",
            None,
            f"CREATE UNIQUE INDEX ix_codes_{table_name}_value ON codes.{table_name} USING btree (value)",  # noqa
        ) in indexes

    # TODO: Check materialized views once we have any
    # cur.execute(
    #     "SELECT matviewname, matviewowner FROM pg_matviews WHERE schemaname='kooste';"
    # )
    # materialized_views = cur.fetchall()
    # assert len(materialized_views) == expected_matview_count

    # for view in materialized_views:
    #     view_name = view[0]
    #     owner = view[1]

    #     # Check view owner and read permissions
    #     # Materialized views must be owned by the read_write user so they can be
    #     updated automatically!
    #     assert owner == os.environ.get("RW_USER", "")
    #     # Materialized views permissions are only stored in psql specific tables
    #     cur.execute(f"SELECT relacl FROM pg_class WHERE relname='{view_name}';")
    #     permission_string = cur.fetchall()[0][0]
    #     assert f"{os.environ.get('R_USER')}=r/" in permission_string
    #     assert f"{os.environ.get('RW_USER')}=arwdDxt/" in permission_string
    #     assert f"{os.environ.get('ADMIN_USER')}=arwdDxt/" in permission_string


@pytest.fixture(scope="module")
def connection_string(hame_database_created) -> str:
    return DatabaseHelper().get_connection_string()


@pytest.fixture(scope="module")
def session(connection_string):
    engine = sqlalchemy.create_engine(connection_string)
    session = sessionmaker(bind=engine)
    yield session()


@pytest.fixture(scope="module")
def code_instance(session):
    instance = codes.LifeCycleStatus(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def another_code_instance(session):
    instance = codes.LifeCycleStatus(value="test2", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def preparation_status_instance(session) -> codes.LifeCycleStatus:
    instance = codes.LifeCycleStatus(value="03", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def plan_type_instance(session):
    instance = codes.PlanType(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def type_of_underground_instance(session):
    instance = codes.TypeOfUnderground(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def type_of_plan_regulation_group_instance(session):
    instance = codes.TypeOfPlanRegulationGroup(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def type_of_plan_regulation_instance(session):
    instance = codes.TypeOfPlanRegulation(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def type_of_verbal_plan_regulation_instance(session):
    instance = codes.TypeOfVerbalPlanRegulation(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def type_of_additional_information_instance(session):
    instance = codes.TypeOfAdditionalInformation(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def type_of_source_data_instance(session):
    instance = codes.TypeOfSourceData(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def type_of_document_instance(session):
    instance = codes.TypeOfDocument(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def category_of_publicity_instance(session):
    instance = codes.CategoryOfPublicity(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def administrative_region_instance(session):
    instance = codes.AdministrativeRegion(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def another_administrative_region_instance(session):
    instance = codes.AdministrativeRegion(value="other-test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def plan_theme_instance(session):
    instance = codes.PlanTheme(value="test", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="function")
def plan_instance(
    session,
    preparation_status_instance,
    organisation_instance,
    plan_type_instance,
    general_regulation_group_instance,
):
    instance = models.Plan(
        geom=from_shape(
            shape(
                {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [381849.834412134019658, 6677967.973336197435856],
                                [381849.834412134019658, 6680613.389312859624624],
                                [386378.427863708813675, 6680613.389312859624624],
                                [386378.427863708813675, 6677967.973336197435856],
                                [381849.834412134019658, 6677967.973336197435856],
                            ]
                        ]
                    ],
                }
            ),
            srid=PROJECT_SRID,
            extended=True,
        ),
        scale=1,
        description={"fin": "test_plan"},
        lifecycle_status=preparation_status_instance,
        organisation=organisation_instance,
        plan_type=plan_type_instance,
        plan_regulation_group=general_regulation_group_instance,
        to_be_exported=True,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="module")
def organisation_instance(session, administrative_region_instance):
    instance = models.Organisation(
        business_id="test", administrative_region=administrative_region_instance
    )
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def another_organisation_instance(session, another_administrative_region_instance):
    instance = models.Organisation(
        business_id="other-test",
        administrative_region=another_administrative_region_instance,
    )
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="function")
def land_use_area_instance(
    session,
    preparation_status_instance,
    type_of_underground_instance,
    plan_instance,
    plan_regulation_group_instance,
):
    instance = models.LandUseArea(
        geom=from_shape(
            shape(
                {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [381849.834412134019658, 6677967.973336197435856],
                                [381849.834412134019658, 6680613.389312859624624],
                                [386378.427863708813675, 6680613.389312859624624],
                                [386378.427863708813675, 6677967.973336197435856],
                                [381849.834412134019658, 6677967.973336197435856],
                            ]
                        ]
                    ],
                }
            ),
            srid=PROJECT_SRID,
            extended=True,
        ),
        name={"fin": "test_land_use_area"},
        description={"fin": "test_land_use_area"},
        height_range=Range(0.0, 1.0),
        height_unit="m",
        lifecycle_status=preparation_status_instance,
        type_of_underground=type_of_underground_instance,
        plan=plan_instance,
        plan_regulation_group=plan_regulation_group_instance,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def other_area_instance(
    session,
    preparation_status_instance,
    type_of_underground_instance,
    plan_instance,
    plan_regulation_group_instance,
):
    instance = models.OtherArea(
        geom=from_shape(
            shape(
                {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [381849.834412134019658, 6677967.973336197435856],
                                [381849.834412134019658, 6680613.389312859624624],
                                [386378.427863708813675, 6680613.389312859624624],
                                [386378.427863708813675, 6677967.973336197435856],
                                [381849.834412134019658, 6677967.973336197435856],
                            ]
                        ]
                    ],
                }
            ),
            srid=PROJECT_SRID,
            extended=True,
        ),
        lifecycle_status=preparation_status_instance,
        type_of_underground=type_of_underground_instance,
        plan=plan_instance,
        plan_regulation_group=plan_regulation_group_instance,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def line_instance(
    session,
    preparation_status_instance,
    type_of_underground_instance,
    plan_instance,
    plan_regulation_group_instance,
):
    instance = models.Line(
        geom=from_shape(
            MultiLineString(
                [
                    [[382000, 6678000], [383000, 6678000]],
                ]
            )
        ),
        lifecycle_status=preparation_status_instance,
        type_of_underground=type_of_underground_instance,
        plan=plan_instance,
        plan_regulation_group=plan_regulation_group_instance,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def land_use_point_instance(
    session,
    preparation_status_instance,
    type_of_underground_instance,
    plan_instance,
    point_plan_regulation_group_instance,
):
    instance = models.LandUsePoint(
        geom=from_shape(MultiPoint([[382000, 6678000]])),
        name={"fin": "test_land_use_point"},
        description={"fin": "test_land_use_point"},
        lifecycle_status=preparation_status_instance,
        type_of_underground=type_of_underground_instance,
        plan=plan_instance,
        plan_regulation_group=point_plan_regulation_group_instance,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def other_point_instance(
    session,
    preparation_status_instance,
    type_of_underground_instance,
    plan_instance,
    point_plan_regulation_group_instance,
):
    instance = models.OtherPoint(
        geom=from_shape(MultiPoint([[382000, 6678000], [383000, 6678000]])),
        lifecycle_status=preparation_status_instance,
        type_of_underground=type_of_underground_instance,
        plan=plan_instance,
        plan_regulation_group=point_plan_regulation_group_instance,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def plan_regulation_group_instance(session, type_of_plan_regulation_group_instance):
    instance = models.PlanRegulationGroup(
        short_name="K",
        type_of_plan_regulation_group=type_of_plan_regulation_group_instance,
        name={"fin": "test_plan_regulation_group"},
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def point_plan_regulation_group_instance(
    session, type_of_plan_regulation_group_instance
):
    instance = models.PlanRegulationGroup(
        short_name="L",
        type_of_plan_regulation_group=type_of_plan_regulation_group_instance,
        name={"fin": "test_point_plan_regulation_group"},
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def general_regulation_group_instance(session, type_of_plan_regulation_group_instance):
    instance = models.PlanRegulationGroup(
        short_name="Y",
        type_of_plan_regulation_group=type_of_plan_regulation_group_instance,
        name={"fin": "test_general_regulation_group"},
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def empty_value_plan_regulation_instance(
    session,
    preparation_status_instance,
    type_of_plan_regulation_instance,
    plan_regulation_group_instance,
):
    instance = models.PlanRegulation(
        name={"fin": "test_regulation"},
        lifecycle_status=preparation_status_instance,
        type_of_plan_regulation=type_of_plan_regulation_instance,
        plan_regulation_group=plan_regulation_group_instance,
        ordering=1,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def numeric_plan_regulation_instance(
    session,
    preparation_status_instance,
    type_of_plan_regulation_instance,
    plan_regulation_group_instance,
):
    instance = models.PlanRegulation(
        name={"fin": "test_regulation"},
        numeric_value=1.0,
        unit="m",
        lifecycle_status=preparation_status_instance,
        type_of_plan_regulation=type_of_plan_regulation_instance,
        plan_regulation_group=plan_regulation_group_instance,
        ordering=2,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def text_plan_regulation_instance(
    session,
    preparation_status_instance,
    type_of_plan_regulation_instance,
    plan_regulation_group_instance,
):
    instance = models.PlanRegulation(
        name={"fin": "test_regulation"},
        text_value={"fin": "test_value"},
        lifecycle_status=preparation_status_instance,
        type_of_plan_regulation=type_of_plan_regulation_instance,
        plan_regulation_group=plan_regulation_group_instance,
        ordering=3,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def point_text_plan_regulation_instance(
    session,
    preparation_status_instance,
    type_of_plan_regulation_instance,
    point_plan_regulation_group_instance,
):
    instance = models.PlanRegulation(
        name={"fin": "test_regulation"},
        text_value={"fin": "test_value"},
        lifecycle_status=preparation_status_instance,
        type_of_plan_regulation=type_of_plan_regulation_instance,
        plan_regulation_group=point_plan_regulation_group_instance,
        ordering=1,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def verbal_plan_regulation_instance(
    session,
    preparation_status_instance,
    type_of_plan_regulation_instance,
    type_of_verbal_plan_regulation_instance,
    plan_regulation_group_instance,
):
    """
    Looks like verbal plan regulations have to be serialized differently, type of
    verbal plan regulation is not allowed in other plan regulations. No idea how
    they differ from text regulations otherwise, though.
    """
    instance = models.PlanRegulation(
        name={"fin": "test_regulation"},
        text_value={"fin": "test_value"},
        lifecycle_status=preparation_status_instance,
        type_of_plan_regulation=type_of_plan_regulation_instance,
        type_of_verbal_plan_regulation=type_of_verbal_plan_regulation_instance,
        plan_regulation_group=plan_regulation_group_instance,
        ordering=4,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def general_plan_regulation_instance(
    session,
    preparation_status_instance,
    type_of_plan_regulation_instance,
    general_regulation_group_instance,
):
    instance = models.PlanRegulation(
        name={"fin": "general_regulation"},
        text_value={"fin": "test_value"},
        lifecycle_status=preparation_status_instance,
        type_of_plan_regulation=type_of_plan_regulation_instance,
        plan_regulation_group=general_regulation_group_instance,
        ordering=1,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def plan_proposition_instance(
    session, preparation_status_instance, plan_regulation_group_instance
):
    instance = models.PlanProposition(
        lifecycle_status=preparation_status_instance,
        plan_regulation_group=plan_regulation_group_instance,
        text_value={"fin": "test_recommendation"},
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def source_data_instance(session, plan_instance, type_of_source_data_instance):
    instance = models.SourceData(
        additional_information_uri="http://test.fi",
        detachment_date=datetime.now(),
        plan=plan_instance,
        type_of_source_data=type_of_source_data_instance,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def document_instance(
    session, type_of_document_instance, category_of_publicity_instance, plan_instance
):
    instance = models.Document(
        name="Testidokumentti",
        type_of_document=type_of_document_instance,
        personal_details="Testihenkilö",
        publicity=category_of_publicity_instance,
        language="fin",
        decision=False,
        plan=plan_instance,
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="module")
def lifecycle_date_instance(session, code_instance):
    instance = models.LifeCycleDate(lifecycle_status=code_instance)
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="function")
def complete_test_plan(
    session: Session,
    plan_instance: models.Plan,
    land_use_area_instance: models.LandUseArea,
    land_use_point_instance: models.LandUsePoint,
    plan_regulation_group_instance: models.PlanRegulationGroup,
    point_plan_regulation_group_instance: models.PlanRegulationGroup,
    general_regulation_group_instance: models.PlanRegulationGroup,
    empty_value_plan_regulation_instance: models.PlanRegulation,
    text_plan_regulation_instance: models.PlanRegulation,
    point_text_plan_regulation_instance: models.PlanRegulation,
    numeric_plan_regulation_instance: models.PlanRegulation,
    verbal_plan_regulation_instance: models.PlanRegulation,
    general_plan_regulation_instance: models.PlanRegulation,
    plan_proposition_instance: models.PlanProposition,
    plan_theme_instance: codes.PlanTheme,
    type_of_additional_information_instance: codes.TypeOfAdditionalInformation,
    participation_plan_presenting_for_public_decision: codes.NameOfPlanCaseDecision,
    plan_material_presenting_for_public_decision: codes.NameOfPlanCaseDecision,
    draft_plan_presenting_for_public_decision: codes.NameOfPlanCaseDecision,
    participation_plan_presenting_for_public_event: codes.TypeOfProcessingEvent,
    plan_material_presenting_for_public_event: codes.TypeOfProcessingEvent,
    presentation_to_the_public_interaction: codes.TypeOfInteractionEvent,
    decisionmaker_type: codes.TypeOfDecisionMaker,
    pending_date_instance: models.LifeCycleDate,
    preparation_date_instance: models.LifeCycleDate,
) -> Iterable[models.Plan]:
    """
    Plan data that might be more or less complete, to be tested and validated with the
    Ryhti API.

    For the plan *matter* to be validated, we also need extra code objects (that are not
    linked to the plan in the database) to be committed to the database, and some
    dates for the plan lifecycle statuses to be set.
    """
    # Add the optional (nullable) relationships. We don't want them to be present in
    # all fixtures.
    empty_value_plan_regulation_instance.plan_theme = plan_theme_instance
    empty_value_plan_regulation_instance.intended_use = (
        type_of_additional_information_instance
    )
    text_plan_regulation_instance.plan_theme = plan_theme_instance
    text_plan_regulation_instance.intended_use = type_of_additional_information_instance
    point_text_plan_regulation_instance.plan_theme = plan_theme_instance
    point_text_plan_regulation_instance.intended_use = (
        type_of_additional_information_instance
    )
    numeric_plan_regulation_instance.plan_theme = plan_theme_instance
    numeric_plan_regulation_instance.intended_use = (
        type_of_additional_information_instance
    )
    verbal_plan_regulation_instance.plan_theme = plan_theme_instance
    verbal_plan_regulation_instance.intended_use = (
        type_of_additional_information_instance
    )
    general_plan_regulation_instance.plan_theme = plan_theme_instance
    general_plan_regulation_instance.intended_use = (
        type_of_additional_information_instance  # noqa
    )
    plan_proposition_instance.plan_theme = plan_theme_instance
    session.commit()
    yield plan_instance
    session.delete(plan_instance)
    session.commit()


@pytest.fixture(scope="module")
def pending_status_instance(session) -> codes.LifeCycleStatus:
    instance = codes.LifeCycleStatus(value="02", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="function")
def pending_date_instance(
    session, plan_instance, pending_status_instance
) -> Iterable[models.LifeCycleDate]:
    instance = models.LifeCycleDate(
        plan=plan_instance,
        lifecycle_status=pending_status_instance,
        starting_at=datetime(2024, 1, 1),
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="function")
def preparation_date_instance(
    session, plan_instance, preparation_status_instance
) -> Iterable[models.LifeCycleDate]:
    instance = models.LifeCycleDate(
        plan=plan_instance,
        lifecycle_status=preparation_status_instance,
        starting_at=datetime(2024, 2, 1),
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="module")
def approved_status_instance(session) -> codes.LifeCycleStatus:
    instance = codes.LifeCycleStatus(value="06", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="function")
def approved_date_instance(
    session, plan_instance, approved_status_instance
) -> Iterable[models.LifeCycleDate]:
    instance = models.LifeCycleDate(
        plan=plan_instance,
        lifecycle_status=approved_status_instance,
        starting_at=datetime(2024, 3, 1),
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="module")
def valid_status_instance(session) -> codes.LifeCycleStatus:
    instance = codes.LifeCycleStatus(value="13", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="function")
def valid_date_instance(
    session, plan_instance, valid_status_instance
) -> Iterable[models.LifeCycleDate]:
    instance = models.LifeCycleDate(
        plan=plan_instance,
        lifecycle_status=valid_status_instance,
        starting_at=datetime(2024, 4, 1),
    )
    session.add(instance)
    session.commit()
    yield instance
    session.delete(instance)
    session.commit()


@pytest.fixture(scope="module")
def participation_plan_presenting_for_public_decision(
    session,
) -> codes.NameOfPlanCaseDecision:
    instance = codes.NameOfPlanCaseDecision(value="04", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def plan_material_presenting_for_public_decision(
    session,
) -> codes.NameOfPlanCaseDecision:
    instance = codes.NameOfPlanCaseDecision(value="05", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def draft_plan_presenting_for_public_decision(
    session,
) -> codes.NameOfPlanCaseDecision:
    instance = codes.NameOfPlanCaseDecision(value="06", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def participation_plan_presenting_for_public_event(
    session,
) -> codes.TypeOfProcessingEvent:
    instance = codes.TypeOfProcessingEvent(value="05", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def plan_material_presenting_for_public_event(
    session,
) -> codes.TypeOfProcessingEvent:
    instance = codes.TypeOfProcessingEvent(value="06", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def presentation_to_the_public_interaction(
    session,
) -> codes.TypeOfInteractionEvent:
    instance = codes.TypeOfInteractionEvent(value="01", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance


@pytest.fixture(scope="module")
def decisionmaker_type(session) -> codes.TypeOfDecisionMaker:
    instance = codes.TypeOfDecisionMaker(value="01", status="LOCAL")
    session.add(instance)
    session.commit()
    return instance