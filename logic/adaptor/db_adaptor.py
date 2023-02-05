from connector.mongo_helper import MongoHelper
from configuration.configs import Configs
from connector.neo4j_helper import Neo4jHelper
from logic.adaptor.adaptor import Adaptor

class DBAdaptor(Adaptor):
    mongo_helper: MongoHelper
    neo4j_helper: Neo4jHelper
    
    def __init__(self, mongo_heler: MongoHelper, neo4j_helper: Neo4jHelper, txs_ids=None):
        self.mongo_helper = mongo_heler
        self.neo4j_helper = neo4j_helper
        self.txs_ids = txs_ids

    def fetch_transactions(self):
        if self.txs_ids:
            for tx_id in self.txs_ids:
                result = []
                result.append(self.mongo_helper.find_one('transactions', {'id': tx_id}))
            return result
        else:   
            return self.mongo_helper.get_all('transactions', limit=2000)

    def fetch_contracts(self):
        return self.mongo_helper.get_all('contracts')