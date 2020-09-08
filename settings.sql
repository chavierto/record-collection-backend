-- settings.sql
CREATE DATABASE record_collection_be;
CREATE USER rc_user WITH PASSWORD 'records';
GRANT ALL PRIVILEGES ON DATABASE record_collection_be TO rc_user;