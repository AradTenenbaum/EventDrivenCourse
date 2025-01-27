from confluent_kafka import Producer
import json
import time
from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro import CachedSchemaRegistryClient
import os
from dotenv import load_dotenv

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

KAFKA_HOST = os.getenv("KAFKA_HOST")
KAFKA_PORT = os.getenv("KAFKA_PORT")
SCHEMA_REGISTRY_HOST = os.getenv("SCHEMA_REGISTRY_HOST")
SCHEMA_REGISTRY_PORT = os.getenv("SCHEMA_REGISTRY_PORT")

avro_producer = AvroProducer(
    {
        'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}',
        'schema.registry.url': f'http://{SCHEMA_REGISTRY_HOST}:{SCHEMA_REGISTRY_PORT}'
    },
    default_key_schema=key_schema,
    default_value_schema=order_schema
)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_order(order, mode):
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


def wait_for_connection():
    max_retries = 5
    retry_interval = 2

    for i in range(max_retries):
        try:
            avro_producer.produce(topic='order_events', value={"test": "test"}, key="test")
            print("Connected to Kafka broker.")
            return True
        except Exception as e:
            print(f"Kafka connection attempt {i + 1} failed: {e}. Retrying in {retry_interval}s...")
            time.sleep(retry_interval)

    print("Failed to connect to Kafka after multiple attempts.")
    return False
