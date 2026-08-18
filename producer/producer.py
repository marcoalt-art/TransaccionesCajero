import time
import json
import pandas as pd
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

producer = None
while not producer:
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Conexion exitosa con Apache Kafka.", flush=True)
    except NoBrokersAvailable:
        print("Esperando a Apache Kafka...", flush=True)
        time.sleep(3)

df = pd.read_csv('/app/data/data_cajeros.csv')

while True:
    for _, row in df.iterrows():
        data = {
            'dia': int(row['dia']),
            'cajero': str(row['cajero']),
            'pagos': int(row['pagos']),
            'cobros': int(row['cobros'])
        }
        producer.send('transacciones-cajero', value=data)
        print(f"Evento enviado a Kafka -> Dia: {data['dia']} | Cajero: {data['cajero']} | Pagos: {data['pagos']} | Cobros: {data['cobros']}", flush=True)
        time.sleep(2)
