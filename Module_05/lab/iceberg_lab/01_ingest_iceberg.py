from pyspark.sql import SparkSession
import os

def create_spark_session() -> SparkSession:
    """
    Creates a Spark session configured to write Apache Iceberg tables to MinIO.
    Downloads necessary Iceberg and AWS/Hadoop jar dependencies automatically.
    """
    # Specifically target Spark 3.5 and Iceberg 1.5.0
    packages = [
        "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0",
        "org.apache.hadoop:hadoop-aws:3.3.4",
        "com.amazonaws:aws-java-sdk-bundle:1.12.262"
    ]

    spark = SparkSession.builder \
        .appName("IcebergLocalLakehouse") \
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
    
    # Decrease logging noise
    spark.sparkContext.setLogLevel("WARN")
    return spark

def main():
    spark = create_spark_session()
    print("Spark Session Created Successfully with Iceberg capabilities!")

    # 1. Provide mock DataFrame representing clean data arriving
    data = [
        (1, "Alice", 100.50),
        (2, "Bob", 200.00),
        (3, "Charlie", 50.00)
    ]
    columns = ["user_id", "user_name", "purchase_amount"]
    
    df = spark.createDataFrame(data, schema=columns)
    
    # 2. Write DataFrame as a new Apache Iceberg Table
    # The format is 'catalog.db.table_name'
    print("Writing Data as Iceberg Table to MinIO...")
    df.write \
        .format("iceberg") \
        .mode("overwrite") \
        .saveAsTable("local.db.users")
        
    print("Iceberg Table created successfully. You can verify the /lakehouse/db/users directory in MinIO.")

    # 3. Read it back via Spark SQL to confirm
    print("Reading data back via Spark SQL:")
    spark.sql("SELECT * FROM local.db.users").show()

if __name__ == "__main__":
    main()
