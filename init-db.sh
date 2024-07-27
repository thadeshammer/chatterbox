#!/bin/bash
set -e

POSTGRES_DB=chatterboxdb
POSTGRES_USER=$(cat /run/secrets/postgres_user.txt)
POSTGRES_PASSWORD=$(cat /run/secrets/postgres_password.txt)

psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
EOSQL

echo "User and database created successfully"
