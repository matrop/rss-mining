from airflow.decorators import dag

import datetime

from AirflowUtils import rss_ingestion_taskflow
from Settings import IngestionSettings, airflowSettings
from SZParser import SZParser

ingestionSettings = IngestionSettings(
    ingestion_source_name="sz",
    ingestion_dag_name="fetch-sources.sz",
    rss_feed_url="https://rss.sueddeutsche.de/alles",
    parser_class=SZParser,
    raw_table_name="raw.sz",
    mart_table_name="mart_sz",
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
