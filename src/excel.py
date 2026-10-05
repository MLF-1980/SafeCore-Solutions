from datetime import date
from io import BytesIO

import pandas as pd
from sqlalchemy.orm import Session

from .models import Incident


REQUIRED_COLUMNS = {
    "Fecha",
    "Proyecto",
    "Afectado",
    "Tipo",
    "Descripción",
    "Días Perdidos",
    "Gravedad",
}


def import_incidents_from_excel(file_bytes: bytes, db: Session) -> int:
    try:
        df = pd.read_excel(BytesIO(file_bytes))
    except Exception as exc:
        raise ValueError(f"No se pudo leer el archivo Excel: {exc}") from exc

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError("Faltan columnas obligatorias: " + ", ".join(sorted(missing)))

    records = []

    for index, row in df.iterrows():
        if row.isna().all():
            continue
        try:
            incident_date = pd.to_datetime(row["Fecha"], errors="raise").date()
            lost_days = int(row["Días Perdidos"]) if pd.notna(row["Días Perdidos"]) else 0
            if lost_days < 0:
                raise ValueError("Días Perdidos no puede ser negativo")

            values = {
                "incident_date": incident_date,
                "project_name": str(row["Proyecto"]).strip(),
                "injured_name": str(row["Afectado"]).strip(),
                "person_type": str(row["Tipo"]).strip(),
                "description": str(row["Descripción"]).strip(),
                "lost_days": lost_days,
                "severity_type": str(row["Gravedad"]).strip(),
            }
            if any(not values[key] for key in ("project_name", "injured_name", "person_type", "description", "severity_type")):
                raise ValueError("Hay campos obligatorios vacíos")
            records.append(Incident(**values))
        except Exception as exc:
            db.rollback()
            raise ValueError(f"Error en la fila {index + 2}: {exc}") from exc

    if records:
        db.add_all(records)
        db.commit()

    return len(records)
