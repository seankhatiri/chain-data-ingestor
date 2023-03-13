import requests
from utility.logger import Logger

class CMCHelper:
    url: str
    apikey: str

    def __init__(self, url, apikey):
        self.url = url
        self.HEADERS = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": apikey
        }

    def search(self, endpoint= None):
        def _search():
            try:
                response = requests.get(self.url + endpoint, headers=self.HEADERS)
                if response.json()['status']['error_code'] == 0:
                    result = response.json()['data']
                    return result
            except Exception as e:
                Logger().error(str(e), additional_data=None)
        return _search()