from confluent_kafka import Producer
import json
import time

producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'retries': 10,
    'retry.backoff.ms': 500,
    'log_level': 2
})

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_order(order):
    producer.produce(
        'order_events',
        key=order['orderId'],
        value=json.dumps(order),
        callback=delivery_report
    )
    producer.flush()


def wait_for_connection():
    max_retries = 5
    retry_interval = 2

    for i in range(max_retries):
        try:
            producer.list_topics(timeout=5)
            print("Connected to Kafka broker.")
            return True
        except Exception as e:
            print(f"Kafka connection attempt {i + 1} failed: {e}. Retrying in {retry_interval}s...")
            time.sleep(retry_interval)

    print("Failed to connect to Kafka after multiple attempts.")
    return False
