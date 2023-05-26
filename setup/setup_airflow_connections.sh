airflow connections delete postgres_zeit_mining

airflow connections add 'postgres_zeit_mining' \
    --conn-json '{
        "conn_type": "my-conn-type",
        "login": "my-login",
        "password": "my-password",
        "host": "my-host",
        "port": 1234,
        "schema": "my-schema",
        "extra": {
            "param1": "val1",
            "param2": "val2"
        }
    }'