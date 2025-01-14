from confluent_kafka import Consumer
import json
from store import add_order
import logging

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'order_service_group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['order_events'])

orders = {}

def consume_orders():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        order = json.loads(msg.value().decode('utf-8'))
        order['shippingCost'] = order['totalAmount'] * 0.02
        add_order(order)
        logging.info(f"Received order: {order}")