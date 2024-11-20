import pika
import json

def send_order(order):
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
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
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
        credentials=credentials
    ))
    channel = connection.channel()
    exchange_name = 'orders_exchange'
    channel.exchange_declare(exchange=exchange_name, exchange_type='headers')
    connection.close()
