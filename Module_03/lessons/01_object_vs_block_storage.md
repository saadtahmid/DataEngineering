# Lesson 3.1: Object vs. Block Storage

In the legacy era of Big Data (Hadoop/HDFS), compute and storage were tightly coupled. If you needed more data storage, you had to buy a physical server that contained both CPU and Hard Drives. This led to massive wasted resources.

The **Modern Data Stack (MDS)** is built on a fundamental paradigm shift: **The Decoupling of Compute and Storage.**

## Block Storage (Local Disk)
When you save a file to your local SSD (`/home/user/data.csv`) or an AWS EBS volume (EC2), you are using Block Storage.
- Files are split into fixed-size chunks (blocks).
- Managed by the Operating System's file system (EXT4, NTFS).
- **Pros:** Extremely fast for small reads/writes (like an Operating System running).
- **Cons:** Does not scale infinitely across a network. It is bound to the server it is attached to.

## Object Storage (The Data Lake)
Object Storage (like AWS S3, Google Cloud Storage, or **MinIO** locally) treats data differently.
- Data is stored as an `Object` within a flat `Bucket`.
- There is no real folder hierarchy, even though `data/2026/01/file.parquet` looks like a path. It's actually just one long string key.
- It sits behind an HTTP/REST API.
- **Pros:** Infinite scalability. You can store exabytes of data. Compute clusters (like DuckDB, Spark, Databricks) can scale completely independently of the storage size.
- **Cons:** You cannot easily "update" a single row in a 10GB file. You must overwrite the whole object (we solve this later with Apache Iceberg).

## Enter MinIO
In this module, we use **MinIO**. MinIO is a high-performance, S3-compatible object storage server. By using MinIO locally, any code we write using the `boto3` (AWS Python SDK) library will work *exactly the same* if we deployed it to a real AWS environment in production.