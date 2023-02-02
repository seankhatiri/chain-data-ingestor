from utility.logger import Logger
from configuration.configs import Configs
import requests

class ChainscanHelper:
    debug: bool
    url: str
    address: str
    apikey: str
   
   #TODO expand the functionality to have one helper for any 'chain'_scan provider
    def __init__(self, url, apikey, debug = False):
        self.debug = debug
        self.apikey = apikey
        self.url = url

    def search(self, search_filter=None):
        def _search():
            result = []
            try:
                payload = {
                    "module": search_filter['module'],
                    "action": search_filter['action'],
                    "address": search_filter['address'],
                    "apikey": self.apikey
                }
                response = requests.get(self.url, params=payload)
                if response.json()['status'] == 1:
                    result = response.json()['result']
                    return result
            except Exception as e:
                #TODO specify which adaptor triger this error, like etherscan adaptor
                Logger().error(str(e), additional_data = None)
            return result

        return _search()
    
