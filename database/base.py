import uuid
from datetime import datetime
from typing import Dict, List, Optional

from geoalchemy2 import Geometry
from shapely.geometry import MultiLineString, MultiPoint, MultiPolygon
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, NUMRANGE, UUID, Range
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func
from typing_extensions import Annotated

PROJECT_SRID = 3067


class Base(DeclarativeBase):
    """
    Here we link any postgres specific data types to type annotations.
    """

    type_annotation_map = {
        uuid.UUID: UUID(as_uuid=False),
        dict[str, str]: JSONB,
        MultiLineString: Geometry(geometry_type="MULTILINESTRING", srid=PROJECT_SRID),
        MultiPoint: Geometry(geometry_type="MULTIPOINT", srid=PROJECT_SRID),
        MultiPolygon: Geometry(geometry_type="MULTIPOLYGON", srid=PROJECT_SRID),
        Range[float]: NUMRANGE,
    }


"""
Here we define any custom type annotations we want to use for columns
"""
uuid_pk = Annotated[
    uuid.UUID, mapped_column(primary_key=True, server_default=func.gen_random_uuid())
]
unique_str = Annotated[str, mapped_column(unique=True, index=True)]
language_str = Annotated[
    dict[str, str], mapped_column(server_default='{"fin": "", "swe": "", "eng": ""}')
]
numeric_range = Annotated[Range[float], mapped_column(nullable=True)]
timestamp = Annotated[datetime, mapped_column(server_default=func.now())]

metadata = Base.metadata


class VersionedBase(Base):
    """
    Versioned data tables should have some uniform fields.
    """

    __abstract__ = True
    __table_args__ = {"schema": "hame"}

    # Go figure. We have to *explicitly state* id is a mapped column, because id will
    # have to be defined inside all the subclasses for relationship remote_side
    # definition to work. So even if there is an id field in all the classes,
    # self-relationships will later break if id is only defined by type annotation.
    id: Mapped[uuid_pk] = mapped_column()
    created_at: Mapped[timestamp]
    # TODO: postgresql has no default onupdate. Must implement this with trigger.
    modified_at: Mapped[timestamp]


class CodeBase(VersionedBase):
    """
    Code tables in Ryhti should refer to national Ryhti code table URIs. They may
    have hierarchical structure.
    """

    __abstract__ = True
    __table_args__ = {"schema": "codes"}
    code_list_uri = ""  # the URI to use for looking for codes online
    local_codes: List[Dict] = []  # local codes to add to the code list

    value: Mapped[unique_str]
    short_name: Mapped[str] = mapped_column(server_default="", index=True)
    name: Mapped[language_str]
    description: Mapped[language_str]
    # Let's import code status too. This tells our importer if the koodisto is final,
    # or if the code can be deleted and/or moved.
    status: Mapped[str]
    # For now, level can just be imported from RYTJ. Let's assume the level in RYTJ
    # is correct, so we don't have to calculate and recalculate it ourselves.
    level: Mapped[int] = mapped_column(server_default="1", index=True)

    # self-reference in abstract base class:
    # We cannot use @classmethod decorator here. Alembic is buggy and apparently
    # does not recognize declared attributes that are correctly marked as class methods.
    @declared_attr
    def parent_id(cls) -> Mapped[Optional[uuid.UUID]]:  # noqa
        return mapped_column(
            ForeignKey(cls.id, name=f"{cls.__tablename__}_parent_id_fkey"), index=True
        )

    # Oh great. Unlike SQLAlchemy documentation states, @classmethod decorator should
    # absolutely *not* be used. Declared relationships are not correctly set if the
    # decorator is present.
    @declared_attr
    def parent(cls) -> Mapped[Optional[VersionedBase]]:  # noqa
        return relationship(cls, remote_side=[cls.id], backref="children")

    @property
    def uri(self):
        return f"{self.code_list_uri}/code/{self.value}"


class PlanBase(VersionedBase):
    """
    All plan data tables should have additional date fields.
    """

    __abstract__ = True

    name: Mapped[language_str]
    # Let's have exported at field for all plan data, because some of them may be
    # exported and others added after the plan has last been exported? This will
    # require finding all the exported objects in the database after export is done,
    # is it worth the trouble?
    exported_at: Mapped[Optional[datetime]]

    lifecycle_status_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("codes.lifecycle_status.id", name="plan_lifecycle_status_id_fkey"),
        index=True,
    )

    # class reference in abstract base class, with backreference to class name:
    @declared_attr
    def lifecycle_status(cls) -> Mapped[VersionedBase]:  # noqa
        return relationship(
            "LifeCycleStatus", backref=f"{cls.__tablename__}s", lazy="joined"
        )

    # Let's add backreference to allow lazy loading from this side.
    @declared_attr
    def lifecycle_dates(cls):  # noqa
        return relationship(
            "LifeCycleDate", back_populates=f"{cls.__tablename__}", lazy="joined"
        )


class PlanObjectBase(PlanBase):
    """
    All plan object tables have the same fields, apart from geometry.
    """

    __abstract__ = True

    description: Mapped[language_str]
    source_data_object: Mapped[str] = mapped_column(nullable=True)
    height_range: Mapped[numeric_range]
    height_unit: Mapped[str] = mapped_column(nullable=True)
    ordering: Mapped[Optional[int]] = mapped_column(index=True)
    plan_identifier: Mapped[Optional[str]]  # Kaavatunnus
    type_of_underground_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("codes.type_of_underground.id", name="type_of_underground_id_fkey"),
        index=True,
    )
    plan_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("hame.plan.id", name="plan_id_fkey"), index=True
    )
    plan_regulation_group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "hame.plan_regulation_group.id", name="plan_regulation_group_id_fkey"
        ),
        index=True,
    )

    # class reference in abstract base class, with backreference to class name
    # Let's load all the codes for objects joined.
    @declared_attr
    def type_of_underground(cls) -> Mapped[VersionedBase]:  # noqa
        return relationship(
            "TypeOfUnderground", backref=f"{cls.__tablename__}s", lazy="joined"
        )

    # class reference in abstract base class, with backreference to class name:
    @declared_attr
    def plan(cls) -> Mapped[VersionedBase]:  # noqa
        return relationship("Plan", backref=f"{cls.__tablename__}s")

    # class reference in abstract base class, with backreference to class name:
    @declared_attr
    def plan_regulation_group(cls) -> Mapped[VersionedBase]:  # noqa
        return relationship("PlanRegulationGroup", backref=f"{cls.__tablename__}s")
