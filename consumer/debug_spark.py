from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, LongType

# --- CONFIG ---
KAFKA_TOPIC = "movielens_ratings"
KAFKA_SERVER = "localhost:9092"

spark = SparkSession.builder \
    .appName("DebugStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Schéma attendu
json_schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("movie_id", IntegerType(), True),
    StructField("rating", IntegerType(), True)
])

# Lecture Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .load()

# Extraction (On garde aussi la colonne 'value' brute pour voir s'il y a un souci)
parsed_df = kafka_stream.select(
    col("value").cast("string").alias("raw_json"),
    from_json(col("value").cast("string"), json_schema).alias("data")
).select("raw_json", "data.*")

# Affichage Console (Au lieu de HDFS)
query = parsed_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
