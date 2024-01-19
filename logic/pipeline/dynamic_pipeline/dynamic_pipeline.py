
from configuration.configs import Configs
from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper
from logic.adaptor.mongo_db_adaptor import MongoDBAdaptor
from logic.pipeline.pipeline import Pipeline
from logic.processor.edge_processor.edge_processor import EdgeProcessor
from logic.processor.graph_insertor.graph_insertor import GraphInsertor
from logic.processor.node_processor.node_processor import NodeProcessor
from logic.processor.edge_interpreter.edge_interpreter import EdgeInterpreter


class DynamicPipeline(Pipeline):
    selected_processors: list
    txs_ids: list

    def __init__(self, selected_processors, txs_ids=None):
        self.selected_processors = selected_processors
        self.txs_ids = txs_ids
        self.mongo_helper = MongoHelper(Configs.mongo_url_cloud)
        self.neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)
        self.data_adaptor = MongoDBAdaptor(self.mongo_helper, self.neo4j_helper, txs_ids)
        self.processors = self.get_processors(self.mongo_helper, self.neo4j_helper)
    
    def get_processors(self, mongo_helper=None, neo4j_helper=None):
        processors = {
            'NodeProcessor': NodeProcessor(mongo_helper, neo4j_helper),
            'EdgeProcessor': EdgeProcessor(mongo_helper, neo4j_helper),
            'EdgeInterpreter': EdgeInterpreter(mongo_helper, neo4j_helper),
            'GraphInsertor': GraphInsertor(mongo_helper, neo4j_helper),
        }
        return [processors[p] for p in self.selected_processors]

    def get_fetch_txs_kwargs(self, **kwargs):
        return {'tx_ids': self.txs_ids}
