# Stream Processing

Moving data asynchronously from Point A (Producer) to Point B (Consumer) via a Topic is called *Event Streaming*.
Reading that continuous data and performing complex mathematical aggregations on it *in real-time* is called **Stream Processing**.

## The Problem with Infinite Data
If you query a PostgreSQL table: `SELECT SUM(amount) FROM transactions;`, the database knows exactly where the table begins and ends.

If you query a Redpanda Topic, **the data never ends**. How do you take an aggregate `SUM()` of infinity? 

## Time Windows
To perform aggregations on infinite streams, we cut the infinite river of data into finite chunks of time called **Windows**.

### 1. Tumbling Windows
Tumbling windows are fixed-sized, contiguous, and non-overlapping.
*Example: "Calculate total revenue every 5 seconds."*
- Window 1: 00:00 to 00:05. (Calculates, emits result, closes).
- Window 2: 00:05 to 00:10.
- Window 3: 00:10 to 00:15.

### 2. Hopping / Sliding Windows
These are fixed-sized but *can* overlap. 
*Example: "Calculate a 5-minute moving average of temperature, updating every 1 minute."*

## The Problem of Time: Event Time vs. Processing Time

When building robust stream processors, you must define what "time" means.

- **Processing Time:** The exact millisecond the server physically received the message.
- **Event Time:** The timestamp attached to the event when it actually occurred on the client's device.

### Late-Arriving Data
Imagine someone buys coffee at 10:01 AM (Event Time). Their phone loses cellular service and doesn't reconnect until 10:06 AM, at which point the phone sends the payload to our server (Processing Time).

If our Stream Processor was using **Processing Time** to calculate total sales for the `10:05 - 10:10` tumbling window, the coffee sale would be erroneously counted in the wrong window. 
Modern Streaming architectures (like Apache Flink, or custom Python applications utilizing strict dictionaries) rely heavily on using the **Event Time** payload, holding specific time-windows "open" in memory to allow for late-arriving data (watermarks) before finally closing out the aggregation.
