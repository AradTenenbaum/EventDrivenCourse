from flask import Flask, request, jsonify
import threading
from store import get_order, get_all_order_ids
from rabbitmq_connect import consume_messages
from kafka_connect import consume_orders
from store import init_store
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

@app.route('/order-details', methods=['GET'])
def order_details():
    orderId = request.args.get('orderId', default=None)
    if orderId == None:
        return jsonify({"error": "No order id provided"}), 400
    
    order = get_order(orderId)

    if order is None:
        return jsonify({"error": "Order not found"}), 404
    
    response = {
        "order": order
    }
    return jsonify(response), 200


@app.route('/getAllOrderIdsFromTopic', methods=['GET'])
def get_all_order_ids_from_topic():
    topic = request.args.get('topic', default=None)

    if topic == None:
        return jsonify({"error": "No topic provided"}), 400
    if topic not in ['order_events']:
        return jsonify({"error": "No such topic"}), 404
    
    all_order_ids = get_all_order_ids(topic)

    return jsonify(all_order_ids), 200


if __name__ == "__main__":
    init_store()
    # consumer_thread = threading.Thread(target=consume_messages)
    # consumer_thread.daemon = True
    # consumer_thread.start()
    consumer_thread = threading.Thread(target=consume_orders, daemon=True)
    consumer_thread.start()
    app.run(debug=True, port=5001, host=os.getenv('HOST'))