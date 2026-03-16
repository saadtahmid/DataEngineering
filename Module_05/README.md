# Module 5: Open Table Formats & Big Data

Welcome to Module 5! Up until now, our data lake consisted of physical directories of `.parquet` files. This works flawlessly for reads, but the moment you need to `UPDATE` an individual row or guarantee ACID compliance (atomicity, consistency, isolation, durability), raw data lakes fail. 

You cannot simply *update* a record in a 200MB Parquet file on S3—you have to rewrite the entire file. When multiple processes try to do this simultaneously, you get data corruption. 

We solve this using **Open Table Formats**, specifically **Apache Iceberg**, which brings database-like features to cheap object storage.

## Lesson Structure
- `lessons/01_the_problem_with_data_lakes.md`: Why Data Lakes needed to evolve into Lakehouses.
- `lessons/02_distributed_compute_and_open_tables.md`: An introduction to PySpark and the fundamental architecture of Apache Iceberg.

## Hands-On Lab: The Iceberg Time Machine

In this lab, we will use distributed compute via **PySpark** running locally to write an Iceberg table onto our MinIO cluster from Module 3. Then, we will intentionally delete a record, and use Iceberg's "Time Travel" feature to instantly restore it from an older snapshot.

1. **Ensure MinIO is Running**
   ```bash
   cd ../Module_03
   docker compose up -d
   cd ../Module_05
   ```

2. **Setup PySpark Environment**
   Because PySpark operates in the JVM, ensure you have Java installed on your Ubuntu machine (`sudo apt install default-jre -y`).
   ```bash
   cd lab/iceberg_lab
   python3 -m venv .venv
   source .venv/bin/activate
   pip install pyspark==3.5.0
   ```

3. **Run the Lab**
   ```bash
   # Script 1 downloads necessary Java dependencies via Ivy and creates the Iceberg table
   python3 01_ingest_iceberg.py
   
   # Script 2 performs an update/delete and then travels back in time
   python3 02_time_travel.py
   ```
