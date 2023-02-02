from connector.mongo_helper import MongoHelper
from logic.adaptor.adaptor import Adaptor
from connector.chainscan_helper import ChainscanHelper
from configuration.configs import Configs

class EtherscanAdaptor(Adaptor):
    etherscan_helper: ChainscanHelper
    mongo_helper: MongoHelper

    def __init__(self):
        self.etherscan_helper = ChainscanHelper(Configs.etherscan_url, Configs.etherscan_apikey)
        self.mongo_helper = MongoHelper(Configs.mongo_url)

    def fetch_contract(self, address: str= None):
        if self.mongo_helper.exists('contracts', {'contractAddress': address}): 
            return self.mongo_helper.find_one('contracts', {'contractAddress': address})
        search_filters = {
            'module': 'contract',
            'action': 'getsourcecode',
            'address': address
        }
        result = self.etherscan_helper.search(search_filters)
        self._cache_contract(result)
        return result

    #TODO let's find is that possible to fetch batch of ethereum transactions from etherscan
    def fetch_transactions(self):
        return super().fetch_transactions()

    def fetch_contracts(self):
        return super().fetch_contracts()

    def _cache_contract(self, data):
        contract = {
            'contractAddress': data['contractAddress'],
            'sourceCode': data['sourceCode'],
            'ABI': data['ABI'],
            'ContractName': data['ContractName'],
            'Proxy': data['Proxy']
        }
        self.mongo_helper.insert_one(contract, 'contracts')