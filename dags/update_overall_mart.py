from airflow.decorators import dag
from airflow.operators.bash import BashOperator

import datetime

from Settings import airflowSettings

@dag(
    dag_id="update-overall-mart",
    schedule_interval=None,
    start_date=datetime.datetime(2021, 1, 1),
    catchup=False,
)
def update_overall_mart():
    BashOperator(
        task_id="dbt_run",
        bash_command=f"""
            dbt run \
                --project-dir {airflowSettings.dbt_project_dir} \
                --profiles-dir {airflowSettings.dbt_project_dir} \
                --profile {airflowSettings.dbt_profile_name} \
                --select mart_overall
        """,
    )


update_dag = update_overall_mart()
