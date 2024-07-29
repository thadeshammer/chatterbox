#!/bin/bash
set -e

DB=chatterboxdb
DBUSER=$(cat /run/secrets/datastore/postgres_user.txt)
DBPASSWORD=$(cat /run/secrets/datastore/postgres_password.txt)

# https://stackoverflow.com/a/75876944/19677371
psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE USER $DBUSER WITH PASSWORD '$DBPASSWORD';
    GRANT ALL PRIVILEGES ON DATABASE $DB TO $DBUSER;
    \c $DB postgres
    GRANT ALL ON SCHEMA public TO $DBUSER;
EOSQL

echo "User and database created successfully"
