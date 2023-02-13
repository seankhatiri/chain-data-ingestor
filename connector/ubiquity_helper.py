import requests
from utility.logger import Logger

class UbiquityHelper:
    url: str
    apikey: str

    def __init__(self, url, apikey):
        self.url = url
        self.apikey = apikey
        self.HEADERS = {
                'Authorization': f'Bearer {apikey}'
            }

    def search(self, endpoint= None):
        def _search():
            try:
                response = requests.get(self.url + endpoint, headers=self.HEADERS)
                if response.json()['status'] == 1:
                    result = response.json()['data']
                    return result
            except Exception as e:
                Logger().error(str(e), additional_data=None)
        
        return _search()
