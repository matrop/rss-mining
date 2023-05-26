import os

# Airflow configuration
RAW_DATA_DIR = "/opt/airflow/python/data/raw"
TRANSFORMED_DATA_DIR = "/opt/airflow/python/data/transformed"
BASE_DIR = "/opt/airflow/python/data"

# Local configuration
# BASE_DIR = "/home/matrops/git/rss-mining/data" 
# RAW_DATA_DIR = os.path.join(BASE_DIR, "raw")
# TRANSFORMED_DATA_DIR = os.path.join(BASE_DIR, "transformed")

ZEIT_URL = "https://newsfeed.zeit.de/index"
FAZ_URL = "https://www.faz.net/rss/aktuell"
