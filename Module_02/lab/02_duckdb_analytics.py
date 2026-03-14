import duckdb
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants
DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_FILE = DATA_DIR / "cleaned_events.parquet"

def query_parquet_pure_sql() -> None:
    """
    Spins up an embedded DuckDB instance to query the Parquet file directly.
    We don't need to load the data into Postgres first!
    """
    logger.info("Starting up embedded DuckDB instance...")
    
    # Connecting to ':memory:' creates a completely embedded, temporary database.
    con = duckdb.connect(':memory:')
    
    if not PROCESSED_FILE.exists():
        logger.error(f"Cannot find {PROCESSED_FILE}. Run lab/01_fast_extractor.py first!")
        return

    logger.info(f"Using DuckDB to run full SQL aggregations directly on the Parquet file...")
    
    # Look closely at the FROM clause. 
    # DuckDB natively reads exactly the parquet file.
    # It will use Column Pruning to ONLY load 'user_name' and 'purchased_amt' memory.
    query = f"""
        SELECT 
            user_name,
            COUNT(*) as total_events,
            SUM(purchased_amt) as total_spent,
            MAX(purchased_amt) as max_single_purchase
        FROM '{PROCESSED_FILE}'
        GROUP BY user_name
        ORDER BY total_spent DESC;
    """
    
    # Execute the query and display the results cleanly using DuckDB's native polars converter
    results = con.execute(query).pl()
    
    logger.info(f"Query Results:\n{results}")

def main() -> None:
    try:
        query_parquet_pure_sql()
    except Exception as e:
        logger.error(f"DuckDB Analysis failed: {e}")

if __name__ == "__main__":
    main()