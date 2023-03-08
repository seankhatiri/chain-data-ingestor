
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
                #Note_Patrck: add the main_func field to each event that has a meta, meaning the interacted func_code + payload, meaning the argument to the interacted func
                func, internal_funcs = self._func_code_handler(event['func_code'], event['func_name'], event['func_input'], event['meta']['contract'])
                self.edges.append(self._get_edges_kwargs(event['source'], 'hasInteraction', event['destination'], func, internal_funcs))

    def _handel_builtin_transfer_txs(self, tx):
        for event in self.data[tx]['events']:
            if 'meta' not in event and 'destination' in event:
                self.edges.append(self._get_edges_kwargs(event['source'], 'etherTransfer', event['destination']))

    def _func_code_handler(self, func_code, func_name, payload, contract_address):
        # TODO: get the internal funcs code, names and attributes from AST util
        internal_funcs = []
        func = {
            'name': func_name,
            'code' : func_code,
            'args': payload
        }
        return func, internal_funcs

    def _get_edges_kwargs(self, src, label, dest, func=None, internal_funcs=None):
        return {
                    'src': src,
                    'label': label,
                    'dest': dest, 
                    'interaction': {
                        'func': func,
                        'internal_funcs': internal_funcs
                    }, 
                    'interpretation': ''
            }