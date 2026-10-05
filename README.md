# SafeCore Solutions

Sistema web de demostración para registrar y consultar información básica de Seguridad, Higiene y Medio Ambiente (HSE), con foco en tres áreas:

- Personal y estado documental.
- Incidentes y días perdidos.
- Matriz IPER (identificación de peligros y evaluación de riesgos).

Además permite importar incidentes desde Excel y consultar un tablero con métricas calculadas a partir de los datos almacenados.

> Este repositorio es un proyecto de portfolio. Los datos de demostración son sintéticos y no representan información de una empresa real.

## Tecnologías

Python, FastAPI, SQLAlchemy, SQLite, Pydantic, Pandas, OpenPyXL, HTML, CSS y JavaScript.

## Estructura

```text
SafeCore-Solutions/
├── src/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── repositories.py
│   ├── services.py
│   ├── excel.py
│   └── static/
│       ├── index.html
│       ├── app.js
│       ├── styles.css
│       └── img/
├── tests/
│   ├── test_services.py
│   └── test_api.py
├── data/
├── .gitignore
├── iniciar.bat
├── requirements.txt
└── README.md
```

## Cómo ejecutar

### 1. Crear entorno virtual

Windows:

```bat
python -m venv .venv
.venv\Scriptsctivate
```

### 2. Instalar dependencias

```bat
pip install -r requirements.txt
```

### 3. Iniciar SafeCore

```bat
uvicorn src.main:app --reload
```

Abrir en el navegador:

`http://127.0.0.1:8000`

Documentación automática de la API:

`http://127.0.0.1:8000/docs`

La base de datos SQLite se crea automáticamente como `safecore.db` en la raíz y queda fuera de Git gracias a `.gitignore`.

## Datos de demostración

Para cargar datos sintéticos y poder mostrar el proyecto funcionando:

```bat
python -m src.seed_demo
```

Esto agrega registros de ejemplo de personal, incidentes, plantas, áreas, peligros e IPER. Los datos están identificados como demostración en el propio script.

## Importación de Excel

La opción de importación espera estas columnas:

```text
Fecha
Proyecto
Afectado
Tipo
Descripción
Días Perdidos
Gravedad
```

El archivo debe ser `.xlsx` o `.xls`.

## Endpoints principales

- `GET /api/health`
- `GET/POST /api/personnel`
- `GET/POST /api/incidents`
- `GET/POST /api/plants`
- `GET/POST /api/areas`
- `GET/POST /api/hazards`
- `GET/POST /api/iper`
- `GET /api/dashboard`
- `POST /api/import-excel`
- `GET /api/export/incidents.csv`

## Criterio de diseño

La versión anterior mezclaba varias arquitecturas, modelos duplicados, bases SQLite diferentes, migraciones incompatibles y archivos de entorno que no debían estar en el repositorio. Esta versión unifica la aplicación en una sola arquitectura y evita datos de negocio hardcodeados en el código de producción.
