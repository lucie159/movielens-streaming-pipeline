from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

spark = SparkSession.builder \
    .appName("KafkaStreaming") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test-topic") \
    .load()

df2 = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

query = df2.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()

