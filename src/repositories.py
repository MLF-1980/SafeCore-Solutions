from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Area, HazardCatalog, IPERRecord, Incident, Personnel, Plant


class PersonnelRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Personnel]:
        return list(self.db.scalars(select(Personnel).order_by(Personnel.id.desc())))

    def create(self, **data) -> Personnel:
        record = Personnel(**data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record


class IncidentRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, start: date | None = None, end: date | None = None) -> list[Incident]:
        stmt = select(Incident).order_by(Incident.incident_date.desc(), Incident.id.desc())
        if start:
            stmt = stmt.where(Incident.incident_date >= start)
        if end:
            stmt = stmt.where(Incident.incident_date < end)
        return list(self.db.scalars(stmt))

    def create(self, **data) -> Incident:
        record = Incident(**data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record


class PlantRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Plant]:
        return list(self.db.scalars(select(Plant).order_by(Plant.name)))

    def create(self, **data) -> Plant:
        record = Plant(**data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record


class AreaRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[Area]:
        return list(self.db.scalars(select(Area).order_by(Area.name)))

    def create(self, **data) -> Area:
        record = Area(**data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record


class HazardRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[HazardCatalog]:
        return list(self.db.scalars(select(HazardCatalog).order_by(HazardCatalog.code)))

    def create(self, **data) -> HazardCatalog:
        record = HazardCatalog(**data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record


class IPERRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[IPERRecord]:
        stmt = select(IPERRecord).order_by(IPERRecord.id.desc())
        return list(self.db.scalars(stmt))

    def create(self, **data) -> IPERRecord:
        record = IPERRecord(**data)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
