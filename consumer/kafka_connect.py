from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
import json
from store import add_order, update_order_status
import logging
import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
SCHEMA_REGISTRY_HOST = os.getenv("SCHEMA_REGISTRY_HOST")
SCHEMA_REGISTRY_PORT = os.getenv("SCHEMA_REGISTRY_PORT")

consumer = AvroConsumer({
    'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
    'group.id': 'order_service_group',
    'auto.offset.reset': 'earliest',
    'schema.registry.url': f'http://{SCHEMA_REGISTRY_HOST}:{SCHEMA_REGISTRY_PORT}'
})
consumer.subscribe(['order_events'])

CREATE = "CREATE"
UPDATE = "UPDATE"

def consume_orders():
    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            order = msg.value()
            mode = order.pop('mode')

            if mode == CREATE:
                order['shippingCost'] = order['totalAmount'] * 0.02
                logging.info(f"Received order creation message: {order}")
                add_order(order)
            elif mode == UPDATE:
                logging.info(f"Received order update message: {order}")
                update_order_status(order['orderId'], order['status'])
                order = {key: item for key, item in order.items() if key in ['orderId', 'status', 'mode']}
            else:
                print(f"Consumer error: mode it not valid")

        except Exception as e:
            print(f"Consumer error: {str(e)}")