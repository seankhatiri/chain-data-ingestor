from web3 import Web3
from utility.logger import Logger
import time

class NodeProviderHelper:

    def __init__(self, node_provider_url, debug: bool = False):
        self.debug = debug
        self.node_provider_url = node_provider_url

    def connect(self):
        self.web3 = Web3(Web3.HTTPProvider(self.node_provider_url))
        if self.web3.is_connected():
            Logger().info(message="Connected to Ethereum network")
        else:
            Logger().info(message="Failed to connect to Ethereum network")
    
    def connect_socket(self):
        self.web3_socket = Web3(Web3.WebsocketProvider(self.node_provider_url))

        if self.web3_socket.is_connected():
            Logger().info(message="Connected to Ethereum network via WebSocket")
        else:
            Logger().info(message="Failed to connect to Ethereum network")
            exit()

    def apply_requerst(self, endpoint, params):
        pass

    ''' To read the transactions from the latest block
        for tx in latest_block.transactions:
            tx_detail = self.web3.eth.get_transaction(tx)
        else:
            Logger().info(message="No transactions found in the latest block.")
    '''
    def get_latest_block(self):
        self.connect()
        latest_block = self.web3.eth.get_block('latest')
        return latest_block
    
    def get_block_filter_event(self):
        block_filter = self.web3_socket.eth.filter('latest')
        return block_filter
