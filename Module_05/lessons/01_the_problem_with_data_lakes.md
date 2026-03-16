# The Problem with Data Lakes

In Module 3, we built a Data Lake. We took large chunks of events, converted them to heavily compressed columnar `.parquet` files, and wrote them to object storage (MinIO/S3). 

This is cheap, fast, and scalable for *reading* massive datasets using DuckDB or Athena.

## The Cracks Begin to Show
However, pure Data Lakes suffer from severe operational problems:

1. **Schema Evolution:** What happens if a software engineer renames `purchase_amount` to `total_purchase_amt` in the application logic? The new Parquet files won't match the old Parquet files. If a DuckDB query spans across the entire bucket, it crashes due to a schema mismatch.
2. **ACID Transactions:** If an ingestion script crashes halfway through uploading 1,000 `.parquet` files, you now have a "dirty" read state. Downstream BI queries might retrieve partial datasets because the upload isn't "atomic".
3. **The Data Privacy Deletion Problem:** GDPR and CCPA require the ability to delete user data. If "User 123" asks to be deleted, you must find which massive immutable Parquet files contain User 123, rewrite those entire files completely without their row, and delete the old files. 

## The Lakehouse Solution
To solve this, the industry invented the **Lakehouse**—an architecture that brings Data Warehouse features (Transactions, Indexing, Schema Enforcement) onto Data Lake files. 

To achieve a Lakehouse, you need an **Open Table Format**. The three main competitors are:
1. **Delta Lake** (invented by Databricks)
2. **Apache Hudi** (invented by Uber)
3. **Apache Iceberg** (invented by Netflix & Apple)

This course focuses on **Iceberg**, which has become the de facto community standard due to its true open-source nature and vendor-neutral stance.
