import polars as pl
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = Path(__file__).parent.parent / "data"
RAW_FILE = DATA_DIR / "raw_events.csv"
PROCESSED_DIR = DATA_DIR / "cleaned_events"

def create_dummy_csv() -> None:
    """Creates a local messy CSV file since we are building purely local."""
    DATA_DIR.mkdir(exist_ok=True)
    if not RAW_FILE.exists():
        logger.info("Creating a dummy raw CSV file...")
        # Simulate messy data with nulls and unstandardized text
        csv_data = """event_id,User_Name,purchased_AMT,event_TIMESTAMP
1,Alice_Smith,100.50,2026-03-14T10:00:00
2,BOB_JONES,,2026-03-14T11:30:00
3,charlie_brown,50.00,2026-03-14T12:15:00
4,Alice_Smith,25.00,2026-03-14T13:45:00
5,invalid_user,-99.00,2026-03-14T14:00:00
"""
        RAW_FILE.write_text(csv_data)
        logger.info(f"Created {RAW_FILE}")

def clean_data_with_polars() -> None:
    """
    Reads the messy CSV using Polars, cleans the data, and writes to Parquet.
    We use Polars expressions to do this blazingly fast.
    """
    logger.info("Reading raw data via Polars Lazy API...")
    
    # 1. Use scan_csv for lazy evaluation instead of read_csv.
    # It builds an execution graph and runs it efficiently.
    lazy_df = pl.scan_csv(RAW_FILE)
    
    # 2. Apply transformations using expressive Polars API
    cleaned_df = (
        lazy_df
        # Standardize column names to lowercase
        .rename({
            "User_Name": "user_name", 
            "purchased_AMT": "purchased_amt",
            "event_TIMESTAMP": "event_timestamp"
        })
        # Clean user names: convert to lowercase and replace underscores with spaces
        .with_columns([
            pl.col("user_name").str.to_lowercase().str.replace("_", " "),
            # Cast timestamp string to actual Datetime object
            pl.col("event_timestamp").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S")
        ])
        # Create a specific date column for partitioning
        .with_columns([
            pl.col("event_timestamp").dt.date().alias("event_date")
        ])
        # Filter out bad data: purchases cannot be null or negative
        .filter(
            pl.col("purchased_amt").is_not_null() & 
            (pl.col("purchased_amt") > 0.0)
        )
    )

    # 3. Collect triggers the execution of the optimized query graph
    logger.info("Collecting and executing Polars optimization graph...")
    final_df = cleaned_df.collect()
    
    logger.info(f"Cleaned DataFrame Result:\n{final_df}")
    
    # 4. Write output to columnar Parquet format using partitioning
    logger.info(f"Writing heavily compressed columnar data to {PROCESSED_DIR}")
    
    # Partitioning physically splits the data into sub-directories (e.g. event_date=2026-03-14/)
    # This exponentially speeds up downstream queries that filter by date!
    final_df.write_parquet(
        PROCESSED_DIR,
        use_pyarrow=True,
        pyarrow_options={"partition_cols": ["event_date"]}
    )
    logger.info("Write successful.")

def main():
    try:
        create_dummy_csv()
        clean_data_with_polars()
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    main()