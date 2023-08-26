from __future__ import annotations  # Cannot import XMLParser since it needs the Ingestnio Settings class

from typing import Type
from dataclasses import dataclass


@dataclass
class IngestionSettings:
    ingestion_source_name: str
    ingestion_dag_name: str
    rss_feed_url: str
    parser_class: Type[XMLParser]
    raw_table_name: str
    mart_table_name: str


@dataclass
class AirflowSettings:
    raw_data_dir: str
    transformed_data_dir: str
    base_dir: str
    dbt_project_dir: str
    dbt_profile_name: str


airflowSettings = AirflowSettings(
    raw_data_dir="/opt/airflow/python/data/raw",
    transformed_data_dir="/opt/airflow/python/data/transformed",
    base_dir="/opt/airflow/python/data",
    dbt_project_dir="/opt/airflow/dbt_transformations",
    dbt_profile_name="dbt_transformations_airflow",
)
