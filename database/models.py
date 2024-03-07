import uuid
from datetime import datetime
from typing import Literal, Optional

# we have to import CodeBase in codes.py from here to allow two-way relationships
from base import (  # noqa
    CodeBase,
    PlanBase,
    PlanObjectBase,
    VersionedBase,
    autoincrement_int,
    language_str,
    numeric_range,
    timestamp,
    unique_str,
)
from shapely.geometry import MultiLineString, MultiPoint, MultiPolygon
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Plan(PlanBase):
    """
    Maakuntakaava, compatible with Ryhti 2.0 specification
    """

    __tablename__ = "plan"

    organisation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hame.organisation.id", name="organisation_id_fkey")
    )

    approved_at: Mapped[Optional[datetime]]
    geom: Mapped[MultiPolygon]


class LandUseArea(PlanObjectBase):
    """
    Osa-alue
    """

    __tablename__ = "land_use_area"

    geom: Mapped[MultiPolygon]


class OtherArea(PlanObjectBase):
    """
    Aluevaraus
    """

    __tablename__ = "other_area"

    geom: Mapped[MultiPolygon]


class Line(PlanObjectBase):
    """
    Viivat
    """

    __tablename__ = "line"

    geom: Mapped[MultiLineString]


class LandUsePoint(PlanObjectBase):
    """
    Maankäytön pisteet
    """

    __tablename__ = "land_use_point"

    geom: Mapped[MultiPoint]


class OtherPoint(PlanObjectBase):
    """
    Muut pisteet
    """

    __tablename__ = "other_point"

    geom: Mapped[MultiPoint]


class PlanRegulationGroup(VersionedBase):
    """
    Kaavamääräysryhmä
    """

    __tablename__ = "plan_regulation_group"

    short_name: Mapped[unique_str]
    name: Mapped[language_str]
    # värikoodi?
    # group_type: oma koodilista


class PlanRegulation(PlanBase):
    """
    Kaavamääräys
    """

    __tablename__ = "plan_regulation"

    plan_regulation_group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "hame.plan_regulation_group.id", name="plan_regulation_group_id_fkey"
        )
    )

    type_of_plan_regulation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "codes.type_of_plan_regulation.id", name="type_of_plan_regulation_id_fkey"
        )
    )
    type_of_verbal_plan_regulation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "codes.type_of_verbal_plan_regulation.id",
            name="type_of_verbal_plan_regulation_id_fkey",
        ),
        nullable=True,
    )
    # type_of_additional_information_id: Mapped[uuid.UUID] = mapped_column(
    #     ForeignKey(
    #         "codes.type_of_additional_information.id",
    #         name="type_of_additional_information_id_fkey",
    #     )
    # )

    plan_regulation_group = relationship(
        "PlanRegulationGroup", backref="plan_regulations"
    )
    type_of_plan_regulation = relationship(
        "TypeOfPlanRegulation", backref="plan_regulations"
    )
    # plan_theme: kaavoitusteema-koodilista
    type_of_verbal_plan_regulation = relationship(
        "TypeOfVerbalPlanRegulation", backref="plan_regulations"
    )
    numeric_range: Mapped[numeric_range]
    unit: Mapped[str] = mapped_column(nullable=True)
    text_value: Mapped[language_str]
    numeric_value: Mapped[float] = mapped_column(nullable=True)
    ordering: Mapped[autoincrement_int]
    # ElinkaaritilaX_pvm?


class PlanProposition(PlanBase):
    """
    Kaavasuositus
    """

    __tablename__ = "plan_proposition"

    plan_regulation_group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "hame.plan_regulation_group.id", name="plan_regulation_group_id_fkey"
        )
    )

    plan_regulation_group = relationship(
        "PlanRegulationGroup", backref="plan_propositions"
    )
    text_value: Mapped[language_str]
    ordering: Mapped[autoincrement_int]
    # plan_theme: kaavoitusteema-koodilista
    # ElinkaaritilaX_pvm


class SourceData(VersionedBase):
    """
    Lähtötietoaineistot
    """

    __tablename__ = "source_data"

    type_of_source_data_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("codes.type_of_source_data.id", name="type_of_source_data_id_fkey")
    )

    type_of_source_data = relationship("TypeOfSourceData", backref="source_data")
    name: Mapped[language_str]
    additional_information_uri: Mapped[str]


class Organisation(VersionedBase):
    """
    Toimija
    """

    __tablename__ = "organisation"

    name: Mapped[language_str]
    business_id: Mapped[str]
    # administrative_region_id: koodilista


class Document(VersionedBase):
    """
    Asiakirja
    """

    __tablename__ = "document"

    type_of_document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("codes.type_of_document.id", name="type_of_document_id_fkey")
    )
    plan_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hame.plan.id", name="plan_id_fkey")
    )

    type_of_document = relationship("TypeOfDocument", backref="documents")
    plan = relationship("Plan", backref="documents")
    name: Mapped[str]
    personal_details: Mapped[str]
    publicity: Mapped[Literal["julkinen", "ei julkinen"]]  # Muita?
    language: Mapped[str]
    decision: Mapped[bool]
    decision_date: Mapped[Optional[timestamp]]
    # file


class View(VersionedBase):
    """
    Virtuaalitaso/näkymä
    """

    __tablename___ = "view"

    land_use_area_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hame.land_use_area.id", name="land_use_area_id_fkey")
    )

    other_area_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hame.other_area.id", name="other_area_id_fkey")
    )

    line_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hame.line.id", name="line_id_fkey")
    )

    land_use_point_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hame.land_use_point.id", name="land_use_point_id_fkey")
    )

    other_point_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hame.other_point.id", name="other_point_id_fkey")
    )
    # plan_regulation_group_name = relationship()
    description: Mapped[language_str]
    ordering: Mapped[autoincrement_int]
    short_name: Mapped[unique_str]
    # color: Mapped[str]
    # combined_text?
