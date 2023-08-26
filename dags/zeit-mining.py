from airflow.decorators import dag

import datetime

from AirflowUtils import rss_ingestion_taskflow
from Settings import IngestionSettings, airflowSettings
from ZEITParser import ZEITParser

ingestionSettings = IngestionSettings(
    ingestion_dag_name="zeit-mining",
    rss_feed_url="https://newsfeed.zeit.de/index",
    parser_class=ZEITParser,
    raw_table_name="raw.zeit",
    mart_table_name="mart_zeit",
)


@dag(
    dag_id=ingestionSettings.ingestion_dag_name,
    schedule_interval=None,
    start_date=datetime.datetime(2021, 1, 1),
    catchup=False,
)
def ingestion_taskflow():
    rss_ingestion_taskflow(ingestionSettings, airflowSettings)


ingestion_dag = ingestion_taskflow()
