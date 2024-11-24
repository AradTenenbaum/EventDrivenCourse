import pika
import json
import os
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def send_order(order):
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv("RABBIT_HOST"),
        credentials=credentials
    ))
    channel = connection.channel()
    exchange_name = 'orders_exchange'
    channel.exchange_declare(exchange=exchange_name, exchange_type='headers')
    message = json.dumps(order)
    headers = {"status": order["status"]}
    channel.basic_publish(
        exchange=exchange_name,
        routing_key='',
        body=message,
        properties=pika.BasicProperties(headers=headers)
    )
    connection.close()


def init_rabbit():
    while(True):
        try:
            credentials = pika.PlainCredentials('user', 'password')
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=os.getenv("RABBIT_HOST"),
                credentials=credentials
            ))
            channel = connection.channel()
            exchange_name = 'orders_exchange'
            channel.exchange_declare(exchange=exchange_name, exchange_type='headers')
            connection.close()
            break
        except:
            logging.info('Retrying to connect Rabbit server')
            time.sleep(5)
