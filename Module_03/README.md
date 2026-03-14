# Module 3: The Local Data Lake

In the modern data stack, compute and storage are fully decoupled. In this module, we transition away from saving files to our local OS filesystem (block storage) and move entirely into a centralized **Data Lake (Object Storage)** using MinIO and the `boto3` python API.

## Lesson Structure
- `lessons/01_object_vs_block_storage.md`: The philosophical and physical differences between hard drives and data lakes.
- `lessons/02_s3_api_and_python.md`: How to communicate programmatically with S3-compatible endpoints using Python's `boto3` library.

## Hands-On Lab Setup: The Local Cloud

In this lab, we will start a local S3-compatible cloud (MinIO) and write a Python script to dynamically upload the partitioned `.parquet` files we generated back in **Module 2** into our local Data Lake.

1. **Start the Data Lake**
   ```bash
   cd Module_03
   docker compose up -d
   ```
   *You can view the MinIO UI at http://localhost:9001 (Username: `minioadmin`, Password: `minioadmin`)*

2. **Setup Python Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install boto3
   ```

3. **Run the Cloud Migration Script**
   ```bash
   # This script reads Module 2's output and pushes it to MinIO via boto3
   python3 lab/01_upload_to_minio.py
   ```
