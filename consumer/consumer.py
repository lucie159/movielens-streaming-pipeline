from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, LongType, StringType

# --- CONFIGURATION ---
KAFKA_TOPIC = "movielens_ratings"
KAFKA_SERVER = "localhost:9092"

# CHEMIN DE SORTIE
HDFS_OUTPUT_PATH = "hdfs://localhost:9000/user/hadoop/streaming/results/clean_ratings"
CHECKPOINT_PATH = "hdfs://localhost:9000/user/hadoop/streaming/checkpoints/clean_ratings"



# 1. Initialisation de la Session Spark (Avec support HIVE)
spark = SparkSession.builder \
    .appName("MovieLensStreaming") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

print("🚀 Démarrage du Consommateur Streaming (Via Filebeat)...")

# 2. Définition du schéma (Ce que Filebeat nous envoie)
# Filebeat ajoute des champs comme "@timestamp" ou "host", mais Spark
# va ignorer ceux qu'on ne liste pas ici. On ne garde que nos données.
json_schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("movie_id", IntegerType(), True),
    StructField("rating", IntegerType(), True),
    StructField("timestamp", LongType(), True)
])

# 3. Lecture du flux Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# 4. Parsing du JSON
# Comme on a mis 'json.keys_under_root: true' dans Filebeat,
# le JSON est directement accessible, pas besoin de fouiller dans "message".
ratings_df = kafka_stream.select(
    from_json(col("value").cast("string"), json_schema).alias("data")
).select("data.*")

# 5. Chargement de la table statique MOVIES depuis Hive
print("Chargement de la table movies depuis Hive...")
movies_df = spark.table("movies").select("movie_id", "title")

# 6. La JOINTURE (Stream + Static)
# On ajoute le titre du film 
enriched_df = ratings_df.filter("movie_id IS NOT NULL").join(movies_df, "movie_id", "left")

# 7. Écriture en continu dans HDFS (Format Parquet)
query = enriched_df.writeStream \
    .format("parquet") \
    .option("path", HDFS_OUTPUT_PATH) \
    .option("checkpointLocation", CHECKPOINT_PATH) \
    .outputMode("append") \
    .start()

print(f"Streaming en cours... Écriture dans {HDFS_OUTPUT_PATH}")

query.awaitTermination()
