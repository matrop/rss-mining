from airflow.decorators import dag

import datetime

from AirflowUtils import rss_ingestion_taskflow
from Settings import IngestionSettings, airflowSettings
from FAZParser import FAZParser

ingestionSettings = IngestionSettings(
    ingestion_source_name="faz",
    ingestion_dag_name="fetch-sources.faz",
    rss_feed_url="https://www.faz.net/rss/aktuell",
    parser_class=FAZParser,
    raw_table_name="raw.faz",
    mart_table_name="mart_faz",
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
