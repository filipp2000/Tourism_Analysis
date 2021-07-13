CREATE DATABASE eurostat_db;
USE eurostat_db;

CREATE TABLE IF NOT EXISTS nights_total(
	country SET('EL', 'ES') NOT NULL,
	year YEAR,
    value INT
);

CREATE TABLE IF NOT EXISTS nights_nonresidents(
	country SET('EL', 'ES') NOT NULL,
	year YEAR,
    value INT
);

CREATE TABLE IF NOT EXISTS arrivals_total(
	country SET('EL', 'ES') NOT NULL,
	year YEAR,
    value INT
);

CREATE TABLE IF NOT EXISTS arrivals_nonresidents(
	country SET('EL', 'ES') NOT NULL,
	year YEAR,
    value INT
);

select * from nights_total;
select * from nights_nonresidents;
select * from arrivals_total;
select * from arrivals_nonresidents;
