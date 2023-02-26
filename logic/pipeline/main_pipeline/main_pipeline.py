from configuration.configs import Configs
from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper
from logic.adaptor.ubiquity_adaptor import UbiquityAdaptor
from logic.processor.edge_processor.edge_processor import EdgeProcessor
from logic.processor.graph_insertor.graph_insertor import GraphInsertor
from logic.processor.node_processor.node_processor import NodeProcessor
from logic.processor.edge_interpreter.edge_interpreter import EdgeInterpreter
from utility.singleton import Singleton
from logic.pipeline.pipeline import Pipeline

class MainPipeline(Pipeline):
    data_adaptor: UbiquityAdaptor
    mongo_helper: MongoHelper
    neo4j_helper: Neo4jHelper

    def get_processors(self, mongo_helper=None, neo4j_helper=None, data_adaptor=None):
        return[
            NodeProcessor(mongo_helper, neo4j_helper, data_adaptor),
            EdgeProcessor(mongo_helper, neo4j_helper, data_adaptor),
            EdgeInterpreter(mongo_helper, neo4j_helper, data_adaptor),
            GraphInsertor(mongo_helper, neo4j_helper, data_adaptor)
        ]

    def __init__(self):
        self.data_adaptor = UbiquityAdaptor()
        self.mongo_helper = MongoHelper(Configs.mongo_url)
        self.neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)
        self.processors = self.get_processors(mongo_helper=self.mongo_helper, neo4j_helper=self.neo4j_helper, data_adaptor=self.data_adaptor)
    
    def before_process():
        pass

