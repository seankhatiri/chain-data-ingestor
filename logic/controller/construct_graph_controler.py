from utility.singleton import Singleton
from configuration.configs import Configs
from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper
from logic.pipeline.main_pipeline.main_pipeline import MainPipeline

class ConstructGraphControler(metaclass=Singleton):
    debug: bool
    mongo_helper: MongoHelper
    neo4j_helper: Neo4jHelper

    def __init__(self):
        self.debug = False
        self.transactions = None
        self.mongo_helper = MongoHelper(Configs.mongo_url, debug=self.debug)
        self.neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)

    
    def run_pipeline_local(self):
        MainPipeline().run()
        pass