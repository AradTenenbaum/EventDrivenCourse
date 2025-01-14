from flask import Flask, request, jsonify
from generate_order import create_random_order
# from rabbitmq_client import send_order, init_rabbit
from kafka_client import send_order, wait_for_connection
from dotenv import load_dotenv
import os
import threading

load_dotenv()
app = Flask(__name__)

from confluent_kafka import Producer
import json

@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not 'orderId' in data:
        return jsonify({"error": "No order id provided"}), 400
    if not 'itemsNum' in data:
        return jsonify({"error": "Number of items is not provided"}), 400
    

    order = create_random_order(data['orderId'], data['itemsNum'])

    try:
        send_order(order)
    
        response = {
            "order": order
        }
        return jsonify(response), 200
    except Exception as e:
        print("Error: ", str(e))
        return jsonify({
            "message": "Server Error"
        }), 500


@app.route('/update-order', methods=['PUT'])
def update_order():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not 'orderId' in data:
        return jsonify({"error": "No order id provided"}), 400
    if not 'status' in data:
        return jsonify({"error": "Status is not provided"}), 400
    
    # send_order(order)
    
    # response = {
    #     "order": order
    # }
    return jsonify(data), 200

if __name__ == '__main__':
    # init_rabbit()
    kafka_connection_check_thread = threading.Thread(target=wait_for_connection, daemon=True)
    kafka_connection_check_thread.start()
    app.run(debug=True, host=os.getenv('HOST'))
