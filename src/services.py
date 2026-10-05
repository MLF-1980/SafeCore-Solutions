from collections import Counter
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import IPERRecord, Incident, Personnel


CRITICAL_RISK_LEVELS = {"Importante", "Intolerable", "Crítico", "Critico", "Alto"}


def dashboard_metrics(db: Session, period: str = "ALL") -> dict:
    start = end = None
    if period != "ALL":
        try:
            year, month = (int(part) for part in period.split("-"))
            start = date(year, month, 1)
            end = date(year + (month == 12), 1 if month == 12 else month + 1, 1)
        except (TypeError, ValueError):
            raise ValueError("El periodo debe tener formato YYYY-MM o ALL.")

    stmt = select(Incident).order_by(Incident.id)
    if start:
        stmt = stmt.where(Incident.incident_date >= start, Incident.incident_date < end)
    incidents = list(db.scalars(stmt))

    type_counts = Counter(item.person_type for item in incidents)
    severity_counts = Counter(item.severity_type for item in incidents)

    critical_stmt = select(func.count(IPERRecord.id)).where(IPERRecord.risk_level.in_(CRITICAL_RISK_LEVELS))
    critical_risk_records = db.scalar(critical_stmt) or 0

    return {
        "period": period,
        "incidents": len(incidents),
        "lost_days": sum(item.lost_days for item in incidents),
        "personnel": db.scalar(select(func.count(Personnel.id))) or 0,
        "iper_records": db.scalar(select(func.count(IPERRecord.id))) or 0,
        "critical_risk_records": critical_risk_records,
        "incidents_by_person_type": dict(type_counts),
        "incidents_by_severity": dict(severity_counts),
    }
