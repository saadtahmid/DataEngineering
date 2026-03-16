from pyspark.sql import SparkSession
from datetime import datetime
import time

def create_spark_session() -> SparkSession:
    packages = [
        "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0",
        "org.apache.hadoop:hadoop-aws:3.3.4",
        "com.amazonaws:aws-java-sdk-bundle:1.12.262"
    ]

    spark = SparkSession.builder \
        .appName("IcebergTimeTravel") \
        .config("spark.jars.packages", ",".join(packages)) \
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
        .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.local.type", "hadoop") \
        .config("spark.sql.catalog.local.warehouse", "s3a://data-lake/lakehouse/") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel("WARN")
    return spark


def main():
    spark = create_spark_session()
    
    print("Initial Table State:")
    spark.sql("SELECT * FROM local.db.users").show()
    
    # Take a timestamp of the exact current moment
    # We delay briefly to ensure timestamp boundaries are clear
    time.sleep(2)
    snapshot_time = datetime.now()
    print(f"Recorded Time Travel Timestamp: {snapshot_time}")
    time.sleep(2)

    # 1. Execute an UPDATE and a DELETE
    # In pure Parquet this is impossible without rewriting files. Iceberg handles it seamlessly.
    print("Running ACID compliant UPDATE on Alice...")
    spark.sql("UPDATE local.db.users SET purchase_amount = 500 WHERE user_name = 'Alice'")
    
    print("Running ACID compliant DELETE on Charlie (GDPR compliance test)...")
    spark.sql("DELETE FROM local.db.users WHERE user_name = 'Charlie'")

    # 2. View new state
    print("Current State (After Update/Delete):")
    spark.sql("SELECT * FROM local.db.users").show()

    # 3. View Snapshot History
    # Every operation creates a new snapshot!
    print("Iceberg Table History/Snapshots:")
    spark.sql("SELECT * FROM local.db.users.history").show(truncate=False)

    # 4. TIME TRAVEL!
    # Let's query the table as it looked before our UPDATE/DELETE
    print(f"Time Traveling back to before the deletion: {snapshot_time}")
    time_travel_df = spark.read \
        .format("iceberg") \
        .option("as-of-timestamp", int(snapshot_time.timestamp() * 1000)) \
        .load("local.db.users")
        
    time_travel_df.show()

if __name__ == "__main__":
    main()
