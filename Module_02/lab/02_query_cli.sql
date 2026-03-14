-- =========================================================================
-- Hands-On Lab 2: Querying Partitioned Parquet Data via DuckDB CLI
-- =========================================================================

-- First, ensure you have the DuckDB CLI installed on your Ubuntu machine:
--   wget https://github.com/duckdb/duckdb/releases/download/v1.1.1/duckdb_cli-linux-amd64.zip
--   unzip duckdb_cli-linux-amd64.zip
--   sudo mv duckdb /usr/local/bin/

-- Alternatively, launch DuckDB in your terminal from the Module_02 folder:
--   duckdb

-- -------------------------------------------------------------------------
-- Query 1: Exploring Parquet Metadata
-- Because Parquet carries its own schema, we don't need to define a table.
-- We can dynamically read across all partitioned folders using a glob (*).
-- -------------------------------------------------------------------------
DESCRIBE SELECT * FROM read_parquet('data/cleaned_events/*/*.parquet');

-- -------------------------------------------------------------------------
-- Query 2: The Analytical Query (Partition Pruning)
-- DuckDB is smart enough to realize that if we specify an `event_date`,
-- it ONLY needs to read the data from that specific partition folder, 
-- saving massive amounts of RAM and I/O.
-- -------------------------------------------------------------------------
SELECT 
    user_name,
    COUNT(*) as total_events,
    SUM(purchased_amt) as total_spent,
    MAX(purchased_amt) as max_single_purchase
FROM read_parquet('data/cleaned_events/*/*.parquet')
WHERE event_date = '2026-03-14'
GROUP BY user_name
ORDER BY total_spent DESC;
