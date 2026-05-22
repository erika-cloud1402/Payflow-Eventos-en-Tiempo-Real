"""
PayFlow - Generador de Eventos de Transacciones
Caso 3 - Procesamiento de Eventos en Tiempo Real
Computación en la Nube 2026-1
"""

import asyncio
import json
import random
import uuid
from datetime import datetime
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

# Cadena de conexión de Azure Event Hubs
CONNECTION_STR = "Endpoint=sb://payflow-events-ns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=f/MRFYnDtHhBdLU6RomdoW0sE+8zDD21o+AEhFKUWpI="
EVENTHUB_NAME = "transacciones"

# Lista de comercios de prueba
COMERCIOS = ["Tienda123", "SuperMercadoX", "RestauranteY", "FarmaciaCentral", "LibreriaZ"]

def generar_transaccion_normal():
    """Transacción normal con monto bajo"""
    return {
        "id": str(uuid.uuid4()),
        "tipo": "compra",
        "monto": random.randint(1000, 4999999),
        "comercio": random.choice(COMERCIOS),
        "fecha": datetime.utcnow().isoformat(),
        "moneda": "COP",
        "estado": "pendiente"
    }

def generar_transaccion_alto_valor():
    """Transacción de alto valor mayor a $5.000.000 COP"""
    return {
        "id": str(uuid.uuid4()),
        "tipo": "compra",
        "monto": random.randint(5000001, 50000000),
        "comercio": random.choice(COMERCIOS),
        "fecha": datetime.utcnow().isoformat(),
        "moneda": "COP",
        "estado": "pendiente"
    }

def generar_transaccion_invalida():
    """Transacción con formato inválido para probar validación"""
    return {
        "id": str(uuid.uuid4()),
        "tipo": "compra",
        "monto": "INVALIDO",  # Monto inválido
        "comercio": "",        # Comercio vacío
        "fecha": "fecha-invalida",
        "moneda": "COP",
        "estado": "pendiente"
    }

async def enviar_eventos():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        eventhub_name=EVENTHUB_NAME
    )

    async with producer:
        print("=" * 60)
        print("PayFlow - Generador de Eventos de Transacciones")
        print("=" * 60)

        # 1. Enviar 5 transacciones normales
        print("\n📤 Enviando transacciones normales...")
        batch = await producer.create_batch()
        for i in range(5):
            tx = generar_transaccion_normal()
            batch.add(EventData(json.dumps(tx)))
            print(f"  ✅ Normal #{i+1}: ${tx['monto']:,} COP - {tx['comercio']} - ID: {tx['id'][:8]}...")
        await producer.send_batch(batch)
        print("  → Lote de transacciones normales enviado a Event Hubs")

        # 2. Enviar 3 transacciones de alto valor
        print("\n📤 Enviando transacciones de alto valor...")
        batch = await producer.create_batch()
        for i in range(3):
            tx = generar_transaccion_alto_valor()
            batch.add(EventData(json.dumps(tx)))
            print(f"  💰 Alto valor #{i+1}: ${tx['monto']:,} COP - {tx['comercio']} - ID: {tx['id'][:8]}...")
        await producer.send_batch(batch)
        print("  → Lote de alto valor enviado a Event Hubs")

        # 3. Enviar 2 transacciones inválidas
        print("\n📤 Enviando transacciones con formato inválido...")
        batch = await producer.create_batch()
        for i in range(2):
            tx = generar_transaccion_invalida()
            batch.add(EventData(json.dumps(tx)))
            print(f"  ❌ Inválida #{i+1}: monto='{tx['monto']}' comercio='{tx['comercio']}' - ID: {tx['id'][:8]}...")
        await producer.send_batch(batch)
        print("  → Lote de transacciones inválidas enviado a Event Hubs")

        print("\n" + "=" * 60)
        print("✅ Total enviado: 10 eventos (5 normales, 3 alto valor, 2 inválidas)")
        print("📊 Revisa Azure Monitor para ver las métricas en tiempo real")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(enviar_eventos())
