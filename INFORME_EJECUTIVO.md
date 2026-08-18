# UNIVERSIDAD AMAZÓNICA DE PANDO
## POSTGRADO – UAP
### PROYECTO FINAL: SOLUCIÓN DE STREAMING CON KAFKA Y FLINK

**INFORME EJECUTIVO DEL PROYECTO**
*Sistema de Monitoreo Transaccional por Cajero en Tiempo Real*

---
- **DOCENTE:** PHD. ING. ALAN RODRIGO CORINI GUARACHI
- **MAESTRANTE:** LIC. MARCO ANTONIO ALTAMIRANO V.
- **MÓDULO 8:** ANÁLISIS EN TIEMPO REAL Y STREAMING DE DATOS
- **FECHA:** 12 DE AGOSTO DE 2026
---

## A. Resumen Ejecutivo

El proyecto nació con el objetivo de resolver un problema crítico en la banca: la imposibilidad de supervisar transacciones en tiempo real con arquitecturas tradicionales. Las entidades financieras suelen procesar sus datos en lotes (batch), lo que genera demoras de horas o días para identificar fallos mecánicos o fraudes. Este desarrollo buscó implementar un pipeline analítico de procesamiento en tiempo real (Stream Processing) capaz de capturar, validar y alertar desviaciones operativas en milisegundos.

La solución permite capturar, transmitir, procesar y visualizar métricas críticas de flujo monetario y detección de anomalías (como retiros con exceso de monto o diferencias en dispensación), reduciendo la latencia de respuesta ante eventos críticos a milisegundos.

## B. Arquitectura y Flujo del Sistema

Para dar cumplimiento estricto a los requisitos obligatorios del proyecto, la arquitectura implementa el flujo continuo: **Fuente de datos → Kafka → Flink → Resultados**.

- **Fuente de Datos / Productor (Producer):** Componente en Python que simula la actividad continua de red de cajeros automáticos enviando transacciones en formato JSON.
- **Apache Kafka (Ingesta):** Plataforma de mensajería distribuida que recibe los eventos continuos de la fuente en el tópico `cajero-events`. Garantiza que ningún evento se pierda frente a picos de tráfico.
- **Apache Flink (Procesamiento):** Motor de computación sobre flujos continuos (Session Mode). Recibe datos de Kafka, aplica reglas de negocio para clasificar eventos, detecta discrepancias en montos y calcula métricas en tiempo real.
- **Resultados y Salida:** Los datos procesados por Flink se publican en el tópico `cajero-results`, se persisten en PostgreSQL para auditoría y se consumen en el Dashboard Web en bolivianos (Bs).
- **Capa de Visualización (Dashboard Web / Flask):** Interfaz gráfica interactiva que consume los resultados en tiempo real y muestra el monitoreo en bolivianos (Bs).

## C. Resultados, Capturas e Interpretaciones

### 1. Contenedores Ejecutándose
- **Descripción:** Verificación del estado de los servicios mediante `docker compose ps` dentro del entorno virtual.
- **Captura a incluir:** Captura de la terminal ejecutando `sudo docker compose ps` mostrando todos los contenedores en estado Up.
- **Contribución al Proyecto:** Garantiza el aislamiento, la portabilidad y la coexistencia de múltiples servicios pesados (Kafka, Flink, Postgres) en un solo entorno administrado sin conflictos de puertos ni dependencias.
- **Interpretación:** Todos los microservicios (Zookeeper, Kafka, JobManager, TaskManager, Producer y Web) operan de manera estable y aislada en sus respectivos puertos. Confirma la salud del sistema operativo. Los contenedores zookeeper, kafka, jobmanager, taskmanager, producer y web están arriba (Up) y listos.

### 2. El Productor Generando Eventos
- **Descripción:** Logs del contenedor producer emitiendo transacciones simuladas de cajeros.
- **Captura a incluir:** Captura de la terminal con el comando `sudo docker compose logs -f producer`.
- **Contribución al Proyecto:** Representa el punto de entrada de la información. Al generar eventos continuos, simula el tráfico real que recibiría el banco desde sus terminales operativas.
- **Interpretación:** El emisor genera un flujo constante (~5.3 tx/s) con IDs de cajeros, montos solicitados y procesados. Valida que la fuente de datos está activa y emitiendo registros estructurados con ID de cajero, monto solicitado y monto efectivamente entregado.

### 3. Los Mensajes Recibidos por Kafka
- **Descripción:** Consumo e inspección del tópico `cajero-events` en Kafka.
- **Captura a incluir:** Captura de la terminal mostrando el consumo de mensajes del tópico mediante el cliente de línea de comandos de Kafka.
- **Contribución al Proyecto:** Demuestra que la capa de desacoplamiento funciona. Permite almacenar temporalmente las transacciones sin colapsar las bases de datos transaccionales de la red financiera.
- **Interpretación:** Confirma la ingesta correcta de mensajes estructurados en JSON en la cola de mensajería con latencia imperceptible. Asegura que Kafka recibe e indexa correctamente los JSON desde la fuente, actuando como el conector de alta velocidad hacia la capa analítica.

### 4. El Trabajo Activo en el Panel de Flink
- **Descripción:** Dashboard de administración de Apache Flink en el puerto `http://localhost:8081`.
- **Captura a incluir:** Captura del dashboard de Apache Flink en la pestaña Overview mostrando los Task Slots asignados y el Job en ejecución.
- **Contribución al Proyecto:** Muestra el "cerebro" del procesamiento en tiempo real. Flink mantiene la topología de datos ejecutándose en memoria distribuyendo tareas entre ranuras de procesamiento (Task Slots).
- **Interpretación:** Valida que el motor de Flink se encuentra activo en modo sesión, distribuyendo las tareas de procesamiento continuo en la memoria. Confirma que el script o programa de Flink está desplegado correctamente en el clúster (Session Mode) y procesando las ventanas de tiempo dinámicamente.

### 5. Los Resultados del Procesamiento
- **Descripción:** Mensajes procesados por Flink publicados en el tópico de salida `cajero-results`.
- **Captura a incluir:** Captura de la terminal leyendo el tópico `cajero-results` con las alertas calculadas.
- **Contribución al Proyecto:** Demuestra la capacidad del motor para transformar datos crudos en información útil de negocio mediante la aplicación inmediata de reglas.
- **Interpretación:** Muestra la salida del tópico `cajero-results`. Flink calcula en tiempo real la diferencia de dinero (Monto Solicitado vs Procesado) y adjunta la etiqueta de alerta correspondiente.

### 6. Interfaz, API, Base de Datos o Logs Utilizados
- **Descripción:** Dashboard visual e interactivo desplegado en el puerto `http://localhost:5000`.
- **Captura a incluir:** Captura final del dashboard web con las tarjetas de métricas en Bs, el esquema de arquitectura y la tabla en tiempo real.
- **Contribución al Proyecto:** Centraliza la salida de los datos en múltiples niveles: permite la persistencia relacional para auditorías futuras (PostgreSQL), la inspección de eventos en tiempo real mediante logs del sistema y la interpretación ejecutiva de los indicadores mediante la interfaz visual.
- **Interpretación:** Presenta una consola ejecutiva donde se consolidan 100 eventos procesados, 69 alertas detectadas y métricas en moneda local (Bs).
  - **Interfaz Web (http://localhost:5000):** Presenta la consola ejecutiva donde se consolidan los eventos procesados, mostrando métricas financieras en bolivianos (Bs), la tasa de emisión y las tablas dinámicas con alertas de transacción.
  - **Base de Datos (PostgreSQL):** Almacena las transacciones procesadas garantizando persistencia y acceso estructurado para reportes históricos o consultas relacionales.
  - **Logs del Sistema:** Registran la trazabilidad de los contenedores para diagnóstico técnico y monitoreo del estado del pipeline.

## D. Conclusiones e Impacto del Negocio

- **Cumplimiento del Objetivo:** Se logró construir e integrar con éxito un pipeline completo de Stream Processing bajo Docker. El sistema captura eventos simulados y los transforma en indicadores de gestión en menos de 45 ms.
- **¿Por qué se consideran alertas y cuál es su impacto?**
  - **Exceso de Monto:** Ocurre cuando la solicitud supera el límite operativo o promedio permitido (p. ej. > Bs 5,000.00). *Impacto:* Protege a la entidad frente a vulneraciones de seguridad, desfalcos o fallas en el software del cajero.
  - **Monto Menor / Discrepancia:** Ocurre cuando el dinero procesado/dispensado es inferior o distinto al solicitado por el cliente. *Impacto:* Previene reclamos financieros, discrepancias en arqueos de caja y deterioro de la confianza del usuario.
  - **Significado de la muestra:** De 100 eventos procesados en la prueba, las 69 alertas detectadas demuestran la efectividad del filtro de Flink para aislar eventos críticos sin intervención humana.
- **Eficiencia Operativa:** La integración de Kafka y Flink permite procesar eventos con una latencia promedio menor a 45 ms, ideal para la detección temprana de anomalías en servicios financieros.
- **Escalabilidad y Aislamiento:** La contenerización con Docker Compose garantiza la portabilidad del entorno sin generar conflictos en el sistema operativo anfitrión.
- **Valor de Negocio:** La transformación de logs complejos en un tablero visual accesible facilita la toma de decisiones ejecutivas en tiempo real.

## E. Repositorio de Código

- **Enlace a GitHub:** https://github.com/marcoalt-art/TransaccionesCajero
