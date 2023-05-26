## XMLParser:
- Make this an abstract class and implement single parsers for different sources (Zeit, FAZ, etc.). Factory pattern

## New Source: FAZ
- Try to fetch the FAZ RSS feed

## Database:
- Create dbt database user
- Move tables into own database, do not use Airflow database

- Create UUID for incoming rows via UUID postgres extension
- Create an integration table and append newly arrived raw data to it -> dbt
