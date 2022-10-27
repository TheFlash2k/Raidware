DROP TABLE IF EXISTS "teamserver"."user";

CREATE TABLE users (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);