import os
import json


def init_store(filename = 'data.json'):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump({}, f)

def get_store(filename = 'data.json'):
    with open(filename, "r") as f:
        return json.load(f)

def update_store(data, filename = 'data.json'):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def add_order(order):
    Orders = get_store()
    Orders[order['orderId']] = order
    update_store(Orders)


def update_order_status(order_id, order_status):
    Orders = get_store()
    Orders[order_id]['status'] = order_status
    update_store(Orders)


def get_order(orderId):
    Orders = get_store()
    if orderId not in Orders:
        return None
    return Orders[orderId]


def get_all_order_ids(topic):
    Orders = get_store()
    return [order_id for order_id in Orders.keys()]
