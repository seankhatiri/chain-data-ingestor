import os 
from decouple import config
from utility.singleton import Singleton


class Configs(Singleton):

    mode: str = config('MODE')
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
                              os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    log_level : int = config('LOG_LEVEL')
    port: int = config('PORT', default=80, cast=int)
    SECRET_KEY = config('SECRET_KEY', default='a;lsdkfh;lakshdhflkajsdf')
    mongo_url: str = config('MONGO_URL', default='')
    neo4j_url: str = config('NEO4J_URL', default='')
    neo4j_user: str = config('NEO4J_USERNAME')
    neo4j_pass: str = config('NEO4J_PASSWORD')
    etherscan_apikey: str = config('ETHERSCAN_APIKEY')
    etherscan_url: str = config('ETHERSCAN_URL')
    ubiquity_apikey: str = config('UBIQUITY_APIKEY')
    ubiquity_url: str = config('UBIQUITY_URL')
    coinmarketcap_apikey: str = config('COINMARKETCAP_API_KEY')
    coinmarketcap_url:str = config('COINMARKETCAP_URL')