# 🚀 Data Engineering: Zero to Mastery (100% Local & Open-Source)

Welcome to the Zero to Mastery Data Engineering course. This curriculum is designed to take you from the absolute basics of data manipulation to building cutting-edge, real-time, AI-ready data pipelines. 

**The Philosophy:** We learn by building. This course relies exclusively on a modern, 100% open-source stack that runs locally on your machine. No cloud subscriptions, no unexpected billing—just raw, SOTA engineering.

## 🛠️ Prerequisites
* **OS:** Linux (Ubuntu 24.04 recommended) or macOS. Windows users should use WSL2.
* **Core Tools:** Python 3.10+, Docker, and Docker Compose installed.
* **Hardware:** A dedicated GPU is highly recommended for Module 8 (Local LLMOps & Vector generation).
* **Mindset:** Readiness to read documentation and debug container networks.

---

## 📚 Course Curriculum

### Module 1: The Core Languages (SQL & Python)
*Understand the foundational languages of data and how modern relational databases operate.*

- [ ] **Lesson 1.1: Relational Data & PostgreSQL**
  - Database normalization, primary/foreign keys, and standard data types.
- [ ] **Lesson 1.2: Advanced SQL Thinking**
  - Common Table Expressions (CTEs), Window Functions, and query execution plans.
- [ ] **Lesson 1.3: Python for Data Engineering**
  - Virtual environments, API interactions (REST), and JSON parsing.
- [ ] **💻 Hands-On Lab 1: The Local Database**
  - Deploy PostgreSQL locally via Docker Compose.
  - Write a Python script to ingest API data into Postgres.
  - Perform advanced aggregations using CTEs and Window Functions.

### Module 2: High-Speed Local Processing
*Ditch slow legacy libraries and process data at blazing speeds using modern, Rust-backed tools.*

- [ ] **Lesson 2.1: Columnar Storage**
  - Why CSVs fail at scale. Understanding the Parquet file format.
- [ ] **Lesson 2.2: SOTA DataFrames (Polars)**
  - Introduction to Polars: lazy evaluation, multi-threading, and vectorization.
- [ ] **Lesson 2.3: In-Memory Analytics (DuckDB)**
  - Using DuckDB to query files directly without a database server.
- [ ] **💻 Hands-On Lab 2: The Fast Extractor**
  - Use Polars to clean a massive, messy CSV dataset.
  - Export the cleaned data to partitioned `.parquet` files.
  - Query the Parquet files instantly via the DuckDB CLI.

### Module 3: The Local Data Lake
*Understand cloud-native object storage by building your own S3-compatible environment.*

- [ ] **Lesson 3.1: Object vs. Block Storage**
  - The decoupling of compute and storage in the Modern Data Stack.
- [ ] **Lesson 3.2: The S3 API & Python**
  - Interacting with object storage programmatically using `boto3`.
- [ ] **💻 Hands-On Lab 3: The Local Cloud**
  - Deploy MinIO (high-performance object storage) via Docker.
  - Automate the upload of your Parquet files from Lab 2 into MinIO buckets using Python.

### Module 4: Modern Transformation (dbt)
*Apply software engineering best practices (version control, testing, DRY) to your SQL pipelines.*

- [ ] **Lesson 4.1: Introduction to dbt-core**
  - The shift from ETL to ELT. Understanding models, materializations, and the DAG.
- [ ] **Lesson 4.2: Data Modeling Fundamentals**
  - Structuring data from raw staging to analytics-ready marts.
- [ ] **💻 Hands-On Lab 4: The dbt Pipeline**
  - Configure `dbt-core` and `dbt-duckdb` to read from your MinIO lake.
  - Build a modular SQL pipeline connecting staging and mart layers.
  - Implement YAML-based data quality tests (`not_null`, `unique`).

### Module 5: Open Table Formats & Big Data
*Bring transactional guarantees (ACID) to the messy files sitting in your data lake.*

- [ ] **Lesson 5.1: The Problem with Data Lakes**
  - Why `UPDATE` and `DELETE` operations fail on raw Parquet files.
- [ ] **Lesson 5.2: Distributed Compute & Open Tables**
  - PySpark fundamentals and the architecture of Apache Iceberg.
- [ ] **💻 Hands-On Lab 5: The Iceberg Time Machine**
  - Run Apache Spark locally.
  - Ingest raw data into MinIO using the Apache Iceberg format.
  - Perform row-level updates and execute a "time travel" query to view previous states.

### Module 6: Asset-Based Orchestration
*Automate your entire pipeline to run reliably based on schedules or data dependencies.*

- [ ] **Lesson 6.1: Containerizing Code**
  - Writing Dockerfiles to guarantee consistent execution environments.
- [ ] **Lesson 6.2: Modern Orchestration (Dagster)**
  - Shifting from task-based (Airflow) to asset-based scheduling.
- [ ] **💻 Hands-On Lab 6: The Automated Graph**
  - Deploy Dagster locally.
  - Map your Python extraction scripts and dbt models as Dagster software-defined assets.
  - Trigger a full end-to-end automated run via the Dagster UI.

### Module 7: Real-Time Event Streaming
*Transition from daily batch jobs to processing continuous streams of live data.*

- [ ] **Lesson 7.1: The Append-Only Log**
  - Understanding Kafka/Redpanda architecture: topics, producers, consumers, and offsets.
- [ ] **Lesson 7.2: Stream Processing**
  - Handling late-arriving data and tumbling windows.
- [ ] **💻 Hands-On Lab 7: The Live Feed**
  - Deploy Redpanda via Docker.
  - Write a Python producer to simulate live sensor/transaction data.
  - Write a consumer script to calculate rolling real-time aggregations.

### Module 8: Data Engineering for AI (Local LLMOps)
*Prepare unstructured data for Generative AI and Large Language Models using local GPU hardware.*

- [ ] **Lesson 8.1: Vector Embeddings & RAG**
  - Chunking strategies and converting text into high-dimensional numerical arrays.
- [ ] **Lesson 8.2: Vector Databases**
  - Storing and querying embeddings for semantic search.
- [ ] **💻 Hands-On Lab 8: The Local AI Backend**
  - Deploy ChromaDB or Milvus locally via Docker.
  - Serve a local embedding model using Ollama.
  - Write a pipeline that chunks documents, generates embeddings, loads them into the vector database, and executes a semantic search.

---
*Maintained by: [saadtahmid](https://github.com/saadtahmid)