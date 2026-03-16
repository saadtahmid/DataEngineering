# Module 4: Modern Transformation (dbt)

Welcome to Module 4! So far, you've extracted data using Polars and loaded it into an S3-compatible Data Lake (MinIO) as Parquet files. Now it's time to transform that data into analytical models.

We will use **dbt (data build tool)** backed by **DuckDB** to define our pipeline entirely in SQL while enforcing Software Engineering best practices like version control, modularity, and automated testing.

## Lesson Structure
- `lessons/01_introduction_to_dbt.md`: The shift from ETL to ELT, and understanding the Directed Acyclic Graph (DAG).
- `lessons/02_data_modeling_fundamentals.md`: Moving from raw data (bronze) to staging (silver) to analytics-ready marts (gold).

## Hands-On Lab Setup: The dbt Pipeline

In this lab, we configure a dbt project that maps to our local MinIO lake, validates data via YAML tests, and transforms our events into a clean fact table.

1. **Ensure your Data Lake is Running**
   Because we depend on data from Module 3, make sure your MinIO instance is still running:
   ```bash
   cd ../Module_03
   docker compose up -d
   cd ../Module_04
   ```

2. **Setup Python Environment & Install dbt-duckdb**
   ```bash
   cd lab/my_platform
   python3 -m venv .venv
   source .venv/bin/activate
   pip install dbt-core dbt-duckdb
   ```

3. **Run the dbt Pipeline**
   We have explicitly located the `profiles.yml` inside `lab/my_platform` to keep everything local.
   ```bash
   # Test the connection to DuckDB & MinIO
   dbt debug --profiles-dir .
   
   # Run the SQL models (Staging -> Marts)
   dbt run --profiles-dir .
   
   # Run our defined YAML data quality tests
   dbt test --profiles-dir .
   ```
