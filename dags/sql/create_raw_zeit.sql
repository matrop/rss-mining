DROP TABLE IF EXISTS raw.zeit;

CREATE TABLE raw.zeit (
    guid VARCHAR PRIMARY KEY,
    title VARCHAR NULL,
    link VARCHAR NULL,
    description VARCHAR NULL,
    category VARCHAR NULL,
    creators VARCHAR NULL,
    timestamp VARCHAR NULL
);