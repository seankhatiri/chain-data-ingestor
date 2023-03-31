from utility.recommender import Recommender
from utility.recommender import Item
from logic.controller.search_controler import SearchControler
from configuration.configs import Configs
from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper
from typing import List, Tuple

class RecommenderControler(Recommender):
    mongo_helper: MongoHelper
    neo4j_helper: Neo4jHelper

    def __init__(self):
        super().__init__()
        self.mongo_helper = MongoHelper(Configs.mongo_url)
        self.neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)
    
    def rank_contents(self, address, items: List[Item]) -> List[Tuple[str, float]]:
        search_controler = SearchControler()
        subgraph = search_controler.search(address, hop=10)
        final_context = self._extract_context(subgraph[0])
        ranked_contents = self.rank_items(items, final_context)
        return ranked_contents

