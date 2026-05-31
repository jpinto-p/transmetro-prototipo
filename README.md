Sistema de Control de Transmetro

Prototipo funcional desarrollado para la Municipalidad de Guatemala. Proporciona una plataforma web para la gestión operativa y el monitoreo en tiempo real del sistema de transporte Transmetro.

Propósito del proyecto

El sistema atiende problemas reales de seguridad, control de flujo y eficiencia operativa mediante herramientas digitales. Permite administrar líneas, estaciones, buses, pilotos y parqueos, así como registrar distancias entre estaciones y monitorear aforo con alertas automáticas.

Tecnologías utilizadas

- Python 3.12 con **Flask** (backend y lógica de rutas)
- SQLite como motor de base de datos relacional
- SQLAlchemy (ORM) para la gestión de modelos
- Flask-Login para autenticación de administrador
- WTForms para la validación y manejo de formularios
- Bootstrap 5 para el diseño responsivo
- JavaScript (Fetch API, Chart.js)** para actualizaciones dinámicas y gráficos
- GitHub Actions para despliegue continuo en Azure

 Contenido del repositorio (archivos principales)

| Archivo / Carpeta | Descripción técnica |
|------------------|----------------------|
| `app.py` | Controlador principal: rutas, lógica de negocio, endpoints de API y configuración de la aplicación. |
| `models.py` | Definición de las 11 clases del modelo de datos (Línea, Estación, Bus, Piloto, Parqueo, Acceso, Guardia, Distancia, HistorialParqueo, etc.). |
| `forms.py` | Formularios WTForms para la captura y validación de datos en cada módulo del CRUD. |
| `templates/` | Plantillas HTML (Jinja2) que estructuran la interfaz de usuario: dashboards, listados, formularios y monitoreo. |
| `static/` | Archivos estáticos: hojas de estilo CSS, imágenes (logos del Transmetro) y recursos gráficos. |
| `seed.py` | Script de población de base de datos con datos de ejemplo realistas (líneas, estaciones, distancias, pilotos, buses). |
| `requirements.txt` | Dependencias del proyecto con versiones fijas para garantizar reproducibilidad. |
| `.github/workflows/` | Flujo de trabajo para despliegue automático en Azure App Service mediante GitHub Actions. |

Estado actual

El prototipo es completamente funcional en entorno local y cumple con la totalidad de los requerimientos priorizados (REQ-001 a REQ-014). La aplicación está preparada para ser desplegada en la nube (Azure App Service) con persistencia de base de datos SQLite mediante variables de entorno.

Autor

**Jermi Pinto** – Proyecto académico para la Municipalidad de Guatemala.
