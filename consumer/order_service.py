from flask import Flask, request, jsonify
import threading
from store import get_order
from rabbitmq_connect import consume_messages

app = Flask(__name__)

@app.route('/order-details', methods=['POST'])
def order_details():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    response = {
        "order": get_order(data['orderId'])
    }
    return jsonify(response), 200

if __name__ == "__main__":
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.daemon = True
    consumer_thread.start()
    app.run(debug=True, port=5001)