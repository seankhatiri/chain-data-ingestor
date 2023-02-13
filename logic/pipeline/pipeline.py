from typing import List
from connector.neo4j_helper import Neo4jHelper
from logic.processor.processor import Processor
from connector.mongo_helper import MongoHelper
from logic.adaptor.adaptor import Adaptor
class Pipeline():
    processors : List[Processor]
    neo4j_helper: Neo4jHelper
    mongo_helper: MongoHelper
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
        self.before_process()
        self._run_processes()
        self.after_process()

    def _run_processes(self):
         # here suppose dbadaptor as data_adaptor, we need to give it txs, if it's ubiquity_adaptor give chain_name and time interval
        all_data = self.data_adaptor.fetch_transactions()
        for processor in self.processors:
            # can we find a way that if we did the process before, don't run the processor for the tx? except dynamix pipeline
            processed_data = processor.run(all_data)
        # print(processed_data)
