import csv
from contextlib import asynccontextmanager
from io import StringIO

from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .database import get_db, init_db
from .excel import import_incidents_from_excel
from .repositories import (
    AreaRepository,
    HazardRepository,
    IncidentRepository,
    IPERRepository,
    PersonnelRepository,
    PlantRepository,
)
from .schemas import (
    AreaCreate,
    AreaResponse,
    DashboardResponse,
    HazardCreate,
    HazardResponse,
    IncidentCreate,
    IncidentResponse,
    IPERCreate,
    IPERResponse,
    PersonnelCreate,
    PersonnelResponse,
    PlantCreate,
    PlantResponse,
)
from .services import dashboard_metrics


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="SafeCore Solutions API",
    version="2.0.0",
    description="Registro HSE, incidentes e IPER con SQLite y FastAPI.",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse("src/static/index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "SafeCore Solutions", "version": "2.0.0"}


@app.get("/api/personnel", response_model=list[PersonnelResponse], tags=["Personal"])
def list_personnel(db: Session = Depends(get_db)):
    return PersonnelRepository(db).list()


@app.post("/api/personnel", response_model=PersonnelResponse, status_code=201, tags=["Personal"])
def create_personnel(data: PersonnelCreate, db: Session = Depends(get_db)):
    try:
        return PersonnelRepository(db).create(**data.model_dump())
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="El DNI ya existe.") from exc


@app.get("/api/incidents", response_model=list[IncidentResponse], tags=["Incidentes"])
def list_incidents(db: Session = Depends(get_db)):
    return IncidentRepository(db).list()


@app.post("/api/incidents", response_model=IncidentResponse, status_code=201, tags=["Incidentes"])
def create_incident(data: IncidentCreate, db: Session = Depends(get_db)):
    return IncidentRepository(db).create(**data.model_dump())


@app.get("/api/plants", response_model=list[PlantResponse], tags=["IPER"])
def list_plants(db: Session = Depends(get_db)):
    return PlantRepository(db).list()


@app.post("/api/plants", response_model=PlantResponse, status_code=201, tags=["IPER"])
def create_plant(data: PlantCreate, db: Session = Depends(get_db)):
    try:
        return PlantRepository(db).create(**data.model_dump())
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="La planta ya existe.") from exc


@app.get("/api/areas", response_model=list[AreaResponse], tags=["IPER"])
def list_areas(db: Session = Depends(get_db)):
    return AreaRepository(db).list()


@app.post("/api/areas", response_model=AreaResponse, status_code=201, tags=["IPER"])
def create_area(data: AreaCreate, db: Session = Depends(get_db)):
    return AreaRepository(db).create(**data.model_dump())


@app.get("/api/hazards", response_model=list[HazardResponse], tags=["IPER"])
def list_hazards(db: Session = Depends(get_db)):
    return HazardRepository(db).list()


@app.post("/api/hazards", response_model=HazardResponse, status_code=201, tags=["IPER"])
def create_hazard(data: HazardCreate, db: Session = Depends(get_db)):
    try:
        return HazardRepository(db).create(**data.model_dump())
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="El código de peligro ya existe.") from exc


@app.get("/api/iper", response_model=list[IPERResponse], tags=["IPER"])
def list_iper(db: Session = Depends(get_db)):
    return IPERRepository(db).list()


@app.post("/api/iper", response_model=IPERResponse, status_code=201, tags=["IPER"])
def create_iper(data: IPERCreate, db: Session = Depends(get_db)):
    return IPERRepository(db).create(**data.model_dump())


@app.get("/api/dashboard", response_model=DashboardResponse, tags=["Dashboard"])
def dashboard(period: str = Query("ALL"), db: Session = Depends(get_db)):
    try:
        return dashboard_metrics(db, period)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/import-excel", tags=["Importación"])
async def import_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = file.filename or ""
    if not filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="El archivo debe ser .xlsx o .xls.")

    content = await file.read()
    try:
        imported = import_incidents_from_excel(content, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "ok", "imported": imported}


@app.get("/api/export/incidents.csv", tags=["Exportación"])
def export_incidents(db: Session = Depends(get_db)):
    incidents = IncidentRepository(db).list()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Fecha", "Proyecto", "Afectado", "Tipo", "Descripción", "Días Perdidos", "Gravedad"
    ])
    for item in incidents:
        writer.writerow([
            item.id,
            item.incident_date.isoformat(),
            item.project_name,
            item.injured_name,
            item.person_type,
            item.description,
            item.lost_days,
            item.severity_type,
        ])
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=incidentes.csv"},
    )
