from connector.mongo_helper import MongoHelper
from configuration.configs import Configs
from connector.neo4j_helper import Neo4jHelper
from logic.adaptor.adaptor import Adaptor

class DBAdaptor(Adaptor):
    mongo_helper: MongoHelper
    
    def __init__(self, mongo_heler: MongoHelper, neo4j_helper: Neo4jHelper):
        self.mongo_helper = mongo_heler
        self.neo4j_helper = neo4j_helper

    def fetch_transactions(self):
        return self.mongo_helper.get_all('transactions')

    def fetch_contracts(self):
        return self.mongo_helper.get_all('contracts')