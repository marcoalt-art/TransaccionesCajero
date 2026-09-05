# Monitoreo NoSQL y Detección de Irregularidades Financieras (UIF) con MongoDB, Prometheus y Grafana

Proyecto aplicado que simula un pipeline de procesamiento e ingesta de transacciones de cajeros automáticos (ATM) en Bolivia (un caso típico de Big Data: alto volumen, alta velocidad de ingesta, datos sensibles y análisis NoSQL), instrumentado de punta a punta para:

* **Monitorear el rendimiento del pipeline en tiempo real** con Prometheus + Grafana.
* **Persistir y auditar datos transaccionales** en MongoDB con esquemas BSON flexibles para auditoría bancaria y reportes regionales.
* **Detectar automáticamente alertas UIF** (Unidad de Investigaciones Financieras) como retiros iguales o superiores a 10,000 Bs, excesos de límite y discrepancias físico-lógicas entre lo solicitado y lo dispensado.
* **Gestionar la base de datos NoSQL** mediante una consola interactiva CLI para operaciones CRUD completas.
* **Aplicar un checklist de buenas prácticas de seguridad y auditoría de datos sensibles.**

Todo el proyecto está pensado para ejecutarse localmente desde **Visual Studio Code** en un entorno Windows.

---

## 1. Arquitectura del proyecto

```text
┌──────────────────────────────┐        scrape /metrics                 ┌──────────────┐        datasource                  ┌──────────┐
│  simulador_cajero.py         │ ─────────────────────────────▶│  Prometheus  │ ─────────────────────────▶│ Grafana  │
│  (VS Code, entorno local)    │   puertos 8000 / 8001                  │  (Binario,   │   puerto 9090                     │ (Binario,│
│                              │                                        │  puerto 9090)│                                   │ puerto   │
│  1. Generación/Ingesta       │                                        └──────────────┘                                   │ 3000)    │
│  2. Reglas UIF & Alertas     │                                                                                           └──────────┘
│  3. Exposición de Métricas   │
│  4. Carga (MongoDB local)    │
└──────────────┬───────────────┘
               │
               │ consultas CRUD / persistencia
               ▼
┌──────────────────────────────┐
│  MongoDB (banco_db)          │
│  - transacciones_cajero      │
└──────────────────────────────┘
El pipeline Python corre nativo en tu máquina Windows (dentro de un entorno virtual .venv) para que puedas depurarlo paso a paso desde VS Code.
MongoDB, Prometheus y Grafana corren como servicios/binarios locales y constituyen la capa NoSQL y la infraestructura de observabilidad.

2. Estructura de carpetas
TransaccionesCajero/
├── requirements.txt            # Dependencias Python del proyecto (pymongo, prometheus_client)
├── .env.example                 # Plantilla de variables de entorno (parámetros de MongoDB y puertos)
├── prometheus.yml              # Configuración de scraping y targets para Prometheus
├── simulador_cajero.py       # Motor de simulación transaccional, reglas UIF y servidor HTTP de métricas
├── crud_mongodb.py           # Interfaz interactiva CLI para operaciones CRUD directas en MongoDB
├── importar_csv_mongo.py     # Script de carga masiva inicial e ingesta NoSQL desde archivos CSV
└── docs/
    └── checklist_seguridad.md    # Checklist de buenas prácticas de seguridad y cumplimiento UIF
3. Requisitos previos
Visual Studio Code

Python 3.10+ (Python 3.12 recomendado)

MongoDB Community Server o MongoDB Compass corriendo en localhost:27017

Prometheus Binario para Windows (puerto 9090)

Grafana Enterprise/OSS para Windows (puerto 3000)

4. Puesta en marcha paso a paso
Paso 1 — Abrir el proyecto en VS Code
Descomprime el archivo del proyecto y ábrelo con Archivo > Abrir carpeta... en VS Code, seleccionando la carpeta TransaccionesCajero.

Paso 2 — Crear el entorno virtual e instalar dependencias
Abre la terminal integrada de VS Code (Ctrl+ñ / Ctrl+Shift+P → Terminal: Create New Terminal) y ejecuta:

Windows (PowerShell):
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Paso 3 — Configurar las variables de entorno
Crea tu archivo .env a partir de la plantilla .env.example:
copy .env.example .env

Abre .env en VS Code y verifica los parámetros de conexión:
MONGO_URI=mongodb://localhost:27017/
MONGO_DB=banco_db
MONGO_COLLECTION=transacciones_cajero
PROMETHEUS_PORT=8000

aso 4 — Iniciar MongoDB y verificar conexión
Asegúrate de que el servicio local de MongoDB esté en ejecución. Puedes comprobar la conectividad ejecutando en terminal:
python -c "import pymongo; client = pymongo.MongoClient('mongodb://localhost:27017/'); print('Conexión exitosa:', client.list_database_names())"

Paso 5 — Carga inicial masiva de datos (Opcional)
Para poblar la base de datos NoSQL con el registro histórico de transacciones, ejecuta:
python importar_csv_mongo.py

Paso 6 — Iniciar Prometheus y Grafana
Prometheus: Abre una nueva terminal en PowerShell, navega al directorio del binario de Prometheus y ejecuta:
.\prometheus.exe --config.file=prometheus.yml
Acceso Web: http://localhost:9090

Verifica los targets en http://localhost:9090/targets para confirmar que cajero_bolivia figura en estado UP.

Grafana: Inicia el ejecutable de Grafana en Windows.

Acceso Web: http://localhost:3000 (usuario admin, contraseña admin).

Añade Prometheus como Data Source conectándolo a http://localhost:9090.

Paso 7 — Ejecutar los componentes del proyecto
Tienes tres formas de ejecutar y probar el pipeline:

Opción A — Ejecución continua del simulador de cajeros (Recomendado):
Abre la terminal integrada y ejecuta:
python simulador_cajero.py
(Inicia la generación continua de transacciones, aplica el motor de reglas UIF, persiste documentos BSON en MongoDB y expone métricas en http://localhost:8000/metrics).

Opción B — Operar la consola interactiva NoSQL (CRUD):
En una terminal adicional, ejecuta:
python crud_mongodb.py
(Despliega el menú CLI interactivo para Insertar, Consultar, Actualizar y Eliminar documentos en transacciones_cajero).

Opción C — Depuración paso a paso en VS Code:
Ve al panel "Run and Debug" (Ctrl+Shift+D), selecciona la configuración de inicio para simulador_cajero.py o crud_mongodb.py y presiona F5.

Paso 8 — Ver las métricas y alertas en tiempo real
Métricas crudas del pipeline: http://localhost:8000/metrics
Panel completo en Grafana: http://localhost:3000 → Dashboard "Monitoreo Cajeros Bolivia

"Deberías ver, en tiempo real:
Throughput: Transacciones procesadas por segundo (atm_transacciones_total).
Alertas UIF (PCC-1): Detección inmediata de retiros $\ge 10,000$ Bs (atm_alertas_uif_total).
Inconsistencias: Gráficos de discrepancias físico-lógicas entre montos solicitados y dispensados.
Distribución Geográfica: Frecuencia de operaciones por departamento en Bolivia.


