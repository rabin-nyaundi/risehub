import aio_pika
from app.config.settings import settings

async def get_rabbitmq_connection():
    """Get RabbitMQ connection"""
    connection = await aio_pika.connect_robust(
        str(settings.RABBITMQ_URL)
    )
    try:
        yield connection
    finally:
        await connection.close()

async def get_rabbitmq_channel():
    """Get RabbitMQ channel"""
    connection = await aio_pika.connect_robust(
        str(settings.RABBITMQ_URL)
    )
    channel = await connection.channel()
    try:
        yield channel
    finally:
        await channel.close()
        await connection.close()

# Queue names
POST_QUEUE = "post_queue"
ANALYTICS_QUEUE = "analytics_queue"
NOTIFICATION_QUEUE = "notification_queue"

# Exchange names
POST_EXCHANGE = "post_exchange"
ANALYTICS_EXCHANGE = "analytics_exchange"
NOTIFICATION_EXCHANGE = "notification_exchange"

# Routing keys
POST_ROUTING_KEY = "post.*"
ANALYTICS_ROUTING_KEY = "analytics.*"
NOTIFICATION_ROUTING_KEY = "notification.*"
