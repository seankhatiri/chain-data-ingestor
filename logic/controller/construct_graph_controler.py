from utility.singleton import Singleton
from configuration.configs import Configs
from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper

class ConstructGraphControler(metaclass=Singleton):
    debug: bool
    mongo_helper: MongoHelper
    neo4j_helper: Neo4jHelper

    def __init__(self):
        self.debug = False
        self.transactions = None
        self.mongo_helper = MongoHelper(Configs.mongo_url, debug=self.debug)
        self.neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)

    
    def run_pipeline_local(self):
        #TODO implement pipeline and processors, then run mainpipeline from here
        pass
    
    def graph_insertor(self):
        #TODO some destination/source addresses are contracts handle them
        self.transactions = self.mongo_helper.get_all('transactions', limit=1000)
        self.node_handler()
        self.edge_handler()
                
    def node_handler(self):
        # self.insert_contracts()
        self.insert_users()
    
    def insert_contracts(self):
        contracts = self.mongo_helper.get_all('contracts')
        for contract in contracts:
            contract_node = {'type': 'CONTRACT', 'address': str(contract['contractAddress']), 'detail': { 'source_code': str(contract['SourceCode'])}}
            self.neo4j_helper.insert_node(contract_node) 
        
    def insert_users(self):
        for transaction in self.transactions:
            for event in transaction['events']:
                user_node = {'type': 'USER', 'address': event['source']}
                if not self.mongo_helper.is_contract(event['source']):
                    self.neo4j_helper.insert_node(user_node)
                if 'destination' in event and not self.mongo_helper.is_contract(event['destination']):
                    user_node = {'type': 'USER', 'address': event['destination']}
                    self.neo4j_helper.insert_node(user_node)
        
    def edge_handler(self):
        for transaction in self.transactions:
            for event in transaction['events']:
                if 'destination' in event and 'meta' in event and 'contract' in event['meta']:
                    contract_address = event['meta']['contract']
                    # question: when we have a src, dest and contract what is the direction of interactions? 
                    contract_node = self.neo4j_helper.find_one_node('CONTRACT', contract_address)
                    dest = self.neo4j_helper.find_one_node('USER', event['destination']) if self.neo4j_helper.is_user(event['destination']) else \
                        self.neo4j_helper.find_one_node('CONTRACT', event['destination'])
                    src = self.neo4j_helper.find_one_node('USER', event['source']) if self.neo4j_helper.is_user(event['source']) else \
                        self.neo4j_helper.find_one_node('CONTRACT', event['source'])
                    if src and contract_node: self.neo4j_helper.insert_relationship(src, 'hasTransaction', contract_node)
                    if dest and contract_node: self.neo4j_helper.insert_relationship(contract_node, 'hasTransaction', dest)