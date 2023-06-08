DROP TABLE IF EXISTS raw.sz;

CREATE TABLE raw.sz (
    guid VARCHAR PRIMARY KEY,
    title VARCHAR NULL,
    link VARCHAR NULL,
    description VARCHAR NULL,
    timestamp VARCHAR NULL
);