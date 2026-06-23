# 🛡️ SafeCore Solutions v1.2 - Control & Auditoría HSE

**SafeCore Solutions** es un sistema inteligente desarrollado en Python diseñado para transformar los datos operativos de Higiene, Seguridad y Medio Ambiente (HSE) en dashboards de control gerencial automatizados. 

El sistema elimina el uso ineficiente de planillas de cálculo tradicionales y centraliza la auditoría de personal operativo, vigencia de EPP y cumplimiento normativo de subcontratistas externos.

---

## 🎯 Enfoque Estratégico e Impacto del Negocio

Este software ha sido diseñado bajo una estructura **modular y altamente escalable**, orientada a resolver las problemáticas reales de las industrias de alta complejidad (Construcción, Minería, Petróleo y Gas):

* **Reducción del Riesgo Legal:** Automatiza el control de subcontratistas externos bloqueando alertas en caso de ARTs vencidas o inducciones de ingreso pendientes.
* **Optimización del Gasto Operativo:** Sistema dinámico que calcula los ciclos de recambio de EPP ajustándose automáticamente al marco regulatorio del rubro de la empresa.
* **Visión Global Corporativa:** Genera de manera autónoma archivos de exportación en formato estructurado de datos, listos para ser consumidos por la alta dirección y gerencias generales.
* **Arquitectura de Exportación (Ready for Global Markets):** La capa lógica está completamente disociada de las reglas locales de localización, permitiendo que el software sea parametrizable y escalable a normativas internacionales como **OSHA (EE. UU.)** o **ISO 45001**.

---

## 🛠️ Arquitectura Técnico y Características

La aplicación implementa conceptos avanzados de ingeniería de software en Python:

1.  **Programación Orientada a Objetos (POO):** Modularización completa utilizando clases y encapsulamiento robusto del flujo del negocio.
2.  **Persistencia de Datos Local (JSON Engine):** Base de datos relacional simplificada en formato JSON local con codificación de texto universal UTF-8 para garantizar que no haya pérdida de datos operacionales entre sesiones.
3.  **Inyección Dinámica de Funciones:** Mecanismo avanzado utilizado para inyectar los módulos de estadísticas analíticas e intercepción de funciones gerenciales sin comprometer el núcleo (Core Engine) de la aplicación original.
4.  **BOM UTF-8-sig CSV Exportador:** Módulo gerencial optimizado para generar planillas CSV con los delimitadores locales estándar (`;`) y firmas binarias necesarias para que los directores puedan abrir los reportes en Microsoft Excel de forma nativa con un doble clic.

---

## 📊 Módulos Corporativos Implementados

Al ejecutar el comando de auditoría masiva (**Opción 3**), el motor procesa el estado del personal y exporta automáticamente tres reportes clave independientes:

| Archivo Generado | Audiencia Objetivo | Indicadores y KPIs Incluidos |
| :--- | :--- | :--- |
| `reporte_personal_capacitaciones.csv` | Jefes de Planta / Capataces | Nombre, Puesto de Trabajo, Meses Uso EPP, Estado y Fecha de Inducción. |
| `dashboard_estadisticas_gerenciales.csv`| Directores Generales / CEO | Días Acumulados Sin Accidentes, Frecuencia de Siniestros, Meta Anual de Días Seguros. |
| `control_subcontratistas.csv` | Auditoría Interna / Legales | Empresa Externa, Gremio, Validación de Seguro de ART, Porcentaje de Cumplimiento. |

---

## 🚀 Guía de Uso del Sistema

### Prerrequisitos
* Tener instalado Python 3.8 o superior.
* No requiere instalar ninguna biblioteca externa (Zero Dependencies System).

### Ejecución
1. Clona este repositorio o descarga el archivo `SafeCore Solutions.py`.
2. Ejecuta el script desde tu terminal o consola Git Bash:
```bash
   python "SafeCore Solutions.py"
