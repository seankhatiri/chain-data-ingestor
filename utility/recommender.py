import torch
from transformers import DistilBertTokenizer, DistilBertModel
from typing import List, Tuple
from logic.controller.search_controler import SearchControler

class Item:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

class Recommender:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.search_controler = SearchControler()

    def rank_items(self, items: List[Item], context: str) -> List[Tuple[str, float]]:
        item_similarities = []
        for item in items:
            temp_item = '' + item.name + item.description
            similarity_score = self.search_controler.calculate_similarity_score( query = temp_item, context = context, recommender = True)
            item_similarities.append((item.name, item.description, similarity_score))

        item_similarities.sort(key=lambda x: x[1], reverse=True)
        return item_similarities