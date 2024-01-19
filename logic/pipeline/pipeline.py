from typing import List
from connector.neo4j_helper import Neo4jHelper
from connector.postgres_helper import PostgresHelper
from connector.mongo_helper import MongoHelper
from logic.processor.processor import Processor
from logic.adaptor.adaptor import Adaptor
class Pipeline():
    processors : List[Processor]
    neo4j_helper: Neo4jHelper
    mongo_helper: MongoHelper
    postgres_helper: PostgresHelper
    data_adaptor: Adaptor
    
    def before_process(self):
        pass

    def after_process(self):
        pass

    def get_processors(self, **kwargs):
        pass

    def get_fetch_txs_kwargs(self, **kwargs):
        pass
    
    def run(self):
        # self.before_process()
        self._run_processes()
        # self.after_process()

    def _run_processes(self):
        self.data_adaptor.fetch_transactions()
        all_data = self.data_adaptor.get_fetched_transactions()
        for processor in self.processors:
            processed_data = processor.run(all_data)
