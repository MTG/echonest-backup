\set ON_ERROR_STOP 1

-- Create the user and the database. Must run as user postgres.

CREATE USER echonest NOCREATEDB NOCREATEUSER;
CREATE DATABASE echonest WITH OWNER = echonest TEMPLATE template0 ENCODING = 'UNICODE';
