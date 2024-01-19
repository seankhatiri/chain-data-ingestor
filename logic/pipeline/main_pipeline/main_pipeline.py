from configuration.configs import Configs
from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper
from connector.postgres_helper import PostgresHelper
from logic.adaptor.node_provider_adaptor import NodeProviderAdaptor
from logic.processor.edge_processor.edge_processor import EdgeProcessor
from logic.processor.graph_insertor.graph_insertor import GraphInsertor
from logic.processor.node_processor.node_processor import NodeProcessor
from logic.processor.edge_interpreter.edge_interpreter import EdgeInterpreter
from logic.processor.postgres_db_inserter.postgres_db_inserter import PostgresDBInserter
from utility.singleton import Singleton
from logic.pipeline.pipeline import Pipeline

class MainPipeline(Pipeline):
    data_adaptor: NodeProviderAdaptor
    mongo_helper: MongoHelper
    neo4j_helper: Neo4jHelper
    postgres_helper: PostgresHelper

    def get_processors(self, mongo_helper=None, neo4j_helper=None, postgres_helper=None, data_adaptor=None):
        return[
            # NodeProcessor(mongo_helper, neo4j_helper, data_adaptor),
            # EdgeProcessor(mongo_helper, neo4j_helper, data_adaptor),
            # EdgeInterpreter(mongo_helper, neo4j_helper, data_adaptor),
            # GraphInsertor(mongo_helper, neo4j_helper, data_adaptor),
            PostgresDBInserter(mongo_helper, neo4j_helper, postgres_helper)
        ]

    def __init__(self):
        self.data_adaptor = NodeProviderAdaptor()
        self.mongo_helper = MongoHelper(Configs.mongo_url)
        self.neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)
        self.postgres_helper = PostgresHelper(Configs.postgres_config)
        self.processors = self.get_processors(mongo_helper=self.mongo_helper, neo4j_helper=self.neo4j_helper, postgres_helper=self.postgres_helper, data_adaptor=self.data_adaptor)
    
    def before_process():
        pass

