from datetime import datetime

import codes
import models
import pytest
from geoalchemy2.shape import from_shape
from shapely import transform
from shapely.geometry import MultiLineString, MultiPoint, MultiPolygon, shape
from sqlalchemy.exc import InternalError
from sqlalchemy.orm import Session


def test_modified_at_triggers(
    session: Session,
    plan_instance: models.Plan,
    land_use_area_instance: models.LandUseArea,
    other_area_instance: models.OtherArea,
    line_instance: models.Line,
    land_use_point_instance: models.LandUsePoint,
    other_point_instance: models.OtherPoint,
    plan_regulation_group_instance: models.PlanRegulationGroup,
    text_plan_regulation_instance: models.PlanRegulation,
    plan_proposition_instance: models.PlanProposition,
    source_data_instance: models.SourceData,
    organisation_instance: models.Organisation,
    document_instance: models.Document,
    lifecycle_date_instance: models.LifeCycleDate,
):
    # Save old modified_at timestamps
    plan_old_modified_at = plan_instance.modified_at
    land_use_area_instance_old_modified_at = land_use_area_instance.modified_at
    other_area_instance_old_modified_at = other_area_instance.modified_at
    line_instance_old_modified_at = line_instance.modified_at
    land_use_point_instance_old_modified_at = land_use_point_instance.modified_at
    other_point_instance_old_modified_at = other_point_instance.modified_at
    plan_regulation_group_instance_old_modified_at = (
        plan_regulation_group_instance.modified_at
    )
    plan_regulation_old_modified_at = text_plan_regulation_instance.modified_at
    plan_proposition_instance_old_modified_at = plan_proposition_instance.modified_at
    source_data_instance_old_modified_at = source_data_instance.modified_at
    organisation_instance_old_modified_at = organisation_instance.modified_at
    document_instance_old_modified_at = document_instance.modified_at
    lifecycle_date_instance_old_modified_at = lifecycle_date_instance.modified_at

    # Edit tables to fire the triggers
    plan_instance.exported_at = datetime.now()
    land_use_area_instance.ordering = 1
    other_area_instance.ordering = 1
    line_instance.ordering = 1
    land_use_point_instance.ordering = 1
    other_point_instance.ordering = 1
    plan_regulation_group_instance.short_name = "foo"
    text_plan_regulation_instance.text_value = "foo"
    plan_proposition_instance.text_value = "foo"
    source_data_instance.additional_information_uri = "http://test2.fi"
    organisation_instance.business_id = "foo"
    document_instance.name = "foo"
    lifecycle_date_instance.ending_at = datetime.now()
    session.flush()
    session.refresh(plan_instance)
    session.refresh(land_use_area_instance)
    session.refresh(other_area_instance)
    session.refresh(line_instance)
    session.refresh(land_use_point_instance)
    session.refresh(other_point_instance)
    session.refresh(plan_regulation_group_instance)
    session.refresh(text_plan_regulation_instance)
    session.refresh(plan_proposition_instance)
    session.refresh(source_data_instance)
    session.refresh(organisation_instance)
    session.refresh(document_instance)
    session.refresh(lifecycle_date_instance)

    assert plan_instance.modified_at != plan_old_modified_at
    assert land_use_area_instance.modified_at != land_use_area_instance_old_modified_at
    assert other_area_instance.modified_at != other_area_instance_old_modified_at
    assert line_instance.modified_at != line_instance_old_modified_at
    assert (
        land_use_point_instance.modified_at != land_use_point_instance_old_modified_at
    )
    assert other_point_instance.modified_at != other_point_instance_old_modified_at
    assert (
        plan_regulation_group_instance.modified_at
        != plan_regulation_group_instance_old_modified_at
    )
    assert text_plan_regulation_instance.modified_at != plan_regulation_old_modified_at
    assert (
        plan_proposition_instance.modified_at
        != plan_proposition_instance_old_modified_at
    )
    assert source_data_instance.modified_at != source_data_instance_old_modified_at
    assert organisation_instance.modified_at != organisation_instance_old_modified_at
    assert document_instance != document_instance_old_modified_at
    assert (
        lifecycle_date_instance.modified_at != lifecycle_date_instance_old_modified_at
    )


def test_new_lifecycle_date_triggers(
    session: Session,
    plan_instance: models.Plan,
    text_plan_regulation_instance: models.PlanRegulation,
    plan_proposition_instance: models.PlanProposition,
    land_use_area_instance: models.LandUseArea,
    other_area_instance: models.OtherArea,
    line_instance: models.Line,
    land_use_point_instance: models.LandUsePoint,
    other_point_instance: models.OtherPoint,
    code_instance: codes.LifeCycleStatus,
    another_code_instance: codes.LifeCycleStatus,
):
    assert plan_instance.lifecycle_status_id != another_code_instance.id
    assert text_plan_regulation_instance.lifecycle_status_id != another_code_instance.id
    assert plan_proposition_instance.lifecycle_status_id != another_code_instance.id
    assert land_use_area_instance.lifecycle_status_id != another_code_instance.id
    assert other_area_instance.lifecycle_status_id != another_code_instance.id
    assert line_instance.lifecycle_status_id != another_code_instance.id
    assert land_use_point_instance.lifecycle_status_id != another_code_instance.id
    assert other_point_instance.lifecycle_status_id != another_code_instance.id

    # Update lifecycle_statuses to populate starting_at fields
    plan_instance.lifecycle_status = another_code_instance
    text_plan_regulation_instance.lifecycle_status = another_code_instance
    plan_proposition_instance.lifecycle_status = another_code_instance
    land_use_area_instance.lifecycle_status = another_code_instance
    other_area_instance.lifecycle_status = another_code_instance
    line_instance.lifecycle_status = another_code_instance
    land_use_point_instance.lifecycle_status = another_code_instance
    other_point_instance.lifecycle_status = another_code_instance
    session.flush()

    # Update again to populate ending_at fields
    plan_instance.lifecycle_status = code_instance
    text_plan_regulation_instance.lifecycle_status = code_instance
    plan_proposition_instance.lifecycle_status = code_instance
    land_use_area_instance.lifecycle_status = code_instance
    other_area_instance.lifecycle_status = code_instance
    line_instance.lifecycle_status = code_instance
    land_use_point_instance.lifecycle_status = code_instance
    other_point_instance.lifecycle_status = code_instance
    session.flush()
    session.refresh(plan_instance)
    session.refresh(text_plan_regulation_instance)
    session.refresh(plan_proposition_instance)
    session.refresh(land_use_area_instance)
    session.refresh(other_area_instance)
    session.refresh(line_instance)
    session.refresh(land_use_point_instance)
    session.refresh(other_point_instance)

    # Get old and new entries in lifecycle_date table
    plan_new_lifecycle_date = plan_instance.lifecycle_dates[0]
    plan_regulation_new_lifecycle_date = text_plan_regulation_instance.lifecycle_dates[
        0
    ]
    plan_proposition_new_lifecycle_date = plan_proposition_instance.lifecycle_dates[0]
    land_use_area_new_lifecycle_date = land_use_area_instance.lifecycle_dates[0]
    other_area_new_lifecycle_date = other_area_instance.lifecycle_dates[0]
    line_new_lifecycle_date = line_instance.lifecycle_dates[0]
    land_use_point_new_lifecycle_date = land_use_point_instance.lifecycle_dates[0]
    other_point_new_lifecycle_date = other_point_instance.lifecycle_dates[0]

    plan_old_lifecycle_date = plan_instance.lifecycle_dates[1]
    plan_regulation_old_lifecycle_date = text_plan_regulation_instance.lifecycle_dates[
        1
    ]
    plan_proposition_old_lifecycle_date = plan_proposition_instance.lifecycle_dates[1]
    land_use_area_old_lifecycle_date = land_use_area_instance.lifecycle_dates[1]
    other_area_old_lifecycle_date = other_area_instance.lifecycle_dates[1]
    line_old_lifecycle_date = line_instance.lifecycle_dates[1]
    land_use_point_old_lifecycle_date = land_use_point_instance.lifecycle_dates[1]
    other_point_old_lifecycle_date = other_point_instance.lifecycle_dates[1]
    session.flush()

    assert plan_new_lifecycle_date.lifecycle_status_id == code_instance.id
    assert plan_new_lifecycle_date.starting_at is not None
    assert plan_old_lifecycle_date.ending_at is not None

    assert plan_regulation_new_lifecycle_date.lifecycle_status_id == code_instance.id
    assert plan_regulation_new_lifecycle_date.starting_at is not None
    assert plan_regulation_old_lifecycle_date.ending_at is not None

    assert plan_proposition_new_lifecycle_date.lifecycle_status_id == code_instance.id
    assert plan_proposition_new_lifecycle_date.starting_at is not None
    assert plan_proposition_old_lifecycle_date.ending_at is not None

    assert land_use_area_instance.lifecycle_status_id == code_instance.id
    assert land_use_area_new_lifecycle_date.starting_at is not None
    assert land_use_area_old_lifecycle_date.ending_at is not None

    assert other_area_instance.lifecycle_status_id == code_instance.id
    assert other_area_new_lifecycle_date.starting_at is not None
    assert other_area_old_lifecycle_date.ending_at is not None

    assert line_instance.lifecycle_status_id == code_instance.id
    assert line_new_lifecycle_date.starting_at is not None
    assert line_old_lifecycle_date.ending_at is not None

    assert land_use_point_instance.lifecycle_status_id == code_instance.id
    assert land_use_point_new_lifecycle_date.starting_at is not None
    assert land_use_point_old_lifecycle_date.ending_at is not None

    assert other_point_instance.lifecycle_status_id == code_instance.id
    assert other_point_new_lifecycle_date.starting_at is not None
    assert other_point_old_lifecycle_date.ending_at is not None


def test_new_lifecycle_status_triggers(
    session: Session,
    plan_instance: models.Plan,
    plan_regulation_group_instance: models.PlanRegulationGroup,
    general_regulation_group_instance: models.PlanRegulationGroup,
    code_instance: codes.LifeCycleStatus,
    another_code_instance: codes.LifeCycleStatus,
    type_of_plan_regulation_instance: codes.TypeOfPlanRegulation,
    type_of_underground_instance: codes.TypeOfUnderground,
):
    assert plan_instance.general_plan_regulation_groups == [
        general_regulation_group_instance
    ]

    plan_instance.lifecycle_status = another_code_instance
    session.flush()

    # Create new objects in the plan area (geometry creates link to plan instance)
    land_use_area_instance = models.LandUseArea(
        lifecycle_status=code_instance,
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
            )
        ),
        plan=plan_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    other_area_instance = models.OtherArea(
        lifecycle_status=code_instance,
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
            )
        ),
        plan=plan_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    line_instance = models.Line(
        lifecycle_status=code_instance,
        geom=from_shape(
            MultiLineString(
                [
                    [[382000, 6678000], [383000, 6678000]],
                ]
            )
        ),
        plan=plan_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    land_use_point_instance = models.LandUsePoint(
        lifecycle_status=code_instance,
        geom=from_shape(MultiPoint([[382000, 6678000], [383000, 6678000]])),
        plan=plan_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    other_point_instance = models.OtherPoint(
        lifecycle_status=code_instance,
        geom=from_shape(MultiPoint([[382000, 6678000], [383000, 6678000]])),
        plan=plan_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    session.add(land_use_area_instance)
    session.add(other_area_instance)
    session.add(line_instance)
    session.add(land_use_point_instance)
    session.add(other_point_instance)
    session.flush()

    # Create new regulations in regulation groups already linked to plan
    general_regulation_instance = models.PlanRegulation(
        lifecycle_status=code_instance,
        type_of_plan_regulation=type_of_plan_regulation_instance,
        plan_regulation_group=general_regulation_group_instance,
    )
    general_proposition_instance = models.PlanProposition(
        lifecycle_status=code_instance,
        plan_regulation_group=general_regulation_group_instance,
    )
    plan_regulation_instance = models.PlanRegulation(
        lifecycle_status=code_instance,
        type_of_plan_regulation=type_of_plan_regulation_instance,
        plan_regulation_group=plan_regulation_group_instance,
    )
    plan_proposition_instance = models.PlanProposition(
        lifecycle_status=code_instance,
        plan_regulation_group=plan_regulation_group_instance,
    )
    session.add(general_regulation_instance)
    session.add(general_proposition_instance)
    session.add(plan_regulation_instance)
    session.add(plan_proposition_instance)
    session.flush()

    session.refresh(land_use_area_instance)
    session.refresh(other_area_instance)
    session.refresh(line_instance)
    session.refresh(land_use_point_instance)
    session.refresh(other_point_instance)
    session.refresh(general_regulation_instance)
    session.refresh(general_proposition_instance)
    session.refresh(plan_regulation_instance)
    session.refresh(plan_proposition_instance)

    # Check that new features and regulations have same status as plan
    print(plan_regulation_instance.lifecycle_status.value)
    print(another_code_instance.value)
    assert land_use_area_instance.lifecycle_status == another_code_instance
    assert other_area_instance.lifecycle_status == another_code_instance
    assert line_instance.lifecycle_status == another_code_instance
    assert land_use_point_instance.lifecycle_status == another_code_instance
    assert other_point_instance.lifecycle_status == another_code_instance
    assert general_regulation_instance.lifecycle_status == another_code_instance
    assert general_proposition_instance.lifecycle_status == another_code_instance
    assert plan_regulation_instance.lifecycle_status == another_code_instance
    assert plan_proposition_instance.lifecycle_status == another_code_instance

    # Delete created objects from the test database
    session.rollback()


def test_update_lifecycle_status_triggers(
    session: Session,
    plan_instance: models.Plan,
    plan_regulation_group_instance: models.PlanRegulationGroup,
    point_plan_regulation_group_instance: models.PlanRegulationGroup,
    general_regulation_group_instance: models.PlanRegulationGroup,
    land_use_area_instance: models.LandUseArea,
    other_area_instance: models.OtherArea,
    line_instance: models.Line,
    land_use_point_instance: models.LandUsePoint,
    other_point_instance: models.OtherPoint,
    text_plan_regulation_instance: models.PlanRegulation,
    general_plan_regulation_instance: models.PlanRegulation,
    plan_proposition_instance: models.PlanProposition,
    code_instance: codes.LifeCycleStatus,
    another_code_instance: codes.LifeCycleStatus,
):
    """
    We must test that the trigger also updates everything in plan objects and plan regulations
    on the plan that *do not* have the same plan regulation group as the plan.
    """
    plan_instance.lifecycle_status = code_instance
    session.flush()
    assert plan_instance.lifecycle_status != another_code_instance
    assert text_plan_regulation_instance.lifecycle_status != another_code_instance
    assert (
        text_plan_regulation_instance.plan_regulation_group
        == plan_regulation_group_instance
    )
    assert general_plan_regulation_instance.lifecycle_status != another_code_instance
    assert (
        general_plan_regulation_instance.plan_regulation_group
        == general_regulation_group_instance
    )
    assert plan_proposition_instance.lifecycle_status != another_code_instance
    assert (
        plan_proposition_instance.plan_regulation_group
        == plan_regulation_group_instance
    )

    assert land_use_area_instance.lifecycle_status != another_code_instance
    assert other_area_instance.lifecycle_status != another_code_instance
    assert line_instance.lifecycle_status != another_code_instance
    assert land_use_point_instance.lifecycle_status != another_code_instance
    assert other_point_instance.lifecycle_status != another_code_instance
    assert plan_instance.general_plan_regulation_groups == [
        general_regulation_group_instance
    ]
    assert land_use_area_instance.plan_regulation_groups == [
        plan_regulation_group_instance
    ]
    assert other_area_instance.plan_regulation_groups == [
        plan_regulation_group_instance
    ]
    assert line_instance.plan_regulation_groups == [plan_regulation_group_instance]
    assert land_use_point_instance.plan_regulation_groups == [
        point_plan_regulation_group_instance
    ]
    assert other_point_instance.plan_regulation_groups == [
        point_plan_regulation_group_instance
    ]

    # Change lifecycle status to fire the triggers
    plan_instance.lifecycle_status = another_code_instance
    session.flush()
    session.refresh(land_use_area_instance)
    session.refresh(other_area_instance)
    session.refresh(line_instance)
    session.refresh(land_use_point_instance)
    session.refresh(other_point_instance)
    session.refresh(text_plan_regulation_instance)
    session.refresh(general_plan_regulation_instance)
    session.refresh(plan_proposition_instance)

    # Check that features and regulations have same status as plan
    assert plan_instance.lifecycle_status == another_code_instance
    assert land_use_area_instance.lifecycle_status == another_code_instance
    assert other_area_instance.lifecycle_status == another_code_instance
    assert line_instance.lifecycle_status == another_code_instance
    assert land_use_point_instance.lifecycle_status == another_code_instance
    assert other_point_instance.lifecycle_status == another_code_instance
    assert text_plan_regulation_instance.lifecycle_status == another_code_instance
    assert general_plan_regulation_instance.lifecycle_status == another_code_instance
    assert plan_proposition_instance.lifecycle_status == another_code_instance


def test_add_plan_id_fkey_triggers(
    session: Session,
    plan_instance: models.Plan,
    plan_type_instance: codes.PlanType,
    code_instance: codes.LifeCycleStatus,
    type_of_underground_instance: codes.TypeOfUnderground,
    plan_regulation_group_instance: models.PlanRegulationGroup,
    organisation_instance: models.Organisation,
):
    # Add another plan instance
    another_plan_instance = models.Plan(
        geom=from_shape(
            MultiPolygon([(((1.0, 2.0), (2.0, 2.0), (2.0, 1.0), (1.0, 1.0)),)])
        ),
        plan_type=plan_type_instance,
        lifecycle_status=code_instance,
        organisation=organisation_instance,
    )
    session.add(another_plan_instance)

    # Geometries inside either plan instance
    polygon_1 = MultiPolygon(
        [
            (
                (
                    (382000.0, 6678000.0),
                    (386000.0, 6678000.0),
                    (386000.0, 6680000.0),
                    (382000.0, 6680000.0),
                ),
            )
        ]
    )
    point_1 = MultiPoint([[(383000.0, 6678500.0)], [384000.0, 6679500.0]])
    polygon_2 = MultiPolygon([(((1.0, 2.0), (2.0, 2.0), (2.0, 1.0), (1.0, 1.0)),)])
    point_2 = MultiPoint([[1.25, 1.25], [1.75, 1.75]])
    line_1 = MultiLineString(
        [
            [[383000.0, 6678500.0], [384000.0, 6679500.0]],
        ]
    )
    line_2 = MultiLineString(
        [
            [[1.25, 1.25], [1.75, 1.75]],
        ]
    )

    # Add new plan object instances to fire the triggers
    another_land_use_area_instance = models.LandUseArea(
        geom=from_shape(polygon_1),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    session.add(another_land_use_area_instance)

    another_area_instance = models.OtherArea(
        geom=from_shape(polygon_2),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    session.add(another_area_instance)

    another_line_instance = models.Line(
        geom=from_shape(line_1),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    session.add(another_line_instance)
    another_another_line_instance = models.Line(
        geom=from_shape(line_2),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    session.add(another_another_line_instance)

    another_land_use_point_instance = models.LandUsePoint(
        geom=from_shape(point_1),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    session.add(another_land_use_point_instance)

    another_point_instance = models.OtherPoint(
        geom=from_shape(point_2),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    session.add(another_point_instance)
    session.flush()

    session.refresh(another_land_use_area_instance)
    session.refresh(another_area_instance)
    session.refresh(another_line_instance)
    session.refresh(another_another_line_instance)
    session.refresh(another_land_use_point_instance)
    session.refresh(another_point_instance)

    assert another_land_use_area_instance.plan_id == plan_instance.id
    assert another_area_instance.plan_id == another_plan_instance.id
    assert another_line_instance.plan_id == plan_instance.id
    assert another_another_line_instance.plan_id == another_plan_instance.id
    assert another_land_use_point_instance.plan_id == plan_instance.id
    assert another_point_instance.plan_id == another_plan_instance.id

    # Delete created objects from the test database
    session.rollback()


def test_validate_polygon_geometry_triggers(
    session: Session,
    code_instance: codes.LifeCycleStatus,
    type_of_underground_instance: codes.TypeOfUnderground,
    plan_regulation_group_instance: models.PlanRegulationGroup,
    organisation_instance: models.Organisation,
):
    invalid_polygon = MultiPolygon(
        [(((0.0, 0.0), (1.0, 1.0), (0.0, 1.0), (1.0, 0.0)),)]
    )

    invalid_plan_instance = models.Plan(
        geom=from_shape(invalid_polygon),
        lifecycle_status=code_instance,
        organisation=organisation_instance,
    )
    session.add(invalid_plan_instance)
    with pytest.raises(InternalError):
        session.commit()

    session.rollback()
    invalid_land_use_area_instance = models.LandUseArea(
        geom=from_shape(invalid_polygon),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    session.add(invalid_land_use_area_instance)
    with pytest.raises(InternalError):
        session.commit()

    session.rollback()
    invalid_other_area_instance = models.OtherArea(
        geom=from_shape(invalid_polygon),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    session.add(invalid_other_area_instance)
    with pytest.raises(InternalError):
        session.commit()
    session.rollback()


def test_validate_line_geometry(
    session: Session,
    code_instance: codes.LifeCycleStatus,
    type_of_underground_instance: codes.TypeOfUnderground,
    plan_regulation_group_instance: models.PlanRegulationGroup,
):
    # Create line_instance that intersects itself
    another_line_instance = models.Line(
        geom=from_shape(
            MultiLineString(
                [[[0.25, 0.25], [0.75, 0.75]], [[0.25, 0.75], [0.75, 0.25]]]
            )
        ),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
        plan_regulation_groups=[plan_regulation_group_instance],
    )
    with pytest.raises(InternalError):
        session.add(another_line_instance)
        session.commit()
    session.rollback()


def test_overlapping_land_use_area_geometries_trigger(
    session: Session,
    plan_instance: models.Plan,
    code_instance: codes.LifeCycleStatus,
    type_of_underground_instance: codes.TypeOfUnderground,
    plan_regulation_group_instance: models.PlanRegulationGroup,
    rollback_after,
):
    square = MultiPolygon([(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)),)])
    overlapping_square = transform(square, lambda x: x + 0.5)

    land_use_area_instance = models.LandUseArea(
        plan=plan_instance,
        name="area 1",
        geom=from_shape(square),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
    )
    session.add(land_use_area_instance)
    session.flush()

    # Create a new land_use_area that overlaps land_use_area_instance
    new_land_use_area_instance = models.LandUseArea(
        plan=plan_instance,
        name="area 2",
        geom=from_shape(overlapping_square),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
    )

    with pytest.raises(InternalError) as excinfo:
        session.add(new_land_use_area_instance)
        session.flush()
    assert "Geometries overlap" in str(excinfo.value.orig.pgerror)


def test_adjacent_land_use_areas_should_be_fine(
    session: Session,
    plan_instance: models.Plan,
    code_instance: codes.LifeCycleStatus,
    type_of_underground_instance: codes.TypeOfUnderground,
    plan_regulation_group_instance: models.PlanRegulationGroup,
    rollback_after,
):
    square = MultiPolygon([(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)),)])
    adjacent_square = transform(square, lambda vertex: vertex + [1, 0])

    land_use_area_instance = models.LandUseArea(
        plan=plan_instance,
        name="area 1",
        geom=from_shape(square),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
    )
    session.add(land_use_area_instance)
    session.flush()

    # Create a new land_use_area that is adjacent to land_use_area_instance
    new_land_use_area_instance = models.LandUseArea(
        plan=plan_instance,
        name="area 2",
        geom=from_shape(adjacent_square),
        lifecycle_status=code_instance,
        type_of_underground=type_of_underground_instance,
    )

    session.add(new_land_use_area_instance)
    session.flush()

    assert True  # No exception was raised
