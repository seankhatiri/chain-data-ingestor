from connector.mongo_helper import MongoHelper
from configuration.configs import Configs
from logic.adaptor.adaptor import Adaptor

class DBAdaptor(Adaptor):
    mongo_helper: MongoHelper
    
    def __init__(self):
        self.mongo_helper = MongoHelper(Configs.mongo_url)

    def fetch_contracts(self):
        return super().fetch_contracts()

    def fetch_transactions(self):
        return super().fetch_transactions()