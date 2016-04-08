PG_USER=postgres

psql -U $PG_USER -f sql/create_db.sql
psql -U $PG_USER -d echonest -f sql/create_extensions.sql
psql -U echonest -f sql/create_tables.sql
psql -U echonest -f sql/create_primary_keys.sql
psql -U echonest -f sql/create_foreign_keys.sql
psql -U echonest -f sql/create_indexes.sql
