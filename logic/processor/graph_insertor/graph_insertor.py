#TODO define the NodeHandller as the first processor, receive new transactions or any data, then call Graph_insertor
from logic.processor.processor import Processor

class GraphInsertor(Processor):
    
    def __init__(self, mongo_helper, neo4j_helper):
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper
    
    def graph_insertor(self, tx):
        self.data[tx]['nodes']
        self.data[tx]['edges']
        for node in self.data[tx]['nodes']:
            self.neo4j_helper.insert_node(node)
        for edge in self.data[tx]['edges']:
            self.neo4j_helper.insert_relationship(edge)