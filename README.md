# Sistema de Monitoreo de Cajeros Automáticos y Detección de Irregularidades (UIF)
**Módulo 9 - Arquitectura e Ingesta de Datos en Tiempo Real**  
**Banco de Bolivia**

---

## 📑 Descripción del Proyecto

Este proyecto implementa una solución integral para la ingesta, procesamiento, persistencia NoSQL y monitoreo en tiempo real de transacciones bancarias ejecutadas en la red de Cajeros Automáticos (ATMs) a nivel nacional en Bolivia.

El sistema simula eventos operativos (retiros, depósitos, discrepancias de efectivo) e identifica irregularidades financieras (ALERTAS UIF) asociadas a montos elevados y sospechas de lavado de activos, almacenando la información en **MongoDB** e integrando **Prometheus** y **Grafana** para la visualización de métricas en tiempo real.

---

## 🛠️ Arquitectura e Infraestructura

La solución está construida bajo los siguientes componentes:

1. **Persistencia NoSQL (MongoDB):** Almacenamiento flexible en formato de documentos BSON para registrar todas las transacciones procesadas, clientes, cuentas y marcas de tiempo.
2. **Servidor de Métricas (Prometheus):** Recolección continua de métricas mediante endpoints HTTP экспоetados desde la simulación Python.
3. **Tablero de Control (Grafana):** Visualización interactiva de KPIs operativos y alertas críticas con reglas de notificación configuradas.
4. **Scripts de Simulación y CRUD (Python 3.12):** Emisión de transacciones sintéticas e interfaz de gestión para la base de datos MongoDB.

---

## 🗂️ Estructura del Repositorio

```text
.
├── crud_mongodb.py          # Interfaz CLI interactiva (Create, Read, Update, Delete) en MongoDB
├── importar_csv_mongo.py    # Script de carga/ingesta masiva de datos iniciales a MongoDB
├── prometheus.yml           # Configuración del servidor Prometheus para la recolección de métricas
├── simulador_cajero.py      # Simulador de transacciones de cajeros y generador de métricas PromQL
├── dataset_transacciones.csv # Datos históricos/sintéticos de transacciones
└── README.md                # Documentación del proyecto
