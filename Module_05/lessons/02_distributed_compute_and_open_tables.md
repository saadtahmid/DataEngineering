# Distributed Compute & Open Tables

To interact with Iceberg, we need an engine capable of writing complex metadata alongside our Parquet files. While DuckDB can *read* Iceberg tables, modifying them at scale in production still heavily relies on **Apache Spark**.

## What is Apache Spark?
Spark is a massively parallel, distributed processing engine. While engines like Polars are optimized for single-node machines (making them exponentially faster for certain workloads), Spark is built to distribute workloads across hundreds of servers (nodes).

Spark uses the JVM (Java Virtual Machine) under the hood, but as Data Engineers, we interface with it using **PySpark**. It utilizes memory heavily, allowing it to cache datasets rather than writing intermediate steps to disk.

## How Apache Iceberg Works
Iceberg is not an execution engine (like Spark) or a file format (like Parquet). Iceberg is a **Metadata Layer**.

When PySpark writes a dataframe to an Iceberg table, it writes three things:
1. **Data Files**: Standard `.parquet` files.
2. **Manifest Files**: Small files instructing the engine exactly *which* data files belong to the current state of the table. It maps out file paths and statistics (e.g., "File A has `user_id` values from 1 to 500").
3. **Snapshot file**: Every time you `INSERT`, `UPDATE`, or `DELETE`, Iceberg creates a new Snapshot ID. 

### Why the Metadata Layer Matters
Because Iceberg tracks Snapshots and Manifests, when you run:
`DELETE FROM my_table WHERE user_id = '5'`

Iceberg doesn't immediately open the massive Parquet files and rewrite them. Instead, it writes a small "delete file" (Copy-on-Write or Merge-on-Read methodology) and updates its Snapshot. The next time you query the table, Iceberg knows to ignore `user_id 5`.

This architecture enables **Time Travel**. Because previous snapshots are preserved, you can append `TIMESTAMP AS OF X` to your SQL query to instruct the engine to read the older Manifest files, letting you view exactly what the table looked like two weeks ago.
