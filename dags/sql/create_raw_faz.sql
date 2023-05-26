DROP TABLE IF EXISTS raw.faz;

CREATE TABLE raw.faz (
    guid VARCHAR PRIMARY KEY,
    title VARCHAR NULL,
    link VARCHAR NULL,
    description VARCHAR NULL,
    timestamp VARCHAR NULL
);