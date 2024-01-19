from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper
from connector.postgres_helper import PostgresHelper
from utility.logger import Logger
from typing import Tuple, Optional

class Processor:
    mongo_helper: MongoHelper
    neo4j_helper: Neo4jHelper
    postgres_helper: PostgresHelper

    def __init__(self, mongo_helper=None, neo4j_helper=None, postgres_helper=None):
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper
        self.postgres_helper = postgres_helper

    def run(self, data):
        self.data = data
        self._process_dataset()
        return self.data

    # TODO: data is the transactions, update all processors except postgres_db_inserter to find the tx_id based on the len of txs
    def _process_dataset(self):
        Logger().info(f'processor started', title=self.__class__.__name__)
        for tx in self.data:
            self._run_iteration(tx)
        Logger().info(f'processor finished', title=self.__class__.__name__)

    def _run_iteration(self, tx):
        self._iterate(tx)
        # try:
        #     ok, error = self._iterate(tx)
        #     if not ok:
        #         self.data[tx]['partial'] = True
        # except Exception as e:
        #     Logger().error(str(e), additional_data=tx_id)
    
    def _iterate(self, tx) -> Tuple[bool, Optional[str]]:
        raise NotImplementedError