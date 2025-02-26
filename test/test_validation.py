from datetime import datetime, timedelta

import pytest
from geoalchemy2.shape import from_shape
from shapely import transform
from shapely.geometry import MultiLineString, MultiPolygon
from sqlalchemy.exc import InternalError
from sqlalchemy.orm import Session

from database import codes, models


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


def test_validate_lifecycle_dates(
    session: Session,
    plan_instance: models.Plan,
    lifecycle_date_instance: models.LifeCycleDate,
):
    assert lifecycle_date_instance.starting_at < lifecycle_date_instance.ending_at
    session.add(lifecycle_date_instance)
    # check that modified date cannot start after ending
    with pytest.raises(InternalError):
        lifecycle_date_instance.starting_at = (
            lifecycle_date_instance.ending_at + timedelta(days=1)
        )
        session.flush()
    session.rollback()
    # check that new date cannot start after ending
    with pytest.raises(InternalError):
        new_lifecycle_date_instance = models.LifeCycleDate(
            plan=plan_instance,
            starting_at=datetime.now() + timedelta(days=1),
            ending_at=datetime.now(),
        )
        session.add(new_lifecycle_date_instance)
        session.flush()
    session.rollback()


def test_validate_event_dates(
    session: Session,
    preparation_date_instance: models.LifeCycleDate,
    interaction_event_date_instance: models.EventDate,
):
    assert (
        interaction_event_date_instance.starting_at
        < interaction_event_date_instance.ending_at
    )
    session.add(interaction_event_date_instance)
    # check that modified event cannot start after ending
    with pytest.raises(InternalError):
        interaction_event_date_instance.starting_at = (
            interaction_event_date_instance.ending_at + timedelta(days=1)
        )
        session.flush()
    session.rollback()
    # check that new event cannot start after ending
    with pytest.raises(InternalError):
        new_event_date_instance = models.EventDate(
            lifecycle_date=preparation_date_instance,
            starting_at=datetime.now() + timedelta(days=1),
            ending_at=datetime.now(),
        )
        session.add(new_event_date_instance)
        session.flush()
    session.rollback()


def test_validate_event_dates_inside_status_dates(
    session: Session,
    preparation_date_instance: models.LifeCycleDate,
    interaction_event_date_instance: models.EventDate,
):
    assert (
        interaction_event_date_instance.starting_at
        > preparation_date_instance.starting_at
    )
    assert (
        interaction_event_date_instance.ending_at < preparation_date_instance.ending_at
    )
    # check that modified event cannot start before status starts
    with pytest.raises(InternalError):
        interaction_event_date_instance.starting_at = (
            preparation_date_instance.starting_at - timedelta(days=1)
        )
        session.flush()
    session.rollback()
    # check that modified event cannot end after status ends
    with pytest.raises(InternalError):
        interaction_event_date_instance.ending_at = (
            preparation_date_instance.ending_at + timedelta(days=1)
        )
        session.flush()
    session.rollback()
    # check that new event cannot start before status starts
    with pytest.raises(InternalError):
        new_event_date_instance = models.EventDate(
            lifecycle_date=preparation_date_instance,
            starting_at=preparation_date_instance.starting_at - timedelta(days=1),
        )
        session.add(new_event_date_instance)
        session.flush()
    session.rollback()
    # check that new event cannot end after status ends
    with pytest.raises(InternalError):
        new_event_date_instance = models.EventDate(
            lifecycle_date=preparation_date_instance,
            starting_at=preparation_date_instance.ending_at + timedelta(days=1),
        )
        session.add(new_event_date_instance)
        session.flush()
    session.rollback()


def test_validate_event_types(
    session: Session,
    preparation_date_instance: models.LifeCycleDate,
    approved_date_instance: models.LifeCycleDate,
    decision_date_instance: models.EventDate,
    participation_plan_presenting_for_public_decision: codes.NameOfPlanCaseDecision,
    plan_proposal_presenting_for_public_decision: codes.NameOfPlanCaseDecision,
):
    assert decision_date_instance.lifecycle_date == preparation_date_instance
    assert (
        decision_date_instance.decision
        == participation_plan_presenting_for_public_decision
    )
    session.add(decision_date_instance)
    # check that modified event cannot be added to wrong status
    with pytest.raises(InternalError):
        decision_date_instance.lifecycle_date = approved_date_instance
        decision_date_instance.starting_at = approved_date_instance.starting_at
        decision_date_instance.ending_at = (
            approved_date_instance.starting_at + timedelta(days=30)
        )
        session.flush()
    session.rollback()
    # check that modified event cannot be added to wrong event type
    with pytest.raises(InternalError):
        decision_date_instance.decision = plan_proposal_presenting_for_public_decision
        session.flush()
    session.rollback()
    # check that new event cannot be added to wrong status/event type combination
    with pytest.raises(InternalError):
        new_event_date_instance = models.EventDate(
            lifecycle_date=approved_date_instance,
            starting_at=approved_date_instance.starting_at,
            decision=participation_plan_presenting_for_public_decision,
        )
        session.add(new_event_date_instance)
        session.flush()
    session.rollback()
