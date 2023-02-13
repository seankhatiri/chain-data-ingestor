#TODO add axelar scan adaptor to have crosschain transactions
from logic.adaptor.adaptor import Adaptor
class AxelarscanAdaptor(Adaptor):
    def fetch_contracts(self):
        return super().fetch_contracts()
    
    def fetch_transactions(self):
        return super().fetch_transactions()