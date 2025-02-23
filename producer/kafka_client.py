from confluent_kafka import Producer
import json
import time
from confluent_kafka.avro import AvroProducer
from confluent_kafka import KafkaException
import os
from dotenv import load_dotenv
import random

load_dotenv()

order_schema = '''
{
  "type": "record",
  "name": "Order",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "currency", "type": "string", "default": ""},
    {"name": "customerId", "type": "string", "default": ""},
    {"name": "items", "type": {"type": "array", "items": {
      "type": "record",
      "name": "Item",
      "fields": [
        {"name": "itemId", "type": "string"},
        {"name": "price", "type": "float"},
        {"name": "quantity", "type": "int"}
      ]
    }}, "default": []},
    {"name": "mode", "type": "string", "default": ""},
    {"name": "orderDate", "type": "string", "default": ""},
    {"name": "status", "type": "string", "default": ""},
    {"name": "totalAmount", "type": "float", "default": 0}
  ]
}
'''

update_order_schema = '''
{
  "type": "record",
  "name": "OrderUpdate",
  "fields": [
    {"name": "orderId", "type": "string"},
    {"name": "mode", "type": "string"},
    {"name": "status", "type": "string"}
  ]
}
'''

key_schema = '''
{
    "type": "string"
}
'''

# Connection fail - exponent backoff parameters
MAX_RETRIES = 5
BASE_DELAY = 1 
MAX_DELAY = 20

KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
SCHEMA_REGISTRY_HOST = os.getenv("SCHEMA_REGISTRY_HOST")
SCHEMA_REGISTRY_PORT = os.getenv("SCHEMA_REGISTRY_PORT")

def error_callback(err):
    print(f"Kafka error callback: {err}")

def create_producer():
    """Create a Kafka producer with exponential backoff on connection failure."""
    retries = 0
    while retries < MAX_RETRIES:
        try:
            producer = AvroProducer(
                {
                    # Connections
                    'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
                    'schema.registry.url': f'http://{SCHEMA_REGISTRY_HOST}:{SCHEMA_REGISTRY_PORT}',
                    # Failure handling
                    'retries': 100_000_000,
                    'message.send.max.retries': 5,
                    'retry.backoff.ms': 500,         # Start with 0.5s backoff
                    'retry.backoff.max.ms': 5000,    # Maximum backoff of 5s
                    'message.timeout.ms': 30000,     # Stop retrying after 30s
                    'enable.idempotence': True,      # Ensures exactly-once delivery, avoiding duplicate messages
                    'request.timeout.ms': 30000,
                    'delivery.timeout.ms': 60000,
                    # 'socket.timeout.ms': 10000,
                    # Callbacks 
                    "error_cb": error_callback
                },
                default_key_schema=key_schema,
                default_value_schema=order_schema,
            )
            # Check if Kafka is reachable by querying metadata
            producer.list_topics(timeout=5)  
            print("Connected to Kafka successfully!")
            return producer  # Successfully created producer
        except KafkaException as e:
            wait_time = min(BASE_DELAY * (2 ** retries) + random.uniform(0, 0.1), MAX_DELAY)
            print(f"KafkaException: {str(e)}. Retrying in {wait_time:.2f}s...")
            time.sleep(wait_time)
            retries += 1
    raise RuntimeError("Failed to connect to Kafka after multiple retries.")

try:
    avro_producer = create_producer()
except RuntimeError as e:
    print(f"Critical Error: {e}")
    exit(1)


def delivery_report(err, msg):
    if err is not None:
        print(f"Kafka log callback: Message delivery failed: {err}")
    else:
        print(f"Kafka log callback: Message delivered to topic {msg.topic()}, partition [{msg.partition()}]")

def send_order(order, mode):
    try:
        order["mode"] = mode
        if mode == "UPDATE":
            avro_producer.produce(
                topic='order_events',
                key=order['orderId'],
                value=order,
                callback=delivery_report,
            )
        else:
            avro_producer.produce(
                topic='order_events',
                key=order['orderId'],
                value=order,
                callback=delivery_report,
            )
        avro_producer.flush()
    except KafkaException as e:
        print(f"KafkaException: {str(e)}")