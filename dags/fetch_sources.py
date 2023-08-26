from airflow import DAG
from airflow.operators.subdag import SubDagOperator
from airflow.operators.bash import BashOperator

import datetime

from faz_mining import ingestion_dag as faz_ingestion_dag
from sz_mining import ingestion_dag as sz_ingestion_dag
from zeit_mining import ingestion_dag as zeit_ingestion_dag

from Settings import airflowSettings

with DAG(
    dag_id="fetch-sources",
    start_date=datetime.datetime(2022, 1, 1),
    schedule=datetime.timedelta(minutes=30),
    catchup=False,
) as dag:
    subdags = [
        ("faz", faz_ingestion_dag),
        ("sz", sz_ingestion_dag),
        ("zeit", zeit_ingestion_dag),
    ]

    subdag_operators = [SubDagOperator(task_id=task_id, subdag=subdag) for task_id, subdag in subdags]

    update_central_mart = BashOperator(
        task_id="dbt_run",
        bash_command=f"""
            dbt run \
                --project-dir {airflowSettings.dbt_project_dir} \
                --profiles-dir {airflowSettings.dbt_project_dir} \
                --profile {airflowSettings.dbt_profile_name} \
                --select mart_overall
        """,
    )

    subdag_operators >> update_central_mart