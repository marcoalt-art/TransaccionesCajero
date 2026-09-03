import pandas as pd
from pymongo import MongoClient

def importar_dataset():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["banco_db"]
    coleccion = db["transacciones_cajero"]

    ruta_csv = "data/data_cajeros.csv"
    
    print(f"📖 Leyendo archivo desde: {ruta_csv}")
    df = pd.read_csv(ruta_csv)

    registros = df.to_dict(orient="records")

    coleccion.delete_many({})
    resultado = coleccion.insert_many(registros)
    
    print(f"✅ Ingesta exitosa: Se insertaron {len(resultado.inserted_ids)} registros en MongoDB.")

if __name__ == "__main__":
    importar_dataset()