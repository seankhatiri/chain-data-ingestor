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

        self.thread = threading.Thread(target=self.fetch_block_stream)
        self.thread.daemon = True
        self.thread.start()


    def fetch_transactions(self):
        while not self.blocks.empty():
            txs = self.blocks.get().transactions
            for tx in txs:
                self.transactions.append(tx)

        Logger().debug(message=f"len of transactions: {len(self.transactions)} waiting to be inserted")

    def get_fetched_transactions(self):
        fetched_transactions = self.transactions
        self.transactions = []
        return fetched_transactions


    def fetch_block_stream(self):
        self.node_provider_helper.connect_socket()
        block_filter = self.node_provider_helper.get_block_filter_event()
        max_retries = 1

        while True:
            try:
                for event in block_filter.get_new_entries():
                    block = self.node_provider_helper.web3_socket.eth.get_block(event, full_transactions=True)
                    Logger().info(message=f"New block number: {block.number}")
                    self.blocks.put(block)
            
                Logger().debug(message=f"Block_stream thread: Wait for {Configs.poll_interval} seconds ...")
                time.sleep(int(Configs.poll_interval))

            except Exception as e:
                retries = 0
                connected = False
                Logger().error(message=f"errro {e}")

                while retries < max_retries and not connected:
                    try:
                        self.node_provider_helper.connect_socket()
                        block_filter = self.node_provider_helper.get_block_filter_event()
                        connected = True
                        Logger().info(message='Block_stream thread: failed once, but now is connected')
                    except Exception as e:
                        retries += 1
                        Logger().info(message=f"Block_stream thread: Attempt {retries} to reconnect failed, retrying...")
                        time.sleep(10)

                if not connected:
                    now = datetime.datetime.now()
                    end_of_day = datetime.datetime(now.year, now.month, now.day, 23, 59, 59)
                    wait_seconds = (end_of_day - now).total_seconds()
                    Logger().info(message=f"Block_stream thread: Daily quota exceeded or unable to reconnect, waiting until the end of day for {wait_seconds} seconds")
                    time.sleep(wait_seconds)

    