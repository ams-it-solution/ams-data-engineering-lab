import os

os.environ["PYSPARK_SUBMIT_ARGS"] = "--packages org.postgresql:postgresql:42.7.3 pyspark-shell"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum

# Environment variables
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# JDBC URL
jdbc_url = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Spark session
spark = SparkSession.builder \
    .appName("SalesETL") \
    .getOrCreate()

# Read from PostgreSQL
df = spark.read.format("jdbc").options(
    url=jdbc_url,
    driver="org.postgresql.Driver",
    dbtable="sales",
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
).load()

# Transformation
result = df.groupBy("product") \
    .agg(
        _sum(col("amount") * col("price")).alias("total_revenue")
    )

# Write back to PostgreSQL
result.write.format("jdbc").options(
    url=jdbc_url,
    driver="org.postgresql.Driver",
    dbtable="sales_summary",
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
).mode("overwrite").save()

spark.stop()