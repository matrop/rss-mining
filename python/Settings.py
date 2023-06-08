import os

# Airflow configuration
RAW_DATA_DIR = "/opt/airflow/python/data/raw"
TRANSFORMED_DATA_DIR = "/opt/airflow/python/data/transformed"
BASE_DIR = "/opt/airflow/python/data"

# Local configuration
# BASE_DIR = "/home/matrops/git/rss-mining/data" 
# RAW_DATA_DIR = os.path.join(BASE_DIR, "raw")
# TRANSFORMED_DATA_DIR = os.path.join(BASE_DIR, "transformed")

SOURCE_CONFIG = {
    "ZEIT": {
        "url": "https://newsfeed.zeit.de/index",
        "raw_table_name": "raw.zeit",
        "ingestion_dag_name": "zeit-mining",
    },
    "FAZ": {
        "url": "https://www.faz.net/rss/aktuell",
        "raw_table_name": "raw.faz",
        "ingestion_dag_name": "faz-mining",
    },
    "SZ": {
        "url": "https://rss.sueddeutsche.de/alles",
        "raw_table_name": "raw.sz",
        "ingestion_dag_name": "sz-mining",
    },
}