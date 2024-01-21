from logic.processor.processor import Processor
import json
from datetime import datetime
from connector.postgres_helper import PostgresHelper

class PostgresDBInserter(Processor):
    postgres_helper:  PostgresHelper
    
    def __init__(self, mongo_helper, neo4j_helper, postgres_helper):
        super().__init__(mongo_helper, neo4j_helper,postgres_helper)
        self.postgres_helper = postgres_helper

    def format_transaction(self, tx):
        return (
            tx.get('hash', None).hex() if tx.get('hash') else None,  # tx_id
            tx.get('blockNumber', None),  # block_number
            datetime.now(),  # timestamp (assuming you have the timestamp field)
            tx.get('from', None),  # from_address
            tx.get('to', None),  # to_address
            tx.get('value', None),  # value
            tx.get('gasPrice', None),  # gas_price
            tx.get('gas', None),  # gas_used
            tx.get('chainId', None),  # chain_id
            None, #tx.get('input', None).hex() if tx.get('input') else None,  # TODO: currently do not store input data in DB, need to store on S3 bucker
            tx.get('gasPrice', 0) * tx.get('gas', 0) if tx.get('gasPrice') and tx.get('gas') else None  # transaction_fee
        )


    def _iterate(self, tx):
        formatted_tx = self.format_transaction(tx)
        self.postgres_helper.insert_transaction(formatted_tx)
