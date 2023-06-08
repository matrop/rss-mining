import datetime
import os

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.decorators import task

from dotenv import load_dotenv, find_dotenv

from sqlalchemy.exc import IntegrityError

env_file = find_dotenv(os.path.join(".database.env"))
load_dotenv(env_file)

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

        print("User: " + os.environ.get("USER"))

        new_conn = Connection(
            conn_id="postgres_default",
            conn_type="postgres",
            login=os.environ.get("USER"),
            password=os.environ.get("PASSWORD"),
            host=os.environ.get("HOST"),
            port=os.environ.get("PORT"),
        )

        session = settings.Session()
        try:
            session.add(new_conn)
            session.commit()
        except IntegrityError:
            print(f"Connection '{new_conn.conn_id}' already exists, skipping...")

        session.close()

    init_scripts = [
        "create_schema_raw",
        "create_raw_zeit",
        "create_raw_faz",
        "create_raw_sz",
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
