import os
import boto3
import logging
from pathlib import Path
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants for Local MinIO Data Lake
MINIO_ENDPOINT = "http://localhost:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
BUCKET_NAME = "data-lake"

# Directory where Module 2 outputted the partitioned Parquet files
SOURCE_DIR = Path(__file__).parent.parent.parent / "Module_02" / "data" / "cleaned_events"

def get_s3_client():
    """
    Initializes a Boto3 S3 client pointed to our local MinIO instance.
    Why this is SOTA: The exact same boto3 API is used for AWS S3 in production.
    """
    return boto3.client(
        's3',
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name='us-east-1' # Required for AWS API standards, even locally
    )

def ensure_bucket_exists(s3_client) -> None:
    """Verifies that the target bucket exists, creating it if it doesn't."""
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        logger.info(f"Bucket '{BUCKET_NAME}' already exists.")
    except ClientError:
        logger.info(f"Bucket '{BUCKET_NAME}' not found. Creating it...")
        s3_client.create_bucket(Bucket=BUCKET_NAME)

def upload_directory_to_datalake(s3_client) -> None:
    """
    Traverses the local directory (Block Storage) and uploads partitioned 
    files to MinIO (Object Storage), maintaining the partition 'Hive' structure 
    (event_date=XXXX) in the S3 keys.
    """
    
    if not SOURCE_DIR.exists():
        logger.error(f"Source directory {SOURCE_DIR} does not exist. Did you run Module 2's lab?")
        return

    logger.info(f"Scanning local block storage at {SOURCE_DIR}...")
    
    upload_count = 0
    # Walk the directory tree
    for root, _, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith('.parquet'):
                local_path = os.path.join(root, file)
                
                # To maintain the partition schema, we calculate the relative path.
                # E.g., 'event_date=2026-03-14/data.parquet'
                relative_path = os.path.relpath(local_path, SOURCE_DIR)
                
                # In S3, we structure our lake. Let's place it in a 'bronze/events/' prefix path
                s3_key = f"bronze/events/{relative_path}"
                
                logger.info(f"Uploading {local_path} -> s3://{BUCKET_NAME}/{s3_key}")
                
                # Upload the object
                s3_client.upload_file(local_path, BUCKET_NAME, s3_key)
                upload_count += 1
                
    logger.info(f"Successfully uploaded {upload_count} files to the Data Lake.")

def main():
    try:
        s3_client = get_s3_client()
        ensure_bucket_exists(s3_client)
        upload_directory_to_datalake(s3_client)
    except Exception as e:
        logger.error(f"Data Lake Migration failed: {e}")

if __name__ == "__main__":
    main()