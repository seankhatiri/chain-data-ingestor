from utility.singleton import Singleton
from configuration.configs import Configs
from logic.pipeline.main_pipeline.main_pipeline import MainPipeline
import time

class RawTransactionController(metaclass=Singleton):
    debug: bool

    def __init__(self):
        self.debug = False
        self.transactions = None

    
    def run_pipeline_local(self, class_, txs_ids=None, **kwargs):
        pipeline = class_(kwargs['processors'], txs_ids) if 'processors' in kwargs else class_()
        time.sleep(10) # For first time waiting to recieve at leaset one block's transactions upon initiating connection to node provider with node_provider_helper in main_pipeline
        while True:
            pipeline.run()
            time.sleep(int(Configs.poll_interval))