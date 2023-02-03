#TODO define the NodeHandller as the first processor, receive new transactions or any data, then call Graph_insertor
from logic.processor.processor import Processor

class GraphInsertor(Processor):
    
    def __init__(self, mongo_helper, neo4j_helper):
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper
    
    #What if the node is a user? it does not have 'detail' => I think all nodes should have the detail field
    def graph_insertor(self, tx):
        self.data[tx]['nodes']
        self.data[tx]['edges']
        for node in self.data[tx]['nodes']:
            self.neo4j_helper.insert_node(node) if not self.neo4j_helper.find_one_node(node['type'], node['address']) else \
                self.neo4j_helper.update_node(node['type'], node['address'], node['detail'])
        for edge in self.data[tx]['edges']:
            self.neo4j_helper.insert_relationship(edge['src'], edge['label'], edge['dest']) if \
                not self.neo4j_helper.find_one_relationship(edge['src'], edge['label'], edge['dest']) else \
                    self.neo4j_helper.update_relationship(edge['src'], None, edge['label'], edge['dest'])