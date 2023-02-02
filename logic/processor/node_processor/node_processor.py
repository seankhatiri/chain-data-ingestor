
from logic.processor.processor import Processor
from logic.adaptor.etherscan_adaptor import EtherscanAdaptor

class NodeProcessor(Processor):

    def __init__(self, mongo_helper, neo4j_helper):
        super.__init__(mongo_helper, neo4j_helper)
        self.etherscan_helper = EtherscanAdaptor()
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper

    def _iterate(self, tx):
        self.data[tx]['nodes'] = []
        for event in tx['events']:
            #TODO when fetch n tx we don't insert new contracts so the mongo_helper.is_Conract always return False
            if not self.mongo_helper.is_contract(event['source']):
                self.data[tx]['nodes'] = self.data[tx]['nodes'].append({'type': 'USER', 'address': event['source']})
            else:
                self.data[tx]['nodes'] = self.data[tx]['nodes'].append({'type': 'CONTRACT', 'address': event['source'], \
                    'detail': { 'source_code': self.etherscan_helper.fetch_contract(event['source'])['source_code']}})
            if 'destination' in event:
                if not self.mongo_helper.is_contract(event['destination']):
                    self.data[tx]['nodes'] = tx['nodes'].append({'type': 'USER', 'address': event['destination']})
                else:
                    self.data[tx]['nodes'] = tx['nodes'].append({'type': 'CONTRACT', 'address': event['destination'], \
                    'detail': { 'source_code': self.etherscan_helper.fetch_contract(event['destination'])['source_code']}})
    