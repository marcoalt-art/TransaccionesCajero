import time
import random
from datetime import datetime
from pymongo import MongoClient
from prometheus_client import start_http_server, Counter, Gauge

# Conexión a MongoDB Local
client = MongoClient("mongodb://localhost:27017/")
db = client["banco_db"]
coleccion = db["transacciones_cajero"]

# Listas de datos para Bolivia
NOMBRES_BOLIVIA = [
    "Juan Carlos Mamani", "María Elena Quispe", "Gonzalo Flores", 
    "Eliana Galván", "Marco Altamirano", "Ramiro Condori", 
    "Sonia Vargas", "Carlos Mendoza", "Ana Lucía Choque"
]

DEPARTAMENTOS = [
    "Santa Cruz", "La Paz", "Cochabamba", "Tarija", 
    "Potosí", "Oruro", "Chuquisaca", "Beni", "Pando"
]

# Métricas de Prometheus
TOTAL_TRANSACCIONES = Counter('atm_transacciones_total', 'Total de transacciones procesadas')
ALERTAS_UIF = Counter('atm_alertas_uif_total', 'Alertas de UIF Formulario PCC-1 (>= 10000 Bs)')
EXCESO_MONTO = Counter('atm_exceso_monto_total', 'Transacciones con exceso de monto (> 5000 Bs)')
DISCREPANCIAS = Counter('atm_discrepancias_total', 'Discrepancias o montos menores dispensados')
ULTIMO_MONTO = Gauge('atm_ultimo_monto_bs', 'Monto de la última transacción')

def generar_y_guardar_transaccion():
    monto_solicitado = random.choice([200, 500, 1200, 3000, 5500, 8000, 10000, 12500, 15000])
    monto_dispensado = monto_solicitado
    
    # Simular disparidad o discrepancia en caja (Monto Menor)
    hay_discrepancia = random.random() < 0.15  # 15% de probabilidad
    if hay_discrepancia:
        monto_dispensado = monto_solicitado - random.choice([50, 100, 200])
        DISCREPANCIAS.inc()

    nombre = random.choice(NOMBRES_BOLIVIA)
    cuenta = f"1000-{random.randint(100000, 999999)}"
    departamento = random.choice(DEPARTAMENTOS)
    cajero_id = f"ATM-{departamento.upper()[:3]}-{random.randint(1, 10)}"
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Documento CRUD para MongoDB
    doc = {
        "cliente": nombre,
        "numero_cuenta": cuenta,
        "departamento": departamento,
        "cajero_id": cajero_id,
        "monto_solicitado": monto_solicitado,
        "monto_dispensado": monto_dispensado,
        "fecha_hora": fecha_hora,
        "tipo": "RETIRO",
        "timestamp": time.time()
    }

    # Guardar en MongoDB
    coleccion.insert_one(doc)

    # Métricas de Prometheus
    TOTAL_TRANSACCIONES.inc()
    ULTIMO_MONTO.set(monto_dispensado)

    # Imprimir en consola con detalles
    info_cliente = f"Cliente: {nombre} | Cuenta: {cuenta} | Fecha/Hora: {fecha_hora} | Depto: {departamento}"

    if monto_solicitado >= 10000:
        ALERTAS_UIF.inc()
        print(f"🚨 [ALERTA UIF PCC-1] {info_cliente} | Monto: Bs {monto_solicitado}")
    elif monto_solicitado > 5000:
        EXCESO_MONTO.inc()
        print(f"⚠️ [EXCESO DE MONTO] {info_cliente} | Monto: Bs {monto_solicitado}")
    elif hay_discrepancia:
        print(f"❌ [DISCREPANCIA / MONTO MENOR] {info_cliente} | Solicitado: Bs {monto_solicitado} - Dispensado: Bs {monto_dispensado}")
    else:
        print(f"✅ [TRANSACCIÓN OK] {info_cliente} | Monto: Bs {monto_solicitado}")

if __name__ == "__main__":
    start_http_server(8000)
    print("🚀 Servidor de métricas en http://localhost:8000/metrics")
    print("🔄 Procesando transacciones e insertando en MongoDB...")
    
    while True:
        generar_y_guardar_transaccion()
        time.sleep(2)