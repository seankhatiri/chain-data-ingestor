# On-chain Data Ingestor 

## Quick Setup

If you have Docker installed on your machine you can simply run the following commands to first create docker containers and then run both db and app on port 5001:

    docker-compose build --no-cache
    docker-compose up

if you want to take the container down:

    docker-compose down

Note: the app will be running on localhost:PORT on your local.

Additioanlly, if you want to run the application directly from init.sh script and setup Postgress locally, you can continue to following sections.

## Dependencies

The init.sh script creates a virtual environment and installs the required dependencies.

## Setup 

The project's entry point is the init.sh file, runnable on macOS with:

    source init.sh


This script first checks for PostgreSQL installation and brings up the database if not present. It creates a database and a database user, then sets up necessary tables using sql/create_tables.sql. Lastly, it runs the Flask application.

Note [TEMP]: when using docker-compose it cannot read the env from compose yml file, so for now if wanna runnning on local use MODE=local and POSTGRES_DB_HOST=localhost, on local_docker use MODEL=local_docker and POSTGRES_DB_HOST=localhost
