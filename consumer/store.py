

Orders = []

def add_order(order):
    Orders.append(order)

def get_order(orderId):
    return next((order for order in Orders if order.get('orderId') == orderId), None)