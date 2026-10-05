from datetime import date, datetime, timezone

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Personnel(Base):
    __tablename__ = "personnel"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    dni: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    company: Mapped[str] = mapped_column(String(150), nullable=False)
    medical_clearance: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    incident_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    project_name: Mapped[str] = mapped_column(String(150), nullable=False)
    injured_name: Mapped[str] = mapped_column(String(150), nullable=False)
    person_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    lost_days: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    severity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )


class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    region: Mapped[str] = mapped_column(String(100), nullable=False)

    areas: Mapped[list["Area"]] = relationship(
        back_populates="plant", cascade="all, delete-orphan"
    )


class Area(Base):
    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id"), nullable=False)

    plant: Mapped[Plant] = relationship(back_populates="areas")
    iper_records: Mapped[list["IPERRecord"]] = relationship(back_populates="area")


class HazardCatalog(Base):
    __tablename__ = "hazard_catalog"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)

    iper_records: Mapped[list["IPERRecord"]] = relationship(back_populates="hazard")


class IPERRecord(Base):
    __tablename__ = "iper_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    area_id: Mapped[int] = mapped_column(ForeignKey("areas.id"), nullable=False)
    hazard_id: Mapped[int] = mapped_column(ForeignKey("hazard_catalog.id"), nullable=False)
    process_name: Mapped[str] = mapped_column(String(150), nullable=False)
    task_description: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False)
    control_measures: Mapped[str | None] = mapped_column(Text)

    area: Mapped[Area] = relationship(back_populates="iper_records")
    hazard: Mapped[HazardCatalog] = relationship(back_populates="iper_records")
