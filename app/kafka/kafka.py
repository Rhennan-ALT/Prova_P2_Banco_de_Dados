from kafka import KafkaProducer
import json
from app.config import settings

_producer = None

def get_producer():
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    return _producer

def publicar_evento(evento: dict):
    producer = get_producer()
    producer.send("pedido_criado", evento)
    producer.flush()