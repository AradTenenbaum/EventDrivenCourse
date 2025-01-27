from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
import json
from store import add_order, update_order_status
import logging

consumer = AvroConsumer({
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'order_service_group',
    'auto.offset.reset': 'earliest',
    'schema.registry.url': 'http://localhost:8081'
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
                add_order(order)
                logging.info(f"Received order: {order}")
            elif mode == UPDATE:
                update_order_status(order['orderId'], order['status'])
                order = {key: item for key, item in order.items() if key in ['orderId', 'status', 'mode']}
                logging.info(f"Order update: {order}")
            else:
                print(f"Consumer error: mode it not valid")

        except Exception as e:
            print(f"Consumer error: {str(e)}")