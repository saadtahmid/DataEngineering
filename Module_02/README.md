# Module 2: High-Speed Local Processing

Welcome to Module 2! In this module, we step away from traditional databases and legacy Python libraries (like Pandas). We are entering the era of the modern data stack characterized by **columnar storage**, **Rust-backed tooling**, and **serverless in-memory databases**.

## Lesson Structure
- `lessons/01_columnar_storage.md`: Why CSVs fail at scale and the architecture of the Parquet format.
- `lessons/02_sota_dataframes_polars.md`: Introduction to Polars, multi-threading, and lazy evaluation.
- `lessons/03_in_memory_analytics_duckdb.md`: Using DuckDB as an embedded SQL engine on top of files.

## Hands-On Lab Setup: The Fast Extractor

In this lab, we will use Python and Polars to extract and clean a dataset, write it to partitioned Parquet files locally, and query those files using DuckDB.

1. **Setup Python Environment**
   ```bash
   cd Module_02
   python3 -m venv .venv
   source .venv/bin/activate
   pip install polars pyarrow duckdb requests
   ```

2. **Run the Fast Extractor Script**
   ```bash
   python3 lab/01_fast_extractor.py
   ```

3. **Run the Serverless Analytics via CLI**
   Instead of writing Python to connect to our database, we will use the embedded DuckDB CLI to directly analyze our folder of generated Parquet files using the raw SQL found in `lab/02_query_cli.sql`.
   
   ```bash
   # Download DuckDB CLI (if not installed)
   wget https://github.com/duckdb/duckdb/releases/download/v1.1.1/duckdb_cli-linux-amd64.zip
   unzip duckdb_cli-linux-amd64.zip
   
   # Run a CLI Query directly against our partitioned Parquet directory
   ./duckdb -c "SELECT user_name, SUM(purchased_amt) FROM read_parquet('data/cleaned_events/*/*.parquet') GROUP BY user_name;"
   ```
