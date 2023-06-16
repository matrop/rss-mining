## XMLParser:
- Make this an abstract class and implement single parsers for different sources (Zeit, FAZ, etc.). Factory pattern
- Add Unit Tests

## Database:
- Create dbt database user
- Move tables into own database, do not use Airflow database

- Create UUID for incoming rows via UUID postgres extension
- Create an integration table and append newly arrived raw data to it -> dbt

## Source: SZ

- Fetch categories into own table to map 1:n (article - categories) relationship

## Source: Zeit

- Fetch authors into own table to map n:m relationship