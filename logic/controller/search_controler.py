import json
from utility.singleton import Singleton
from configuration.configs import Configs
from connector.mongo_helper import MongoHelper
from connector.neo4j_helper import Neo4jHelper
import nltk
import torch
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification

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
        # nltk.download('punkt')
        # nltk.download('averaged_perceptron_tagger')

    def search(self, query, hop):
        sub_graphs = []
        path_scores = []
        seed_entities = self.seed_entity_finder(query)
        seed_nodes = self.find_seed_nodes(seed_entities)
        for seed_node in seed_nodes:
            sub_graph = self.neo4j_helper.get_subgraph(seed_node['address'], max_hop=hop)
            paths = self.simple_graph_traversal(sub_graph, seed_node, max_hop=hop)
            # for path in paths:
            #     score = self.calculate_similarity_score(query, path)
            #     path_scores.append({
            #         'path': path,
            #         'score': score
            #     })
            sub_graph['paths'] = path_scores
            sub_graphs.append(sub_graph)
        return sub_graphs


    def simple_graph_traversal(self, sub_graph, seed_node, max_hop):
        #return paths in this structure -> [{path, score}], path -> R(ei,ej),...
        paths = []
        visited = set()
        stack = [(seed_node, [])]
        while stack:
            node, path = stack.pop()
            #TODO: here we ignore loops, add the check for visited_edges
            visited.add(node)
            if len(path) <= int(max_hop) and self.neo4j_helper.get_outgoing_edges(src=node) != None:
                #TODO: it searching on all graph, improve that to just search on returned sub-graph
                for edge in self.neo4j_helper.get_outgoing_edges(src=node):
                    #TODO: test the same_tx_id rule for each path
                    if not path:
                        if edge.end_node not in visited:
                            stack.append((edge.end_node, [edge]))
                    elif edge.end_node not in visited and edge['tx_id'] == path[0]['tx_id']:
                        stack.append((edge.end_node, path + [edge]))
            else:
                paths.append(path)
        for path in paths:
            for edge in path:
                print(f"start node: {edge.start_node['address']}")
                print(f"end node: {edge.end_node['address']}")
            print('next_path')
        return paths

    def seed_entity_finder(self, query):
        tokens = nltk.word_tokenize(query)
        tagged_tokens = nltk.pos_tag(tokens)
        nouns = [word for word, pos in tagged_tokens if pos.startswith('N')]
        # verbs = [word for word, pos in tagged_tokens if pos.startswith('V')]
        # adjectives = [word for word, pos in tagged_tokens if pos.startswith('J')]
        # adverbs = [word for word, pos in tagged_tokens if pos.startswith('R')]
        for token in tokens:
            if token not in nouns and token !=',':
                nouns.append(token)
        return nouns
    
    def find_seed_nodes(self, entities):
        nodes = []
        for entity in entities:
            if self.neo4j_helper.find_one_node(address=entity): nodes.append(self.neo4j_helper.find_one_node(address=entity))
            if self.neo4j_helper.find_node_by_attribute(attribute=entity): nodes.append(self.neo4j_helper.find_node_by_attribute(attribute=entity))
        return nodes

    def calculate_similarity_score(self, query, path):
        if self.model is None:
            self.load_model()
        with torch.no_grad():
            context = self.get_similarity_context(path)
            inputs = self.tokenizer.encode_plus(query, context, return_tensors='pt', padding=True)
            outputs = self.model(**inputs)
            logits = outputs.logits
            score = torch.softmax(logits, dim=1)[0][1].item()
        return score
    
    def get_similarity_context(self, path):
        context = ''
        for edge in path:
            temp_context = json.loads(edge['properties'])
            context += temp_context['interpretation']
            #******************************** create context on the fly *******************************
            # src_node = self.neo4j_helper.find_one_node(address=edge.start_node['address'])
            # dest_node = self.neo4j_helper.find_one_node(address=edge.end_node['address'])
            # if self.neo4j_helper._find_node_type(src_node['address']) == 'USER':
            #     context += f" {src_node['address']} "
            # else:
            #     context += f" {src_node['address']} {src_node['ContractName']} {src_node['Token']} "
            # context += f"call function:{edge['interaction']['function_signature']} args:{edge['interaction'][''function_args'']} interpretation:{edge['interpretation']}"
            # if self.neo4j_helper._find_node_type(dest_node['address']) == 'USER':
            #     context += f" {dest_node['address']} "
            # else:
            #     context += f" {dest_node['address']} {dest_node['ContractName']} {src_node['Token']} "
        return context

    def load_model(self):
        model_name = 'sentence-transformers/paraphrase-distilroberta-base-v1'
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.eval()

    # ***************** Advance Graph Traversal **************************
    
    # def _get_kwargs_relationship(self, relationship, context=False):
    #     src, edge_label, dest = self.neo4j_helper.get_relationship_attributes(relationship)
    #     return f'{src} {edge_label} {dest}' if context else src, dest

    # def _get_topk_subgraph(self, nodes, relationships):
    #     # return 'nodes': [Node(type, address, detail), ...], 'relationshsips': [edge_label(src_node, dest_node), ...]
    #     sub_graph = {
    #         'nodes': [],
    #         'relationshsips': []
    #     }
    #     for node in nodes:
    #         sub_graph['nodes'].append(node)
    #     for relationship in relationships:
    #         sub_graph['relationshsips'].append(relationship)
    #     return sub_graph

    # def _efficient_graph_travers(self, query, seed_nodes):
    #     #In this traversal we get the see_node, expand just one hop in each step and keep the top_k paths, it's more memory efficient unlike the simple mode 
    #     top_k_nodes = set()
    #     top_k_relationships = set()
    #     scores = set()
    #     top_k = 3
    #     for seed_node in seed_nodes:
    #         sub_graph = self.neo4j_helper.get_subgraph(address=seed_node)
    #         for relationship in sub_graph['relationships']:
    #             score = self.calculate_similarity_score(query, self._get_kwargs_relationship(relationship, context=True))
    #             scores.add({
    #                 'relationship': relationship,
    #                 'score': score
    #             })
    #         scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    #         for score in scores[:top_k]:
    #             top_k_relationships.add(score['relationship'])
    #             src_node, dest_node = self._get_kwargs_relationship(score['relationship'])
    #             top_k_nodes.add(src_node)
    #             top_k_nodes.add(dest_node)
    #     return top_k_nodes, top_k_relationships

    # def ranker(self, sub_graph, seed_node):
    #     #recieves sub-graph, traverse recursively, find the overal score (for each path) = sum(score in each srtep), return the top-k
    #     counter = 0
    #     all_paths = []
    #     current_path = []
    #     relationships = sub_graph['relationships']
    #     def ranker_traverse(node, path, prev_node=None):
    #         for relationship in relationships:
    #             src, dest = self._get_kwargs_relationship(relationship)
    #             if node['address'] == src['address'] and (node['address'] != prev_node['address'] if prev_node else 1): 
    #                 prev_node = src
    #                 current_path.append(path + [relationship])
    #                 return ranker_traverse(dest, current_path)
    #             else: return all_paths.append(current_path)
    #         # I need to add a condition: if there isn't any outgoing edges, or visiting prev_node (for now skip the loops)
    #     return len(all_paths)
