import requests
import psycopg2
from psycopg2.extras import execute_values
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# PostgreSQL connection parameters
PG_CREDS = {
    "host": "localhost",
    "port": "5432",
    "database": "de_database",
    "user": "de_user",
    "password": "de_password"
}

def fetch_users_from_api() -> List[Dict[str, Any]]:
    """
    Simulates extracting data from a third-party REST API.
    We are using a public placeholder API that returns user records in JSON format.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    logger.info(f"Extracting data from API: {url}")
    
    response = requests.get(url, timeout=10)
    response.raise_for_status() # Raise an exception for bad status codes
    
    data = response.json()
    logger.info(f"Successfully extracted {len(data)} user records.")
    return data

def setup_database_schema(conn) -> None:
    """
    Creates the destination table using standard relational database types.
    """
    logger.info("Initializing relational schema...")
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        api_user_id INT UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        username VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL,
        city VARCHAR(100),
        company_name VARCHAR(255),
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with conn.cursor() as cur:
        cur.execute(create_table_sql)
    conn.commit()
    logger.info("Schema setup complete.")

def load_data_to_postgres(conn, users: List[Dict[str, Any]]) -> None:
    """
    Transforms the nested JSON structure into flat tuples and loads 
    them into PostgreSQL efficiently using execute_values.
    """
    logger.info("Transforming JSON payload to flat records...")
    records = []
    
    for u in users:
        # Flatten the nested JSON payload
        record = (
            u['id'],
            u['name'],
            u['username'],
            u['email'],
            u['address']['city'],
            u['company']['name']
        )
        records.append(record)

    insert_sql = """
        INSERT INTO users (api_user_id, name, username, email, city, company_name)
        VALUES %s
        ON CONFLICT (api_user_id) DO UPDATE SET
            name = EXCLUDED.name,
            email = EXCLUDED.email,
            company_name = EXCLUDED.company_name;
    """
    
    logger.info("Loading records into PostgreSQL...")
    with conn.cursor() as cur:
        # execute_values is significantly faster than executing single INSERTS in a loop
        execute_values(cur, insert_sql, records)
    
    conn.commit()
    logger.info(f"Successfully heavily inserted/upserted {len(records)} records.")

def main() -> None:
    try:
        # 1. Extract
        raw_data = fetch_users_from_api()
        
        # 2. Connect
        conn = psycopg2.connect(**PG_CREDS)
        
        # 3. Setup
        setup_database_schema(conn)
        
        # 4. Load
        load_data_to_postgres(conn, raw_data)
        
    except psycopg2.Error as db_err:
        logger.error(f"Database error occurred: {db_err}")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            logger.info("Database connection closed.")

if __name__ == "__main__":
    main()