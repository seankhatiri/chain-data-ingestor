
from logic.adaptor.etherscan_adaptor import EtherscanAdaptor
from logic.processor.processor import Processor

class EdgeProcessor(Processor):

    def __init__(self, mongo_helper, neo4j_helper):
        super().__init__(mongo_helper, neo4j_helper)
        self.etherscan_helper = EtherscanAdaptor()
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper

    def _iterate(self, tx):
        tx_id = tx
        self.data[tx]['edges'] = []
        self.edges = self.data[tx]['edges']
        self._handel_main_tx(tx)
        for event in self.data[tx]['events']:
            #TODO: handel situation that tx main from and to are in an event, skip that event
            if 'destination' in event and 'meta' in event and 'contract' in event['meta']:
                if event['meta']['contract'] != event['source'] and event['meta']['contract'] != event['destination']:
                    self.edges.append(self._get_edges_kwargs(tx_id, event['source'], 'tokenTransfer', event['meta']['contract']))
                    self.edges.append(self._get_edges_kwargs(tx_id, event['meta']['contract'], 'tokenTransfer', event['destination']))
                else:
                    self.edges.append(self._get_edges_kwargs(tx_id, event['source'], 'tokenTransfer', event['destination'])) 
            #events that just have 'destination' and don't have 'meta'
            if 'destination' in event and 'meta' not in event:
                self.edges.append(self._get_edges_kwargs(tx_id, event['source'], 'tokenTransfer', event['destination'])) 

    def _handel_main_tx(self, tx_id):
        tx = self.data[tx_id]
        detail = self._func_code_handler(tx['func_name'], tx['func_signature'], tx['func_args'])
        self.edges.append(self._get_edges_kwargs(tx_id, tx['from'], tx['func_signature'], tx['to'], detail))

    def _edge_detail_handler(self, func_name, func_signature, func_args):
        detail = {
            'function_name': func_name,
            'function_signature' : func_signature,
            'function_args': func_args
        }
        return detail

    def _get_edges_kwargs(self, tx, src, label, dest, detail=None):
        return {
                    'src': src,
                    'label': label,
                    'dest': dest,
                    'tx_id': tx,
                    'interaction': detail, 
                    'interpretation': ''
            }