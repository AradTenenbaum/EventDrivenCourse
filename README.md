# Event-Driven Development Course RabbitMQ Assignment

## Personal Information

**Name:** Arad Tenenbaum
**ID Number:** 212293799

---

## API Endpoints and Requests

### Producer Application:

- **URL:** `http://localhost:5000/create-order`
- **Type of Request:** POST  
  This endpoint is used to create new orders and send messages to the exchange.

### Consumer Application:

- **URL:** `http://localhost:5001/order-details`
- **Type of Request:** GET  
  This endpoint retrieves details of processed orders from the queue.

---

## Exchange Type and Justification

- **Exchange Type:** Headers Exchange

  The headers exchange was chosen because it provides flexibility in routing messages. It enables me to send the message to all the consumers and allow the consumer itself to decide which type of messages it receives, in our case orders with status 'new'

---

## Binding Key on the Consumer

- **Binding Key:** Not using any

---

## Declaration of Exchange and Queue

- **Exchange Declaration:** Producer  
  The producer declares the exchange because it originates messages and needs to define the routing logic.

- **Queue Declaration:** Consumer  
  The consumer declares the queue to ensure it has control over how messages are consumed and processed. By declaring the queue, the consumer ensures it is properly set up to receive messages routed by the exchange.
