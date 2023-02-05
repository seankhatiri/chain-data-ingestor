
from logic.adaptor.etherscan_adaptor import EtherscanAdaptor
from logic.processor.processor import Processor

class EdgeProcessor(Processor):

    def __init__(self, mongo_helper, neo4j_helper):
        super().__init__(mongo_helper, neo4j_helper)
        self.etherscan_helper = EtherscanAdaptor()
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper

    def _iterate(self, tx):
        self.data[tx]['edges'] = []
        self.edges = self.data[tx]['edges']
        self._handel_builtin_transfer_txs(tx)
        for event in self.data[tx]['events']:
            # TODO: we have some txs that just have a 'fee' on event without any dest (~30k), process them
            if 'destination' in event and 'meta' in event and 'contract' in event['meta']:
                contract_address = event['meta']['contract']
                # TODO: we should add different labels based on some other processors here, like payTip
                self.edges.append(self._get_edges_kwargs(event['source'], 'hasInteraction', event['destination']))

    def _handel_builtin_transfer_txs(self, tx):
        for event in self.data[tx]['events']:
            if 'meta' not in event and 'destination' in event:
                self.edges.append(self._get_edges_kwargs(event['source'], 'etherTransfer', event['destination']))

    def _get_edges_kwargs(self, src, label, dest):
        return {
                    'src': src,
                    'label': label,
                    'dest': dest
            }
            