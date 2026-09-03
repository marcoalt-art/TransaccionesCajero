from pymongo import MongoClient
from datetime import datetime

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["banco_db"]
coleccion = db["transacciones_cajero"]

def crear_transaccion():
    print("\n--- 1. INSERTAR NUEVA TRANSACCIÓN (CREATE) ---")
    cliente = input("Nombre del cliente: ")
    cuenta = input("Número de cuenta: ")
    depto = input("Departamento: ")
    monto = float(input("Monto en Bs: "))
    
    doc = {
        "cliente": cliente,
        "numero_cuenta": cuenta,
        "departamento": depto,
        "cajero_id": f"ATM-{depto.upper()[:3]}-MANUAL",
        "monto_solicitado": monto,
        "monto_dispensado": monto,
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": "MANUAL",
        "timestamp": datetime.now().timestamp()
    }
    
    res = coleccion.insert_one(doc)
    print(f"✅ Transacción registrada exitosamente con ID: {res.inserted_id}")

def leer_transacciones():
    print("\n--- 2. CONSULTAR ÚLTIMAS 5 TRANSACCIONES (READ) ---")
    registros = coleccion.find().sort("fecha_hora", -1).limit(5)
    for reg in registros:
        print(f"ID: {reg['_id']} | {reg.get('cliente')} | Cuenta: {reg.get('numero_cuenta')} | Depto: {reg.get('departamento')} | Monto: Bs {reg.get('monto_solicitado')} | Fecha: {reg.get('fecha_hora')}")

def actualizar_transaccion():
    print("\n--- 3. ACTUALIZAR TRANSACCIÓN (UPDATE) ---")
    cuenta = input("Ingrese el número de cuenta a modificar: ")
    nuevo_monto = float(input("Ingrese el nuevo monto ajustado (Bs): "))
    
    res = coleccion.update_many(
        {"numero_cuenta": cuenta},
        {"$set": {"monto_solicitado": nuevo_monto, "monto_dispensado": nuevo_monto}}
    )
    print(f"🔄 Registros actualizados: {res.modified_count}")

def eliminar_transacciones_menores():
    print("\n--- 4. ELIMINAR REGISTROS (DELETE) ---")
    monto_limite = float(input("Eliminar transacciones con monto menor a (Bs): "))
    res = coleccion.delete_many({"monto_solicitado": {"$lt": monto_limite}})
    print(f"🗑️ Registros eliminados: {res.deleted_count}")

def menu():
    while True:
        print("\n==========================================")
        print("   GESTIÓN CRUD MONGOBD - BANCO DE BOLIVIA")
        print("==========================================")
        print("1. Insertar transacción (Create)")
        print("2. Consultar últimas transacciones (Read)")
        print("3. Actualizar monto por cuenta (Update)")
        print("4. Eliminar transacciones menores (Delete)")
        print("5. Salir")
        
        opcion = input("Seleccione una opción (1-5): ")
        
        if opcion == "1":
            crear_transaccion()
        elif opcion == "2":
            leer_transacciones()
        elif opcion == "3":
            actualizar_transaccion()
        elif opcion == "4":
            eliminar_transacciones_menores()
        elif opcion == "5":
            print("Saliendo del módulo CRUD...")
            break
        else:
            print("Opción inválida, intente de nuevo.")

if __name__ == "__main__":
    menu()