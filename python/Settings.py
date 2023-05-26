import os

# RAW_DATA_DIR = "/opt/airflow/python/data/raw"
# TRANSFORMED_DATA_DIR = "/opt/airflow/python/data/transformed"

# BASE_DIR = "/opt/airflow/python/data"

BASE_DIR = "/home/matrops/git/zeit-mining/data" 
RAW_DATA_DIR = os.path.join(BASE_DIR, "raw")
TRANSFORMED_DATA_DIR = os.path.join(BASE_DIR, "transformed")

ZEIT_URL = "https://newsfeed.zeit.de/index"
