DROP TABLE IF EXISTS student;
CREATE TABLE student (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, first_name VARCHAR (32), last_name VARCHAR(32));
INSERT INTO student (first_name, last_name) VALUES ('misha', 'kurashev')