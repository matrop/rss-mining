## Installation instructions

### Airfow

## Usage

1. Enter poetry shell

```bash
poetry shell
```

2. Start the docker containers

```bash
./up.sh
```

Most importantly, docker-compose spins up a Postgres instance at `localhost:5432` and a Airflow Web UI at `localhost:8080`.

3. Open the Airflow Web UI and log in using the default credentials (User: airflow, Password: airflow)
4. Run the `init_db` DAG 