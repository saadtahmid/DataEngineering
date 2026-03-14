# Lesson 2.3: In-Memory Analytics (DuckDB)

In Module 1, we used PostgreSQL. PostgreSQL is an incredible **OLTP (Online Transaction Processing)** engine—it handles thousands of small inserts and updates perfectly.

However, for Data Engineering analytics and aggregations (OLAP), standing up a full database server just to run reports on a Parquet file is massive overhead.

## DuckDB: The SQLite for Data Analysis

DuckDB is a serverless, in-process SQL OLAP database.

**Why DuckDB is SOTA:**
1. **Serverless (Embedded):** DuckDB runs inside your Python process. There are no ports to map, no background services to configure, and zero network latency overhead.
2. **Native Arrow / Polars Integration:** DuckDB can query a Polars DataFrame or a Parquet file directly with *zero-copy* memory transfers.
3. **Columnar Vectorized Engine:** While Postgres evaluates rows one at a time, DuckDB processes data in "vectors" (batches of columns) leveraging CPU cache efficiency.

We will use DuckDB as our highly-agile query layer to inspect the Parquet files we generate via Polars.