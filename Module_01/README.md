# Module 1: The Core Languages (SQL & Python)

Welcome to Module 1! Before we can build complex, distributed Data Lakes or use bleeding-edge Rust-based dataframes, we must master the foundational tools of Data Engineering: 
1. **Relational Databases (PostgreSQL)**
2. **Advanced SQL (CTEs, Window Functions)**
3. **Python (API interactions, JSON parsing)**

## Lesson Structure
- `lessons/01_postgresql_fundamentals.md`: Understanding relational modeling.
- `lessons/02_advanced_sql.md`: How to think in sets using CTEs and Window Functions.
- `lessons/03_ingest_api_to_postgres.py`: Our first Python script to extract data from a web API and load it strictly into PostgreSQL.

## Hand-on Lab Setup

1. **Start the Database**
   ```bash
   cd Module_01
   docker compose up -d
   ```

2. **Setup Python Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install requests psycopg2-binary
   ```

3. **Run the Ingestion Script**
   ```bash
   python3 lessons/03_ingest_api_to_postgres.py
   ```

4. **Run Advanced Analytics**
   Connect to your database and run the queries found in `lab/advanced_queries.sql` to analyze the data!
