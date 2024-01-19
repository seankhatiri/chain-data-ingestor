from logic.processor.processor import Processor
import json
from datetime import datetime
from connector.postgres_helper import PostgresHelper

class PostgresDBInserter(Processor):
    postgres_helper:  PostgresHelper
    
    def __init__(self, postgres_helper=postgres_helper):
        super().__init__(postgres_helper=postgres_helper)
        self.postgres_helper = postgres_helper

    def format_transaction(self, tx):
        return (
            tx['hash'].hex(),  # tx_id
            tx['blockNumber'],  # block_number
            datetime.utcfromtimestamp(tx['timestamp']),  # timestamp (assuming you have the timestamp field)
            tx['from'],  # from_address
            tx['to'],  # to_address
            tx['value'],  # value
            tx['gasPrice'],  # gas_price
            tx['gas'],  # gas_used
            tx['chainId'],  # chain_id
            'unknown',  # status (since it's not provided in the sample)
            tx['input'].hex(),  # input_data
            tx['gasPrice'] * tx['gas']  # transaction_fee
        )

    def _iterate(self, tx):
        formatted_tx = self.format_transaction(tx)
        self.postgres_helper.insert_transaction(formatted_tx)
