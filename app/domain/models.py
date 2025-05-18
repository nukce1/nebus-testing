from typing import List

from database import (
    Base,
    intpk,
)
from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(255))
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    building: Mapped["Building"] = relationship(back_populates="organizations")
    activities: Mapped[List["Activity"]] = relationship(secondary=organization_activity, back_populates="organizations")


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[intpk]
    address: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float]
    longitude: Mapped[float]
    organizations: Mapped[List[Organization]] = relationship(back_populates="building")

    __table_args__ = (
        CheckConstraint("latitude >= -90 AND latitude <= 90", name="latitude_range_check"),
        CheckConstraint("longitude >= -180 AND latitude <= 180", name="longitude_range_check"),
    )


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50))
    organizations: Mapped[List[Organization]] = relationship(
        secondary=organization_activity, back_populates="activities"
    )


class ActivityClosure(Base):
    __tablename__ = "activities_closures"

    id: Mapped[intpk]
    ancestor_id: Mapped[int] = mapped_column(ForeignKey("activities.id", ondelete="CASCADE"))
    descendant_id: Mapped[int] = mapped_column(ForeignKey("activities.id", ondelete="CASCADE"))
    depth: Mapped[int]

    __table_args__ = (UniqueConstraint("ancestor_id", "descendant_id", name="uq_ancestor_descendant"),)
