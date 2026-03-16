# Module 7: Real-Time Event Streaming

Welcome to Module 7! Thus far, our entire architecture has been **batch-based**. We extract data daily, load it into MinIO, transform it using dbt, and compute snapshots via Iceberg. This is enough for 90% of business reporting.

However, certain use cases (fraud detection, dynamic pricing, real-time dashboards) cannot wait 24 hours. They need milliseconds of latency. To achieve this, we transition to **Streaming Analytics**.

Instead of waiting for data to pile up in a database table, we treat data as an infinite, continuous log of events. We will use **Redpanda**, a high-performance, C++ based drop-in replacement for Apache Kafka that runs beautifully on local environments.

## Lesson Structure
- `lessons/01_the_append_only_log.md`: Understanding the fundamental architecture of Kafka/Redpanda (Topics, Producers, Consumers, and Offsets).
- `lessons/02_stream_processing.md`: How to compute maths over infinite streams (Handling late-arriving data and tumbling windows).

## Hands-On Lab: The Live Feed

In this lab, we will:
1. Deploy a Redpanda broker locally.
2. Spin up a Python **Producer** that simulates a massive firehose of live credit card transactions.
3. Spin up a Python **Consumer** that reads that infinite stream and calculates real-time aggregated metrics (tumbling windows).

1. **Start the Redpanda Cluster**
   ```bash
   cd lab/live_feed
   docker compose up -d
   ```

2. **Setup your environment**
   ```bash
   cd lab/live_feed
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Streaming Pipeline**
   Open **two** separate terminal windows.
   
   In Terminal A, start the producer (this will run forever, generating data):
   ```bash
   source .venv/bin/activate
   python3 producer.py
   ```
   
   In Terminal B, start the consumer (this will also run forever, aggregating data):
   ```bash
   source .venv/bin/activate
   python3 consumer.py
   ```
