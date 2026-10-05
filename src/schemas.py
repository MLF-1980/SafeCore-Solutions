from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


def clean_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("El campo no puede estar vacio.")
    return value


class PersonnelCreate(BaseModel):
    full_name: str
    dni: str
    company: str
    medical_clearance: str
    status: str

    _clean = field_validator(
        "full_name", "dni", "company", "medical_clearance", "status"
    )(clean_text)


class PersonnelResponse(PersonnelCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class IncidentCreate(BaseModel):
    incident_date: date
    project_name: str
    injured_name: str
    person_type: str
    description: str
    lost_days: int = Field(default=0, ge=0)
    severity_type: str

    _clean = field_validator(
        "project_name", "injured_name", "person_type", "description", "severity_type"
    )(clean_text)


class IncidentResponse(IncidentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class PlantCreate(BaseModel):
    name: str
    region: str
    _clean = field_validator("name", "region")(clean_text)


class PlantResponse(PlantCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AreaCreate(BaseModel):
    name: str
    plant_id: int = Field(gt=0)
    _clean = field_validator("name")(clean_text)


class AreaResponse(AreaCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class HazardCreate(BaseModel):
    code: str
    description: str
    category: str

    _clean = field_validator("code", "description", "category")(clean_text)


class HazardResponse(HazardCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class IPERCreate(BaseModel):
    area_id: int = Field(gt=0)
    hazard_id: int = Field(gt=0)
    process_name: str
    task_description: str
    risk_level: str
    control_measures: str | None = None

    _clean = field_validator(
        "process_name", "task_description", "risk_level"
    )(clean_text)


class IPERResponse(IPERCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class DashboardResponse(BaseModel):
    period: str
    incidents: int
    lost_days: int
    personnel: int
    iper_records: int
    critical_risk_records: int
    incidents_by_person_type: dict[str, int]
    incidents_by_severity: dict[str, int]
