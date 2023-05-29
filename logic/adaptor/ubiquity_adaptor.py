
from connector.mongo_helper import MongoHelper
from connector.ubiquity_helper import UbiquityHelper
from logic.adaptor.adaptor import Adaptor
from configuration.configs import Configs


class UbiquityAdaptor(Adaptor):
    ubiquity_helper: UbiquityHelper
    mongo_helper: MongoHelper

    def __init__(self):
        self.ubiquity_helper = UbiquityHelper(Configs.ubiquity_url, Configs.ubiquity_apikey)
        self.mongo_helper = MongoHelper(Configs.mongo_url)

    def fetch_transactions(self, protocol: str = 'ethereum', network: str = 'mainnet', page_size: int =100, page_token=None):
        endpoint = f"/{protocol}/{network}/txs?page_size={page_size}"
        result = self.mongo_helper.find_one('status')
        page_token = result['next_page_token']
        if page_token:
            endpoint += f"&page_token={page_token}"
        return self.ubiquity_helper.search(endpoint)

    def fetch_contracts(self):
        # TODO: implement the fetch_contract from ubiquity_helper
        return super().fetch_contracts()