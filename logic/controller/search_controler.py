import json
from utility.singleton import Singleton
from configuration.configs import Configs
from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper
import pickle
import redis
# import nltk
# import torch

class SearchControler(metaclass=Singleton):
    debug: bool
    mongo_helper: MongoHelper
    neo4j_helper: Neo4jHelper

    def __init__(self):
        self.debug = False
        self.transactions = None
        self.mongo_helper = MongoHelper(Configs.mongo_url, debug=self.debug)
        self.neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)
        self.tokenizer = None
        self.model = None
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        # nltk.download('punkt')
        # nltk.download('averaged_perceptron_tagger')

    def search(self, query, hop):
        sub_graphs = []
        path_scores = []
        seed_entities = self.seed_entity_finder(query)
        seed_nodes = self.find_seed_nodes(seed_entities)
        for seed_node in seed_nodes:
            sub_graph = self.neo4j_helper.get_subgraph(seed_node['address'], max_hop=hop)
            paths = self.simple_graph_traversal(seed_node, max_hop=hop)
            for path in paths:
                score = self.calculate_similarity_score(query, path)
                path_scores.append({
                    'path': path,
                    'score': score
                })
            sub_graph['paths'] = path_scores
            sub_graphs.append(sub_graph)
        return sub_graphs


    def simple_graph_traversal(self, seed_node, max_hop):
        #return paths in this structure -> [{path, score}], path -> R(ei,ej),...
        paths = []
        visited = []
        stack = [(seed_node, [])]
        while stack:
            node, path = stack.pop()
            #TODO: here we ignore loops, need to add the check for visited_edges
            visited.append(node)
            if len(path) <= int(max_hop) and node != {} and self.neo4j_helper.get_outgoing_edges(src=node) != None:
                #TODO: it searching on all graph, improve that to just search on returned sub-graph
                for edge in self.neo4j_helper.get_outgoing_edges(src=node):
                    #TODO: test the same_tx_id rule for each path
                    if not path:
                        if edge['end_node'] not in visited:
                            stack.append((edge['end_node'], [edge]))
                    elif edge['end_node'] not in visited and edge['tx_id'] == path[0]['tx_id']:
                        stack.append((edge['end_node'], path + [edge]))
            else:
                paths.append(path)
        return paths

    def seed_entity_finder(self, query):
        pass
        # # Uncomment
        # tokens = nltk.word_tokenize(query)
        # tagged_tokens = nltk.pos_tag(tokens)
        # nouns = [word for word, pos in tagged_tokens if pos.startswith('N')]
        # for token in tokens:
        #     if token not in nouns and token !=',':
        #         nouns.append(token)
        # return nouns
    
    def find_seed_nodes(self, entities):
        nodes = []
        for entity in entities:
            if self.neo4j_helper.find_one_node(address=entity): nodes.append(self.neo4j_helper.find_one_node(address=entity))
            if self.neo4j_helper.find_node_by_attribute(attribute=entity): nodes.append(self.neo4j_helper.find_node_by_attribute(attribute=entity))
        return nodes

    def calculate_similarity_score(self, query, path=None, recommender=False, context=None):
        if self.model is None:
            self.load_model()
        # # Uncomment
        # with torch.no_grad():
        #     context = context if recommender else self.get_similarity_context(path)
        #     inputs = self.tokenizer.encode_plus(query, context, return_tensors='pt', padding=True)
        #     outputs = self.model(**inputs)
        #     logits = outputs.logits
        #     score = torch.softmax(logits, dim=1)[0][1].item()
        # return score
    
    def get_similarity_context(self, path):
        context = ''
        for edge in path:
            temp_context = json.loads(edge['properties'])
            context += temp_context['interpretation']
        return context

    def load_model(self):
        model_data = self.r.get("model")
        tokenizer_data = self.r.get("tokenizer")
        self.model = pickle.loads(model_data)
        self.tokenizer = pickle.loads(tokenizer_data)
        self.model.eval()
