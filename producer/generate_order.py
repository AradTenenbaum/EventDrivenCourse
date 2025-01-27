import random
import string
import datetime
from decimal import Decimal

STATUSES = ['confirmed', 'pending', 'shipped', 'delivered', 'cancelled', 'new']

def is_valid_status(status):
    return status in STATUSES

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_decimal(min_value=1.00, max_value=100.00):
    return round(Decimal(random.uniform(min_value, max_value)), 2)

def create_random_order(order_id, num_items):
    currencies = ['USD', 'EUR', 'GBP', 'AUD', 'CAD', 'ILS']

    items = []
    total_amount = Decimal(0)
    for _ in range(num_items):
        quantity = random.randint(1, 10)
        price = generate_random_decimal(1.00, 100.00)
        total_amount += price * quantity

        items.append({
            'itemId': generate_random_string(12),
            'quantity': quantity,
            'price': float(price)
        })

    order = {
        'orderId': order_id,
        'customerId': generate_random_string(10),
        'orderDate': datetime.datetime.now().isoformat(),
        'items': items,
        'totalAmount': float(total_amount),
        'currency': random.choice(currencies),
        'status': random.choice(STATUSES),
    }

    return order