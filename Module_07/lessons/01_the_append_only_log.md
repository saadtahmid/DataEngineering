# The Append-Only Log

When discussing streaming messaging systems like **Apache Kafka** or its modern C++ equivalent **Redpanda**, you must unlearn how standard relational databases work. 

In a PostgreSQL table, when a record is changed, the physical disk alters the existing row. 

In a distributed message broker, data is represented as an **Append-Only Log**. You cannot `UPDATE` or `DELETE` a message. You can only write *new* messages to the end of the log. If a user changes their address, you simply append a new "AddressUpdated" event.

## Core Architecture

### 1. Topics
A **Topic** is a categorized stream of records. Think of it like a table in a database, but strictly ordered by time. You might have a topic named `transactions` or `website_clicks`.

### 2. Producers
A **Producer** is a lightweight application (often Python, Java, or Go) that generates data and "publishes" or pushes it into a specific Topic. A rideshare app might have producers running on millions of smartphones emitting `location_ping` events every 3 seconds.

### 3. Consumers
A **Consumer** is an application that subscribes to a Topic. It continuously polls the broker ("Do you have any new data for me?"). It reads the events and processes them (e.g., inserts them into MinIO, triggers an email alert, or updates a real-time dashboard).

### 4. Partitions & Offsets
To handle petabytes of data, a single Topic is broken into multiple **Partitions** (scaling across multiple servers). 
Inside a partition, every message gets a sequential ID number called an **Offset**.

The Broker doesn't care if the Consumer has read the message. The message stays there until its retention period expires (e.g., 7 days).
It is up to the *Consumer* to remember its current Offset. "I just read message #402. Next time I ask for data, I'll start at #403."

## Why Redpanda?
Historically, Apache Kafka required deploying multiple Java Virtual Machines (JVMs) and complex Apache ZooKeeper clusters just to run effectively. It was a nightmare to run locally.
**Redpanda** is a Kafka-compatible streaming data platform built in C++. It is a single binary that requires no JVM, no ZooKeeper, and boasts up to 10x lower tail latencies. It's the SOTA choice for ultra-fast, local-friendly event architectures.
