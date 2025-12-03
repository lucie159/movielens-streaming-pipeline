import time
import json
import os

# --- CONFIGURATION ---
# On écrit dans un fichier log local dans /tmp 
LOG_FILE = "/tmp/streaming_movies/movies_data.log"
DATA_FILE = "movieslens/ratings/u.data"    #provenant de hdfs

print(f"Démarrage du logging vers '{LOG_FILE}'...")

try:
    # On s'assure que le fichier source existe
    if not os.path.exists(DATA_FILE):
        raise FileNotFoundError(f"Le fichier source {DATA_FILE} est introuvable.")

    with open(DATA_FILE, 'r') as f_source, open(LOG_FILE, 'a') as f_log:
        count = 0
        for line in f_source:
            columns = line.split('\t')
            
            # Création du dictionnaire
            rating_data = {
                "user_id": int(columns[0]),
                "movie_id": int(columns[1]),
                "rating": int(columns[2]),
                "timestamp": int(columns[3].strip())
            }
            
            # ÉCRITURE DANS LE FICHIER (JSON sur une ligne + retour à la ligne)
            f_log.write(json.dumps(rating_data) + "\n")
            f_log.flush()  # Force l'écriture immédiate sur le disque
            
            count += 1
            print(f" {count} logs écrits...", end="\r")
            
            time.sleep(0.1) # Simulation temps réel

except Exception as e:
    print(f"\n ERREUR : {e}")
except KeyboardInterrupt:
    print("\n Arrêt du logger.")
