from typing import List
from logic.processor.processor import Processor
from connector.mongo_helper import MongoHelper
from logic.adaptor.adaptor import Adaptor
class Pipeline():
    processors : List[Processor]
    mongo_helper: MongoHelper
    data_adaptor: Adaptor
    
    def before_process(self):
        pass

    def after_process(self):
        pass

    def get_processors(self, **kwargs):
        pass

    def run(self):
        self.before_process()
        self._run_processes()
        self.after_process()

    def _run_processes(self):
        all_data = self.data_adaptor.fetch_transactions()
        for processor in self.processors:
            processed_data = processor.run(all_data)

# parent pipeline has a run method which run pre/post processes and all the processors, so first we should fetch a batch of transaction
# and run each processor for each one of them, so when we finished all the processed we have in a pipeline's processors we call insertors
# which can be dbInsertor or GraphInsertor
# so every pipeline can have difference dataAdaptor as input data (data_adaptor.fetch_transactions/fetch_contract) and different processors
# let's say for main pipeline we fetch transactions from Ubiquity_adapter, for each tx run all mainPipeline's processors if the pipeline
# class is "main", the first processor will be inserting contract nodes to do so we need to parse each event in tx and if it has contract field 
# in 'meta' insert the contract. or use a 3rd party API to check the user/contract type. Then we should insert tx with the same approach parse
# each tx and if the address is not a contract add as an user node.
# 100 txs -> find user and contract nodes -> find edge between two node and tx -> graph_insertor(insert contracts -> insert users -> insert edges)
# other processors? our main goal is to find other insights from a user & contract address like NLP_processor that receive a contract code and 
# generate predicate for it's functions.
# We need to have batch insertion for anything like fetching 100 txs, then run first processor for 100 txs and going to the end processor
# which is graphInsertor, then fetch the next 100 txs and do the same