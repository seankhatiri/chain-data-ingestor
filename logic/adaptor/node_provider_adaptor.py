from connector.node_provider_helper import NodeProviderHelper
from logic.adaptor.adaptor import Adaptor
from configuration.configs import Configs
from utility.logger import Logger
import time
import queue
import threading
from datetime import datetime

class NodeProviderAdaptor(Adaptor):

    def __init__(self):
        self.node_provider_helper = NodeProviderHelper(Configs.node_provider_url)
        self.blocks = queue.Queue()
        self.transactions = []

        self.thread = threading.Thread(target=self.fetch_transactions)
        self.thread.daemon = True
        self.thread.start()


    def fetch_transactions(self):
        transactions = []
        while not self.blocks.empty():
            transactions.append(self.blocks.get().transactions)
        
        return transactions


    def fetch_block_stream(self):
        self.node_provider_helper.connect_socket()
        block_filter = self.node_provider_helper.get_block_filter_event()
        while True:
            try:
                for event in block_filter.get_new_entries():
                    block = self.node_provider_helper.web3_socket.eth.getBlock(event, full_transactions=True)
                    Logger().info(message=f"New block number: {block.number}")
                    self.blocks.put(block)
                
                time.sleep(Configs.poll_interval)

            except Exception as e:
                now = datetime.datetime.now()
                end_of_day = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
                wait_seconds = (end_of_day - now).total_seconds()
                Logger().info(message=f"Daily quota exceeded, waiting until the end of day for {wait_seconds} seconds")

                time.sleep(wait_seconds)

    