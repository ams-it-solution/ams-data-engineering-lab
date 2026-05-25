import os
os.environ["PYSPARK_SUBMIT_ARGS"] = "--packages org.postgresql:postgresql:42.7.3 pyspark-shell"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum

spark = SparkSession.builder \
    .appName("SalesETL") \
    .getOrCreate()

# 1. Ler do Postgres
df = spark.read.format("jdbc").options(
    url="jdbc:postgresql://postgres:5432/airflow",
    driver="org.postgresql.Driver",
    dbtable="sales",
    user="admin",
    password="admin"
).load()

# 2. Transformação
result = df.groupBy("product") \
    .agg(
        _sum(col("amount") * col("price")).alias("total_revenue")
    )

# 3. Escrever resultado de volta no Postgres
result.write.format("jdbc").options(
    url="jdbc:postgresql://postgres:5432/airflow",
    driver="org.postgresql.Driver",
    dbtable="sales_summary",
    user="admin",
    password="admin"
).mode("overwrite").save()

spark.stop()