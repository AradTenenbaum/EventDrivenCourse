from flask import Flask, request, jsonify
import threading
from store import get_order
from rabbitmq_connect import consume_messages
from kafka_connect import consume_orders
from store import init_store
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

@app.route('/order-details', methods=['POST'])
def order_details():
    data = request.json
    if not data:
        return jsonify({"error": "No order id provided"}), 400
    
    order = get_order(data['orderId'])

    if order is None:
        return jsonify({"error": "Order not found"}), 404
    
    response = {
        "order": order
    }
    return jsonify(response), 200

if __name__ == "__main__":
    init_store()
    # consumer_thread = threading.Thread(target=consume_messages)
    # consumer_thread.daemon = True
    # consumer_thread.start()
    consumer_thread = threading.Thread(target=consume_orders, daemon=True)
    consumer_thread.start()
    app.run(debug=True, port=5001, host=os.getenv('HOST'))