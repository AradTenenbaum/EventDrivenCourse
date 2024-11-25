from flask import Flask, request, jsonify
from generate_order import create_random_order
from rabbitmq_client import send_order, init_rabbit
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

@app.route('/create-order', methods=['POST'])
def create_order():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    order = create_random_order(data['orderId'], data['itemNum'])

    send_order(order)
    
    response = {
        "order": order
    }
    return jsonify(response), 200

if __name__ == '__main__':
    init_rabbit()
    app.run(debug=True, host=os.getenv('HOST'))
