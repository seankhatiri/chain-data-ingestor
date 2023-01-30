from connector.mongo_helper import MongoHelper

#TODO define a base class for processors
class Processor:
    mongo_helper: MongoHelper
    concurrency: int = 10
    run_id: str = None
    pipeline_name: str
    pipeline_version: str
    transactions: None

    def __init__(self, mongo_helper, pipeline_name: str = 'main', pipeline_version: int = 1):
        self.mongo_helper = mongo_helper

    def run(self, transactions):
        self.transactions = transactions
        pass
