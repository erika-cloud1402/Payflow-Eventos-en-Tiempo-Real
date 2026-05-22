"""
PayFlow - Enviador de mensajes de alto valor a Service Bus
Caso 3 - Procesamiento de Eventos en Tiempo Real
"""

import json
import uuid
from datetime import datetime
from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "Endpoint=sb://payflow-servicebus-ns.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=BcSWgByfnnxl9heQOmFSfP5ky7M5rar0o+ASbOuJOas="
QUEUE_NAME = "alto-valor"

transacciones_alto_valor = [
    {
        "id": str(uuid.uuid4()),
        "tipo": "compra",
        "monto": 17810026,
        "comercio": "RestauranteY",
        "fecha": datetime.utcnow().isoformat(),
        "moneda": "COP",
        "estado": "pendiente",
        "canal": "alto-valor"
    },
    {
        "id": str(uuid.uuid4()),
        "tipo": "compra",
        "monto": 25868200,
        "comercio": "Tienda123",
        "fecha": datetime.utcnow().isoformat(),
        "moneda": "COP",
        "estado": "pendiente",
        "canal": "alto-valor"
    },
    {
        "id": str(uuid.uuid4()),
        "tipo": "transferencia",
        "monto": 36662567,
        "comercio": "SuperMercadoX",
        "fecha": datetime.utcnow().isoformat(),
        "moneda": "COP",
        "estado": "pendiente",
        "canal": "alto-valor"
    }
]

print("=" * 60)
print("PayFlow - Enviador de mensajes de alto valor a Service Bus")
print("=" * 60)

with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
    with client.get_queue_sender(QUEUE_NAME) as sender:
        for tx in transacciones_alto_valor:
            mensaje = ServiceBusMessage(json.dumps(tx))
            sender.send_messages(mensaje)
            print(f"💰 Enviado: ${tx['monto']:,} COP - {tx['comercio']} - ID: {tx['id'][:8]}...")

print("\n✅ 3 mensajes de alto valor encolados en Service Bus")
print("📊 Verifica la cola 'alto-valor' en el portal Azure")
print("=" * 60)
