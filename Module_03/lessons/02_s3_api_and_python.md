# Lesson 3.2: The S3 API & Python

Because Object Storage is disconnected from the local operating system, we can no longer use standard Python OS libraries like `open("file.csv", "r")` or `os.listdir()` to manage our files.

Instead, we must communicate with the storage using the **S3 API**. The S3 API has become the de-facto standard language for interacting with Object Storage globally, supported by AWS, Google, Azure, and MinIO.

## Boto3
In Python, the official AWS SDK is called `boto3`. 

Even though we are not using AWS (we are using Local MinIO), we still use `boto3` because MinIO translates the S3 API calls flawlessly.

### Core Concepts in Boto3

1. **The Client vs The Resource:**
   - `boto3.client('s3')`: The low-level interface. It maps directly 1:1 with the S3 HTTP API. Returns dictionary responses.
   - `boto3.resource('s3')`: A higher-level, object-oriented interface. (AWS is slowly deprecating aspects of this, so standard Data Engineering relies primarily on the `client`).

2. **Keys (Not Paths):**
   In S3, an object name is called a `Key`. 
   `"raw-zone/events/2026-03-14/data.parquet"` is just a string key. There are no actual folders named `raw-zone` or `events`.

3. **Interfacing with local MinIO:**
   To make `boto3` talk to our local docker container instead of real AWS, we simply have to pass the `endpoint_url` pointing to our localhost.

```python
import boto3

s3_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin'
)
```

In the next lab, we will use this exact setup to traverse our local hard drive and push the partitioned Parquet files from Module 2 up into our local Data Lake!