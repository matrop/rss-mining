import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.decorators import task

with DAG(
    dag_id="init_db",
    schedule_interval=None,
    start_date=datetime.datetime(2021, 1, 1),
    catchup=False,
) as dag:

    @task(task_id="create_postgres_connection")
    def create_postgres_connection():
        from airflow.models import Connection
        from airflow import settings

        # TODO: This fails when connection already exists
        # TODO: Put credentials somewhere safe

        new_conn = Connection(
            conn_id="postgres_default",
            conn_type="postgres",
            login="airflow",
            password="airflow",
            host="postgres",
            port=5432,
        )

        session = settings.Session()
        session.add(new_conn)
        session.commit()
        session.close()

    init_scripts = [
        "create_schema_raw",
        "create_raw_zeit",
    ]

    tasks = [
        PostgresOperator(
            task_id=scriptname,
            postgres_conn_id="postgres_default",
            sql=f"sql/{scriptname}.sql",
        )
        for scriptname in init_scripts
    ]

    create_postgres_connection() >> tasks[0]

    for i in range(len(init_scripts) - 1):
        tasks[i] >> tasks[i + 1]
