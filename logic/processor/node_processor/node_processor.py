
from logic.processor.processor import Processor
from logic.adaptor.etherscan_adaptor import EtherscanAdaptor

class NodeProcessor(Processor):

    def __init__(self, mongo_helper, neo4j_helper):
        super.__init__(mongo_helper, neo4j_helper)
        self.etherscan_adaptor = EtherscanAdaptor()
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper

    def _iterate(self, tx):
        self.data[tx]['nodes'] = []
        for event in tx['events']:
            if 'meta' in event and 'contract' in event['meta']:
                self._insert_node('CONTRACT', tx, event['meta']['contract'])
        for event in tx['events']:
            if not self.etherscan_adaptor.is_contract(event['source']):
                self._insert_node('USER', tx, event['source'])
            else:
                self._insert_node('CONTRACT', tx, event['source'])
            if 'destination' in event:
                if not self.etherscan_adaptor.is_contract(event['destination']):
                    self._insert_node('USER', tx, event['destination'])
                else:
                    self._insert_node('CONTRACT', tx, event['destination'])
    
    def _insert_node(self, type, tx, address):
        if type == 'CONTRACT':
            contract = self.etherscan_adaptor.fetch_contract(address)['source_code']
            detail = {
                'SourceCode': contract['SourceCode'] ,
                'ContractName': contract['ContractName']
            } if type == 'CONTRACT' else {}
            self.data[tx]['nodes'] = self.data[tx]['nodes'].append({'type': type, 'address': address, \
                    'detail': { 
                        'SourceCode': contract['SourceCode'] ,
                        'ContractName': contract['ContractName']
                     }})
        if type == 'USER':
            self.data[tx]['nodes'] = tx['nodes'].append({'type': type, 'address': address})

# 0xad9f9d1f2ea57643fdc9c89d89b8b275ea85413b2d7cfad76c9ff3aafeabb397