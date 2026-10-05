from datetime import date

from src.repositories import IncidentRepository, IPERRepository, PersonnelRepository
from src.services import dashboard_metrics


def test_dashboard_metrics(db):
    PersonnelRepository(db).create(
        full_name="Persona Test", dni="99999999", company="Propio",
        medical_clearance="Al día", status="Apto"
    )
    IncidentRepository(db).create(
        incident_date=date(2026, 8, 10), project_name="Obra Test",
        injured_name="Persona Test", person_type="Propio",
        description="Incidente de prueba", lost_days=4, severity_type="Leve"
    )
    metrics = dashboard_metrics(db, "2026-08")
    assert metrics["incidents"] == 1
    assert metrics["lost_days"] == 4
    assert metrics["personnel"] == 1
    assert metrics["incidents_by_person_type"] == {"Propio": 1}


def test_critical_risk_count(db):
    from src.repositories import AreaRepository, HazardRepository, PlantRepository
    plant = PlantRepository(db).create(name="Planta Test", region="BA")
    area = AreaRepository(db).create(name="Area Test", plant_id=plant.id)
    hazard = HazardRepository(db).create(code="T-001", description="Peligro test", category="Mecánico")
    IPERRepository(db).create(
        area_id=area.id, hazard_id=hazard.id, process_name="Proceso",
        task_description="Tarea", risk_level="Importante", control_measures="Control"
    )
    metrics = dashboard_metrics(db)
    assert metrics["critical_risk_records"] == 1
