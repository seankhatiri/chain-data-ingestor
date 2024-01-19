#!/bin/bash

set -o allexport
source .env
set +o allexport

DESIRED_PORT=5432
export PGPASSWORD=$DB_PASS

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
    echo "Creating database for $DB_NAME..."
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -tAc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || psql -c "CREATE DATABASE $DB_NAME;"

    echo "Creating the $DB_USER user..."
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -tAc "SELECT 1 FROM pg_roles WHERE rolname = '$DB_USER'" | grep -q 1 || psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"

    echo "Granting privileges to the $DB_USER user..."
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

    echo "PostgreSQL setup and user database creation complete."
}

migration() {
    echo "Running migration..."
    psql -h $DB_HOST -U $DB_USER -d $DB_NAME -a -f sql/create_tables.sql
}

run_flask_app() {
    echo "Running Flask app..."
    if [[ "$DOCKER_ENV" != "1" ]]; then
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
    fi
    python main.py
}

if [[ "$DOCKER_ENV" != "1" ]]; then
    DB_HOST=localhost
    if is_postgres_installed; then
        echo "PostgreSQL is already installed."
    else
        install_postgres
    fi

    start_postgres_on_port $DESIRED_PORT
else
    echo "Using Docker env ..."
    DB_HOST=db
fi

create_user_database
migration

run_flask_app