# Event-Driven Producer-Consumer Application Using Kafka

## Full Name and ID Number

**Full Name:** Arad Tenenbaum

---

## API Endpoints and Requests

### Producer Application:

#### Create Order

- **URL:** `http://localhost:5000/create-order`
- **Type of Request:** POST  
  This endpoint is used to create new orders and send messages to the kafka via the order_events topic.
- **Example request body:**

```json
{
  "orderId": "ord-1",
  "itemsNum": 2
}
```

#### Update Order

- **URL:** `http://localhost:5000/update-order`
- **Type of Request:** PUT  
  This endpoint is used to update a specific order status given an order id and new status. The status update is sent as a message to order_events topic in kafka.
- **Example request body:**

```json
{
  "orderId": "ord-1",
  "status": "new"
}
```

### Consumer Application:

#### Order details

- **URL:** `http://localhost:5001/order-details`
- **Type of Request:** GET  
  This endpoint retrieves details of processed orders received as messages from the order_events topic via kafka
- **Example request with params:**

`http://localhost:5001/order-details?orderId=ord1`

#### Order ids from topic

- **URL:** `http://localhost:5001/getAllOrderIdsFromTopic`
- **Type of Request:** GET  
  This endpoint retrieves all the order ids by the given topic in the query params.
- **Example request with params:**

`http://localhost:5001/getAllOrderIdsFromTopic?topic=order_events`

---

## Topics Used and Their Purpose

1. **Topic Name:** `order_events`
   - **Purpose (Producer):**  
     The `cart_service` sends messages to this topic to notify about order-related events, such as creating a new order (`/create_order`) or updating an existing order's status (`/update_order`).
   - **Purpose (Consumer):**  
     The `order_service` consumes messages from this topic to process the received events.

---

## Key Used in the Message and Why

- **Key Used:** `order_id`
- **Reason:**  
  The `order_id` is used as the message key to ensure ordering for events related to the same order. By using `order_id` as the key, Kafka ensures that all messages with the same key are sent to the same partition. This guarantees that:
  - A create message for an order will always be processed before an update message for the same `order_id` if it was sent before.
  - The order of events for a given `order_id` is preserved, reducing the risk of state inconsistencies in the `order_service`.

---

## Kafka Error Handling and Reliability Improvements

### 1. **Producer Error Handling**

- **Retry & Backoff**: Configured `retries=100_000_000` for retry sending a message if it fails, `retry.backoff.ms=500` for the time interval between retries, `retry.backoff.max.ms=5000` and `message.timeout.ms=30000` to prevent infinite retry loops.
- **Serialization/Deserialization Errors**: I use schema registry to manage the schema of the order.
- **Idempotence**: Enabled `enable.idempotence=True` to avoid duplicate messages.
- **Timeout Handling**: Configured `request.timeout.ms=30000` and `delivery.timeout.ms=60000` for longer wait periods if network latency is expected.​
- **Topic Handling**: Auto topic creation is enabled. It is less recommended but I only have one topic.
- **Logic Catching Errors**: Catching KafkaException and logging the error

### 2. **Consumer Error Handling**

- **Reconnect & Timeout Settings**

  - **`reconnect.backoff.ms=1000`** – Initial delay before reconnecting to a broker.
  - **`reconnect.backoff.max.ms=16000`** – Maximum backoff time between reconnection attempts.
  - **`session.timeout.ms=45000`** – Time before the broker considers a consumer dead if no heartbeat is received.
  - **`fetch.wait.max.ms=500`** – Max wait time before the broker returns data to the consumer.
  - **`max.poll.interval.ms=300000`** – Max time between polls before the consumer is removed from the group.

- **Deserialization Errors**: Using confluent schema registry and logging all exceptions.
- **Message order**: I used the order id as key both for the update and the create order so every message with the same order id should be received in the same partition avoiding an update to be received before a create.
