import logging
from store import get_order, add_order
import json
import pika
import sys
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def process_order(ch, method, properties, body):
    try:
        order = json.loads(body)
        order['shippingCost'] = order['totalAmount'] * 0.02
        add_order(order)
        logging.info(f"Received order: {order}")
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON message.")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv("RABBIT_HOST"),
        credentials=pika.PlainCredentials('user', 'password')
    ))
    channel = connection.channel()

    exchange_name = 'orders_exchange'
    queue_name = 'new_orders_queue'

    channel.queue_declare(queue=queue_name, durable=True)

    headers_filter = {"x-match": "all", "status": "new"}
    channel.queue_bind(exchange=exchange_name, queue=queue_name, arguments=headers_filter)

    def graceful_shutdown():
        logging.info("Shutting down consumer...")
        channel.close()
        connection.close()
        sys.exit(0)

    try:
        logging.info("Waiting for new orders...")
        channel.basic_consume(queue=queue_name, on_message_callback=process_order)
        channel.start_consuming()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        graceful_shutdown()