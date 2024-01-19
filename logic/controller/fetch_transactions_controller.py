from utility.singleton import Singleton
from configuration.configs import Configs
from logic.pipeline.main_pipeline.main_pipeline import MainPipeline

class ConstructGraphControler(metaclass=Singleton):
    debug: bool

    def __init__(self):
        self.debug = False
        self.transactions = None

    
    def run_pipeline_local(self, class_, txs_ids=None, **kwargs):
        # TODO: add the scheduling here
        class_(kwargs['processors'], txs_ids).run()
        pass