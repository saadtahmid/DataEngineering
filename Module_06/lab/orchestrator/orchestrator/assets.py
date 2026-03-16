from dagster import asset
import logging

logger = logging.getLogger("dagster")

@asset(group_name="extract")
def extract_raw_events() -> None:
    """
    Symbolic asset representing our Polars extraction from Module 2.
    In a real Dagster project, we would invoke Polars here to read from 
    the API and write to local disk.
    """
    logger.info("Executing fast Polars extraction...")
    logger.info("Mocked: Data saved to standard location.")


@asset(deps=["extract_raw_events"], group_name="load")
def load_to_minio() -> None:
    """
    Symbolic asset representing uploading Parquet configs to MinIO Data Lake.
    Depends on the execution of extract_raw_events first.
    """
    logger.info("Connecting to local MinIO via boto3...")
    logger.info("Mocked: Transferred parquet partition datasets.")

