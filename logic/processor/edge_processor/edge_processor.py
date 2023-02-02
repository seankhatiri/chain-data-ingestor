
from logic.adaptor.etherscan_adaptor import EtherscanAdaptor
from logic.processor.processor import Processor

class EdgeProcessor(Processor):

    def __init__(self, mongo_helper, neo4j_helper):
        super.__init__(mongo_helper, neo4j_helper)
        self.etherscan_helper = EtherscanAdaptor()
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper

    def _iterator(self, tx):
            self.data[tx]['edges'] = []
            for event in self.data[tx]['events']:
                #Question: do we have any tx that a user intracts directly with another user?
                if 'destination' in event and 'meta' in event and 'contract' in event['meta']:
                    contract_address = event['meta']['contract']
                    self.data[tx]['edges'] = self.data[tx]['edges'].append({
                        'src': event['source'],
                        # TODO: we should add different labels based on some other processors here, like payTip
                        'edge_label': 'hasInteraction',
                        'dest': event['destination']
                    })