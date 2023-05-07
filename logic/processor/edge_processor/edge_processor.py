
from logic.adaptor.etherscan_adaptor import EtherscanAdaptor
from logic.processor.processor import Processor

class EdgeProcessor(Processor):

    def __init__(self, mongo_helper, neo4j_helper):
        super().__init__(mongo_helper, neo4j_helper)
        self.etherscan_helper = EtherscanAdaptor()
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper

    def _iterate(self, tx_id):
        self.data[tx_id]['edges'] = []
        self.edges = self.data[tx_id]['edges']
        self.nodes = self.data[tx_id]['nodes']
        tx_hash =self.data[tx_id]['id']
        self._handel_main_tx(tx_id, tx_hash)
        for event in self.data[tx_id]['events']:
            if 'destination' in event:
                if event['source'].lower() == self.data[tx_id]['from'] and event['destination'].lower() == self.data[tx_id]['to']: continue
            if 'destination' in event and 'meta' in event and 'contract' in event['meta']:
                #TODO: we are missing two same edges (tokenTransfer) between two nodes (e31, 06)
                if event['meta']['contract'] != event['source'] and event['meta']['contract'] != event['destination']:
                    self.edges.append(self._get_edges_kwargs(tx_hash, event['source'], 'tokenTransfer', event['meta']['contract']))
                    self.edges.append(self._get_edges_kwargs(tx_hash, event['meta']['contract'], 'tokenTransfer', event['destination']))
                else:
                    self.edges.append(self._get_edges_kwargs(tx_hash, event['source'], 'tokenTransfer', event['destination'])) 
            if 'destination' in event and 'meta' not in event:
                self.edges.append(self._get_edges_kwargs(tx_hash, event['source'], 'tokenTransfer', event['destination'])) 

    def _handel_main_tx(self, tx_id, tx_hash):
        tx = self.data[tx_id]
        detail = self._edge_detail_handler(tx['func_name'], tx['func_signature'], tx['func_args'])
        self.edges.append(self._get_edges_kwargs(tx_hash, tx['from'], tx['func_name'], tx['to'], detail))

    def _edge_detail_handler(self, func_name, func_signature, func_args):
        detail = {
            'function_name': func_name,
            'function_signature' : func_signature,
            'function_args': func_args
        }
        return detail

    def _get_edges_kwargs(self, tx_hash, src, label, dest, detail=None):
        #TODO: handel custom edge labels where we don't have func_name in tx
        if label == '': label = 'hadInteraction'
        return {
                    'src': src.lower(),
                    'label': label,
                    'dest': dest.lower(),
                    'tx_id': tx_hash,
                    'interaction': detail, 
                    'interpretation': ''
            }

    # ******************** CREATE SAMEAS EDGE BETWEEN SAME CONTRACTS ********************
    # def _handel_same_contracts(self, tx_id, tx_hash):
    #     nodes = []
    #     for node in self.nodes:
    #         if self.etherscan_helper.is_contract(node['address']):
    #             nodes.append(node)
    #     for first_node in nodes:
    #         for second_node in nodes:
    #             #TODO: prevent adding two 'sameAs' relationships here
    #             if first_node['detail']['ContractName'] == second_node['detail']['ContractName'] and first_node['detail']['SourceCode'] == second_node['detail']['SourceCode'] and first_node['address'] != second_node['address']:
    #                 self.data[tx_id]['edges'].append(self._get_edges_kwargs(tx_hash, first_node['address'], 'sameAs', second_node['address']))
    #                 print('same contract has been found ...')
