from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper
from utility.logger import Logger
from typing import Tuple, Optional

#TODO define a base class for processors
class Processor:
    mongo_helper: MongoHelper
    neo4j_helper: Neo4jHelper

    def __init__(self, mongo_helper, neo4j_helper):
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper

    def run(self, data):
        self.data = data
        self._process_dataset()
        return self.data

    def _process_dataset(self):
        Logger().info(f'processor started', title=self.__class__.__name__)
        for tx_id in range(len(self.data)):
            self._run_iteration(tx_id)
        Logger().info(f'processor finished', title=self.__class__.__name__)

    def _run_iteration(self, tx_id):
        self._iterate(tx_id)
        # try:
        #     ok, error = self._iterate(tx)
        #     if not ok:
        #         self.data[tx]['partial'] = True
        # except Exception as e:
        #     Logger().error(str(e), additional_data=tx_id)
    
    def _iterate(self, tx_id) -> Tuple[bool, Optional[str]]:
        pass