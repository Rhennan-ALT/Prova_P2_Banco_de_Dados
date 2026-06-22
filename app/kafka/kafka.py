from kafka import KafkaProducer
import json
from app.config import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def publicar_evento(evento: dict):
    producer.send("pedido_criado", evento)
    producer.flush()