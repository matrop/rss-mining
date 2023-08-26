from Settings import IngestionSettings, AirflowSettings
from airflow.decorators import task


def rss_ingestion_taskflow(
    ingestionSettings: IngestionSettings, airflowSettings: AirflowSettings
):
    from airflow.providers.postgres.operators.postgres import PostgresOperator
    from airflow.operators.bash import BashOperator

    truncate_landing_table = PostgresOperator(
        task_id="truncate_landing_table",
        postgres_conn_id="postgres_default",
        sql=f"TRUNCATE {ingestionSettings.raw_table_name}",
    )

    @task(task_id="get_rss_feed")
    def get_rss_feed():
        from RSSGetter import RSSGetter

        rss_getter = RSSGetter(ingestionSettings, airflowSettings)
        rss_getter.save_to_file()
        return rss_getter.output_filename

    @task(task_id="parse_rss_feed")
    def parse_rss_feed(rss_filename):
        xml_parser = ingestionSettings.parser_class(
            rss_filename, ingestionSettings, airflowSettings
        )
        xml_parser.save_to_csv()
        return xml_parser.output_filename

    @task(task_id="load_csv")
    def load_csv(parsed_rss_filename: str):
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        hook = PostgresHook(postgres_conn_id="postgres_default")
        hook.bulk_load(ingestionSettings.raw_table_name, parsed_rss_filename)

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"""
            dbt run \
                --project-dir {airflowSettings.dbt_project_dir} \
                --profiles-dir {airflowSettings.dbt_project_dir} \
                --profile {airflowSettings.dbt_profile_name} \
                --select +{ingestionSettings.mart_table_name}
        """,
    )

    rss_filename = get_rss_feed()
    parsed_rss_filename = parse_rss_feed(rss_filename)

    (
        parsed_rss_filename
        >> truncate_landing_table
        >> load_csv(parsed_rss_filename)
        >> dbt_run
    )
