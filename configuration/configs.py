import os 
from decouple import config
from utility.singleton import Singleton


class Configs(Singleton):

    mode: str = config('MODE')
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                              os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    log_level : int = config('LOG_LEVEL', 3)
    port: int = config('PORT', default=80, cast=int)
    SECRET_KEY = config('SECRET_KEY', default='a;lsdkfh;lakshdhflkajsdf')
    mongo_url: str = config('MONGO_URL', default='')
    mongo_url_cloud: str = config('MONGO_URL_CLOUD', default='')
    neo4j_url: str = config('NEO4J_URL', default='')
    neo4j_user: str = config('NEO4J_USERNAME')
    neo4j_pass: str = config('NEO4J_PASSWORD')
    etherscan_apikey: str = config('ETHERSCAN_APIKEY')
    etherscan_url: str = config('ETHERSCAN_URL')
    ubiquity_apikey: str = config('UBIQUITY_APIKEY')
    ubiquity_url: str = config('UBIQUITY_URL')
    coinmarketcap_apikey: str = config('COINMARKETCAP_API_KEY')
    coinmarketcap_url:str = config('COINMARKETCAP_URL')

    is_docker: bool = config('IS_DOCKER', default=False)
    postgres_db_name: str = config('POSTGRES_DB_NAME')
    postgres_db_user: str = config('POSTGRES_DB_USER')
    postgres_db_pass: str = config('POSTGRES_DB_PASS')

    postgres_config = {
        "host": "db" if is_docker else "localhost",
        "database": postgres_db_name,
        "user": postgres_db_user,
        "password": postgres_db_pass,
    }

    node_provider_url: str = config('NODE_PROVIDER_URL')
    poll_interval: int = config('POLL_INTERVAL', default=10) # second