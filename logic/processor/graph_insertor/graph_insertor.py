#TODO define the NodeHandller as the first processor, receive new transactions or any data, then call Graph_insertor
from logic.processor.processor import Processor

class GraphInsertor(Processor):
    
    def __init__(self, mongo_helper, neo4j_helper):
        super().__init__(mongo_helper, neo4j_helper)
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper

    def _iterate(self, tx_id):
        nodes = self.data[tx_id]['nodes']
        edges = self.data[tx_id]['edges']
        # for node in self.data[tx_id]['nodes']:
        #     if node['type'] == 'USER': print(node['address'], node['detail'])
        for node in nodes:
            self.neo4j_helper.insert_node(node) if not self.neo4j_helper.find_one_node(node['type'], node['address']) else \
                self.neo4j_helper.update_node(node['type'], node['address'], node['detail'])
        for edge in edges:
            src = self.neo4j_helper.find_one_node(address=edge['src'])
            dest = self.neo4j_helper.find_one_node(address=edge['dest'])
            self.neo4j_helper.insert_relationship(src, edge['label'], dest) if \
                not self.neo4j_helper.find_one_relationship(src, edge['label'], dest) else \
                    self.neo4j_helper.update_relationship(src, None, edge['label'], dest)   