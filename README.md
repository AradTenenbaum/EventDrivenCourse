# README - Event-Driven Producer-Consumer Application Using Kafka

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

## Error Handling

1. **Producer-Side Errors (Cart Service):**

   - **Handling Kafka Connection Errors:**
     - If Kafka is unreachable, the producer retries sending the message with exponential backoff to avoid overwhelming the system.
     - After a maximum retry count, the error is logged, and an alert is raised for manual intervention.
   - **Invalid Message Format:**
     - Before sending, all messages are validated to ensure required fields (e.g., `order_id`, `type`) are present. Invalid messages are rejected with an appropriate HTTP response (400 Bad Request).

2. **Consumer-Side Errors (Order Service):**

   - **Deserialization Errors:**
     - If a message cannot be deserialized (e.g., malformed JSON), the consumer logs the error and skips the message to avoid disrupting the entire processing stream.
   - **Business Logic Errors:**
     - For example, if an update message is received for a non-existent `order_id`, the consumer logs the error.
