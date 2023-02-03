
from configuration.configs import Configs
from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper
from logic.adaptor.db_adaptor import DBAdaptor
from logic.pipeline.pipeline import Pipeline
from logic.processor.edge_processor.edge_processor import EdgeProcessor
from logic.processor.graph_insertor.graph_insertor import GraphInsertor
from logic.processor.node_processor.node_processor import NodeProcessor


class DynamicPipeline(Pipeline):
    selected_processors: list
    txs: list

    def get_processors(self, mongo_helper=None, neo4j_helper=None):
        processors = {
            'NodeProcessor': lambda: NodeProcessor(mongo_helper, neo4j_helper),
            'EdgeProcessor': lambda: EdgeProcessor(mongo_helper, neo4j_helper),
            'GraphInsertor': lambda: GraphInsertor(mongo_helper, neo4j_helper)
        }
        return [processors[p] for p in self.selected_processors]

    def __init__(self, selected_processors, txs):
        self.selected_processors = selected_processors
        self.txs = txs
        self.mongo_helper = MongoHelper(Configs.mongo_url)
        self.neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)
        self.data_adaptor = DBAdaptor(self.mongo_helper)
        self.processors = self.get_processors(self.mongo_helper, self.neo4j_helper)
