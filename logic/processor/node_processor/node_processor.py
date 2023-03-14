
from logic.processor.processor import Processor
from logic.adaptor.etherscan_adaptor import EtherscanAdaptor
from logic.adaptor.cmc_adaptor import CMCAdaptor

class NodeProcessor(Processor):

    def __init__(self, mongo_helper, neo4j_helper):
        super().__init__(mongo_helper, neo4j_helper)
        self.etherscan_adaptor = EtherscanAdaptor()
        self.cmc_adaptor = CMCAdaptor()
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper

    def _iterate(self, tx):
        self.data[tx]['nodes'] = []
        self._preprocess_contracts(tx)
        self._handel_main_tx_nodes(tx)
        for event in self.data[tx]['events']:
            self._insert_node(tx, event['source'])
            if 'destination' in event:
                self._insert_node(tx, event['destination'])
    
    def _insert_node(self, tx, address):
        nodes = self.data[tx]['nodes']
        node_type = 'CONTRACT' if self.etherscan_adaptor.is_contract(address) else 'USER'
        if node_type == 'CONTRACT':
            contract = self.etherscan_adaptor.fetch_contract(address)
            #TODO: after enrichment, add tags, social_media_description based on token in detail
            detail = self._get_node_detail_kwargs(contract)
            nodes.append({'type': node_type, 'address': address.lower(), 'detail': detail})
        if node_type == 'USER':
            nodes.append({'type': node_type, 'address': address.lower(), 'detail': {}})

    def _preprocess_contracts(self, tx):
        for event in self.data[tx]['events']:
            if 'meta' in event and 'contract' in event['meta']:
                self._insert_node(tx, event['meta']['contract'])

    def _handel_main_tx_nodes(self, tx):
        self._insert_node(tx, self.data[tx]['from'])
        self._insert_node(tx, self.data[tx]['to'])

    def _extract_token_names(self, contract_name):
        return True if 'token' in contract_name.lower() else False
    
    def _get_token_context(self, token):
        token = token.replace('token', "")
        return self.cmc_adaptor.fetch_token_info(token_name=token)

    def _get_node_detail_kwargs(self, node):
        if self._extract_token_names(node['ContractName']):
            token['name'] = node['ContractName']
            token['description'] = self._get_token_context(node['ContractName'])
        else:
            token = 'NOT TOKEN CONTRACT'
        detail = {
            'ContractName': node['ContractName'],
            'SourceCode': node['SourceCode'],
            'Token': token
        }
        return detail

# interesting: 0xad9f9d1f2ea57643fdc9c89d89b8b275ea85413b2d7cfad76c9ff3aafeabb397