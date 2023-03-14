
from connector.mongo_helper import MongoHelper
from connector.cmc_helper import CMCHelper
from logic.adaptor.adaptor import Adaptor
from configuration.configs import Configs


class CMCAdaptor(Adaptor):
    cmc_helper: CMCHelper
    mongo_helper: MongoHelper

    def __init__(self):
        self.cmc_helper = CMCHelper(Configs.coinmarketcap_url, Configs.coinmarketcap_apikey)
        self.mongo_helper = MongoHelper(Configs.mongo_url)

    def fetch_token_info(self, token_name: str = None, token_contract_address: str = None):
        if self.mongo_helper.exists('tokens', {'name': token_name}): 
            token = self.mongo_helper.find_one('tokens', {'name': token_name})
            if 'detail' in token.keys():
                return self.mongo_helper.find_one('tokens', {'name': token_name})
        endpoint = f"/v2/cryptocurrency/info?address={token_contract_address}" if token_contract_address else f"/v2/cryptocurrency/info?slug={token_name}"
        result = self.cmc_helper.search(endpoint)
        if result:
            result = list(result.values())
            return result[0]
        else:
            return None

    def fetch_tokens_map(self):
        endpoint = f"/v1/cryptocurrency/map"
        return self.cmc_helper.search(endpoint)