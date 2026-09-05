# Sistema de Monitoreo de Cajeros Automáticos y Detección de Irregularidades (UIF)

Proyecto aplicado para la simulación, persistencia NoSQL y monitoreo en tiempo real de transacciones de cajeros automáticos (ATM), instrumentado con **MongoDB**, **Prometheus** y **Grafana** para la evaluación de eventos operativos y la generación de alertas de la Unidad de Investigaciones Financieras (UIF).

---

## 1. Arquitectura del Proyecto

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ENTORNO LOCAL NATIVO (WINDOWS / VS CODE)                        │
└────────────────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────┐         ingesta BSON          ┌────────────────────────────────┐
│  importar_csv_mongo.py │ ────────────────────────────▶ │    MongoDB (Base de Datos)     │
└────────────────────────┘                               │  - Base: banco_db              │
                                                         │  - Colección:                  │
┌────────────────────────┐         persistencia          │    transacciones_cajero        │
│   simulador_cajero.py  │ ────────────────────────────▶ └────────────────────────────────┘
│  (Generador continuo   │                                               ▲
│   de transacciones)    │                                               │ consultas CRUD
└───────────┬────────────┘                               ┌───────────────┴────────────────┐
            │                                            │        crud_mongodb.py         │
            │ expone métricas HTTP                       └────────────────────────────────┘
            │ (puerto 8000 / 8001)
            ▼
┌────────────────────────┐       scrape /metrics         ┌────────────────────────────────┐
│  Prometheus (Binario)  │ ────────────────────────────▶ │       Grafana (Binario)        │
│  (puerto 9090)         │                               │  (puerto 3000)                 │
│  - prometheus.yml      │                               │  - Dashboards y Alertas UIF    │
└────────────────────────┘                               └────────────────────────────────┘
