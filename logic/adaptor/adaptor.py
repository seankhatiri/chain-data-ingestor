from typing import Any, Tuple, List
class Adaptor:
    
    def fetch_contracts(self):
        raise NotImplementedError()

    def fetch_transactions(self):
        raise NotImplementedError()
    
    def get_fetched_transactions(self):
        raise NotImplementedError()
