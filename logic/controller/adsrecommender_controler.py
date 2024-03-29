import json
from utility.recommender import Recommender
from logic.controller.search_controler import SearchControler
from configuration.configs import Configs
from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper
from typing import List, Tuple
from utility.recommender import Item

class AdsRecommender(Recommender):
    mongo_helper: MongoHelper
    neo4j_helper: Neo4jHelper

    def __init__(self):
        super().__init__()
        self.ads = []
        self.mongo_helper = MongoHelper(Configs.mongo_url_cloud)
        self.neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)

    def _get_ads(self):
        campaigns = self.mongo_helper.get_all('campaigns')
        for campaign in campaigns:
            self.ads.append(Item(campaign['title'], campaign['description']))


    def rank_ads(self, address) -> List[Tuple[str, float]]:
        subgraph = SearchControler().search(address, hop=10)
        final_context = self._extract_context(subgraph[0])
        self._get_ads()
        ranked_ads = self.rank_items(self.ads, final_context)
        return ranked_ads
