from datetime import date

from .database import SessionLocal, init_db
from .repositories import AreaRepository, HazardRepository, IncidentRepository, IPERRepository, PersonnelRepository, PlantRepository


def seed() -> None:
    init_db()
    db = SessionLocal()
    try:
        personnel_repo = PersonnelRepository(db)
        incident_repo = IncidentRepository(db)
        plant_repo = PlantRepository(db)
        area_repo = AreaRepository(db)
        hazard_repo = HazardRepository(db)
        iper_repo = IPERRepository(db)

        existing = personnel_repo.list()
        if not existing:
            for item in [
                {"full_name": "Persona Demo 01", "dni": "30000001", "company": "Propio", "medical_clearance": "Al día", "status": "Apto"},
                {"full_name": "Persona Demo 02", "dni": "30000002", "company": "Contratista A", "medical_clearance": "Al día", "status": "Apto"},
                {"full_name": "Persona Demo 03", "dni": "30000003", "company": "Contratista B", "medical_clearance": "Vencido", "status": "Observado"},
            ]:
                personnel_repo.create(**item)

        if not incident_repo.list():
            for item in [
                {"incident_date": date(2026, 7, 15), "project_name": "Proyecto Demo Norte", "injured_name": "Persona Demo 04", "person_type": "Tercero", "description": "Golpe leve por caída de herramienta.", "lost_days": 3, "severity_type": "Leve"},
                {"incident_date": date(2026, 8, 1), "project_name": "Proyecto Demo Norte", "injured_name": "Persona Demo 02", "person_type": "Propio", "description": "Lesión leve durante tarea de mantenimiento.", "lost_days": 0, "severity_type": "Leve"},
            ]:
                incident_repo.create(**item)

        plants = plant_repo.list()
        if not plants:
            plant = plant_repo.create(name="Planta Demo", region="Buenos Aires")
        else:
            plant = plants[0]

        areas = area_repo.list()
        if not areas:
            area = area_repo.create(name="Mantenimiento", plant_id=plant.id)
        else:
            area = areas[0]

        hazards = hazard_repo.list()
        if not hazards:
            hazard = hazard_repo.create(code="H-001", description="Manipulación de cargas", category="Ergonómico")
        else:
            hazard = hazards[0]

        if not iper_repo.list():
            iper_repo.create(
                area_id=area.id,
                hazard_id=hazard.id,
                process_name="Mantenimiento preventivo",
                task_description="Movimiento y posicionamiento de piezas.",
                risk_level="Importante",
                control_measures="Capacitación, procedimiento de trabajo y EPP adecuado.",
            )

        print("Datos de demostración cargados correctamente.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
