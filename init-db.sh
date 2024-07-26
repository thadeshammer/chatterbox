#!/bin/bash
set -e

# Function to create a user and grant privileges
create_user_and_db() {
  local db_name=$1
  local user_file=$2
  local password_file=$3
  local superuser=$4
  local superuser_pw_file=$5

  psql -v ON_ERROR_STOP=1 --username "$superuser" --dbname "$db_name" <<-EOSQL
    CREATE USER $(cat $user_file) WITH PASSWORD '$(cat $password_file)';
    GRANT ALL PRIVILEGES ON DATABASE $db_name TO $(cat $user_file);
EOSQL
}

# Main database
create_user_and_db "$POSTGRES_DB" /run/secrets/postgres_user /run/secrets/postgres_password "$POSTGRES_SUPERUSER" /run/secrets/postgres_superuser_password

# Test database
create_user_and_db "$POSTGRES_DB" /run/secrets/test_postgres_user /run/secrets/test_postgres_password "$POSTGRES_SUPERUSER" /run/secrets/test_postgres_superuser_password
