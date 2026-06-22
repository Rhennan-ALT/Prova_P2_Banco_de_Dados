import pika
import json
from app.config import settings

def enviar_mensagem(mensagem: dict):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
    )

    channel = connection.channel()

    channel.queue_declare(queue='pedidos')

    channel.basic_publish(
        exchange='',
        routing_key='pedidos',
        body=json.dumps(mensagem)
    )

    connection.close()