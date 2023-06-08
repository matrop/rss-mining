import datetime
import Settings

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

CONFIG = Settings.SOURCE_CONFIG["SZ"]


def get_rss_feed():
    from RSSGetter import RSSGetter

    rss_getter = RSSGetter(CONFIG["url"])
    rss_getter.save_to_file()
    return rss_getter.output_filename


def parse_rss_feed(**kwargs):
    from SZParser import SZParser

    ti = kwargs["ti"]
    rss_filename = ti.xcom_pull(task_ids="get_rss_feed")

    xml_parser = SZParser(rss_filename)
    xml_parser.save_to_csv()
    return xml_parser.output_filename


def load_csv(**kwargs):
    from airflow.providers.postgres.hooks.postgres import PostgresHook

    ti = kwargs["ti"]
    parsed_rss_filename = ti.xcom_pull(task_ids="parse_rss_feed")

    hook = PostgresHook(postgres_conn_id="postgres_default")
    hook.bulk_load(CONFIG["raw_table_name"], parsed_rss_filename)


with DAG(
    dag_id=CONFIG["ingestion_dag_name"],
    schedule_interval=None,
    start_date=datetime.datetime(2021, 1, 1),
    catchup=False,
) as dag:
    # TODO: Change to new decorator-based notation
    get_rss = PythonOperator(task_id="get_rss_feed", python_callable=get_rss_feed)
    parse_rss = PythonOperator(
        task_id="parse_rss_feed",
        python_callable=parse_rss_feed,
        provide_context=True,
    )

    truncate_landing_table = PostgresOperator(
        task_id="truncate_landing_table",
        postgres_conn_id="postgres_default",
        sql=f"TRUNCATE {CONFIG['raw_table_name']}",
    )

    load_csv_file = PythonOperator(task_id="load_csv", python_callable=load_csv)

    get_rss >> parse_rss >> truncate_landing_table >> load_csv_file