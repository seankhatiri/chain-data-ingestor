#!/bin/bash

set -o allexport
source .env
set +o allexport

DESIRED_PORT=5432
export PGPASSWORD=$POSTGRES_DB_PASS

is_postgres_installed() {
    arch -arm64 brew ls --versions postgresql > /dev/null
    return $?
}

install_postgres() {
    echo "Installing PostgreSQL..."
    arch -arm64 brew install postgresql
}

start_postgres_on_port() {
    local port=$1
    echo "Starting PostgreSQL on port $port..."
    sed -i '' "s/#port = 5432/port = $port/" /opt/homebrew/var/postgresql@14/postgresql.conf
    arch -arm64 brew services start postgresql@14
}

create_user_database() {
    echo "Creating database for $POSTGRES_DB_NAME..."
    psql -h $POSTGRES_DB_HOST -U $POSTGRES_DB_USER -d $POSTGRES_DB_NAME -tAc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB_NAME'" | grep -q 1 || psql -c "CREATE DATABASE $POSTGRES_DB_NAME;"

    echo "Creating the $POSTGRES_DB_USER user..."
    psql -h $POSTGRES_DB_HOST -U $POSTGRES_DB_USER -d $POSTGRES_DB_NAME -tAc "SELECT 1 FROM pg_roles WHERE rolname = '$POSTGRES_DB_USER'" | grep -q 1 || psql -c "CREATE USER $POSTGRES_DB_USER WITH PASSWORD '$POSTGRES_DB_PASS';"

    echo "Granting privileges to the $POSTGRES_DB_USER user..."
    psql -h $POSTGRES_DB_HOST -U $POSTGRES_DB_USER -d $POSTGRES_DB_NAME -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB_NAME TO $POSTGRES_DB_USER;"

    echo "PostgreSQL setup and user database creation complete."
}

migration() {
    echo "Running migration..."
    psql -h $POSTGRES_DB_HOST -U $POSTGRES_DB_USER -d $POSTGRES_DB_NAME -a -f sql/create_schemas.sql
    psql -h $POSTGRES_DB_HOST -U $POSTGRES_DB_USER -d $POSTGRES_DB_NAME -a -f sql/create_tables.sql
}

run_flask_app() {
    echo "Running Flask app..."
    if [[ "$MODE" == "local" ]]; then
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    fi
    python main.py
}

if [[ "$MODE" == "local" ]]; then
    if is_postgres_installed; then
        echo "PostgreSQL is already installed."
    else
        install_postgres
    fi

    start_postgres_on_port $DESIRED_PORT
fi


create_user_database
migration

run_flask_app