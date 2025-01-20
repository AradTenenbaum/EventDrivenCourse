from confluent_kafka import Consumer
import json
from store import add_order, update_order_status
import logging

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'order_service_group',
    'auto.offset.reset': 'earliest'
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

            order = json.loads(msg.value().decode('utf-8'))
            mode = order.pop('mode')

            if mode == CREATE:
                order['shippingCost'] = order['totalAmount'] * 0.02
                add_order(order)
                logging.info(f"Received order: {order}")
            elif mode == UPDATE:
                update_order_status(order['orderId'], order['status'])
                logging.info(f"Order update: {order}")
            else:
                print(f"Consumer error: mode it not valid")

        except Exception as e:
            print(f"Consumer error: {str(e)}")