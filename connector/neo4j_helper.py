#TODO we need to add sth like mongoHelper but for Neo4J
from py2neo import Graph, Node, Relationship
from utility.logger import Logger

class Neo4jHelper:
    debug: bool
    url: str
    username: str
    password: str
    graph: Graph

    def __init__(self, url, username, password, debug: bool = False):
        self.debug = debug
        self.url = url
        self.username = username
        self.password = password
        self.connect()
        self.add_constraints()
    
    def add_constraints(self):
        try:
            self.graph.run("CREATE CONSTRAINT FOR (u:CONTRACT) REQUIRE u.address IS UNIQUE")
            self.graph.run("CREATE CONSTRAINT FOR (u:USER) REQUIRE u.address IS UNIQUE")
            print('constrains has been added')
        except Exception as e:
            # Logger().error(str(e), title = 'Constrain', additional_data = None)
            pass
    
    def connect(self):
        self.graph = Graph(self.url, auth = (self.username, self.password), secure = True)

    def insert_node(self, node):
        if node['type'] == 'CONTRACT':
            node = Node(node['type'], address = node['address'], ContractName = node['detail']['ContractName'], SourceCode = f''' {node['detail']['SourceCode']}''' )
        else:
             node = Node(node['type'], address = node['address'], detail = f''' {node['detail']}''')
        try:
            self.graph.create(node)
            print('node has been created')
        except Exception as e:
            print('node exists, pass ...')
            # Logger().error(str(e), title = 'node creation', additional_data = node)
        return node
    
    def insert_relationship(self, src: Node, label: str, dest: Node, properties):
        relationship = Relationship(src, label, dest, properties=properties)
        try:
            self.graph.create(relationship)
            print('edge has been created')
        except Exception as e:
            print('edge exists, pass ...')
            # Logger().error(str(e), title = 'relationship creation', additional_data = relationship)

    def find_one_node(self, type=None, address=None) -> Node:
        type = self._find_node_type(address) if not type else type
        query = f"MATCH (n:{type} {{address: '{address}'}}) RETURN n"
        result = self.graph.run(query).data()
        return result[0]["n"] if result else None
    
    def find_node_by_attribute(self, attribute) -> Node:
        query = f"MATCH (n) WHERE n.ContractName = '{attribute}' RETURN n"
        result = self.graph.run(query).data()
        return result[0]["n"] if result else None
    
    def find_one_relationship(self, src: Node, label: str, dest: Node):
        query = f"MATCH (a)-[r:{label}]->(b) WHERE a.address = '{src['address']}' AND b.address = '{dest['address']}' RETURN r"
        result = self.graph.run(query).data()
        return result[0]["r"] if result else None

    def get_all_nodes(self, type=None):
        query = f"MATCH (n:{type}) RETURN n" if type else "MATCH (n) RETURN n"
        results = self.graph.run(query).data()
        return [result["n"] for result in results]

    def get_relationships(self, src: Node , dest: Node):
        query = f"MATCH (a)-[r]->(b) WHERE a.address = '{src['address']}' AND b.address = '{dest['address']}' RETURN r"
        result = self.graph.run(query).data()
        relationships = []
        if result: 
            for i in range(len(result)):
                relationships.append(result[i]["r"])
            return relationships
        else:
            return None

    def relationship_exists(self, src: Node, label: str, dest: Node):
        query = f"MATCH (a)-[r:{label}]->(b) WHERE a.address = '{src['address']}' AND b.address = '{dest['address']}' RETURN r"
        result = self.graph.run(query).data()
        # TODO: check the response if it couldn't find any relation
        return result[0]["r"] if result else None
    
    def drop_collection(self, label: str):
        try:
            self.graph.run(f"DROP LABEL {label}")
        except Exception as e:
            Logger().error(str(e), title='drop label', additional_data=label)

    def delete_node(self, type: str, property_key: str, property_value: str):
        # TODO: to delete a node first we need to delete it's relationships
        self.graph.run(f"MATCH (n:{type} {{ {property_key}: '{property_value}' }})\nDELETE n")
        
    def delete_relationship(self, src: Node, label: str, dest: Node):
        query = f"MATCH (a)-[r:{label}]->(b) WHERE a.address = '{src['address']}' AND b.address = '{dest['address']}' DELETE r"
        self.graph.run(query)

    def update_node(self, type, address, data):
        node = self.find_one_node(type, address)
        for key, value in data.items():
            node[key] = value
        print('node has been updated')
        self.graph.push(node)
        return node

    def update_relationship(self, src: Node, old_label, new_label, dest: Node, properties=None):
        old_label=self.get_relationships(src, dest).__class__.__name__ if old_label is None else old_label
        try: 
            relationships = self.get_relationships(src, dest)
            for relationship in relationships:
                if relationship.__class__.__name__ == old_label:
                    self.delete_relationship(src, old_label, dest)
                    self.insert_relationship(src, new_label, dest, properties=properties)
                    print('edge has been updated')
        except Exception as e:
            Logger().error(str(e), title='update edge label')

    def is_contract(self, address):
        return True if self.find_one_node('CONTRACT', address) else False

    def is_user(self, address):
        return True if self.find_one_node('USER', address) else False

    def get_outgoing_edges(self, sub_graph: Graph = None, src: Node = None):
        query = f"MATCH (n)-[r]->(m) WHERE id(n) = {src.identity} RETURN r"
        results = sub_graph.run(query) if sub_graph else self.graph.run(query)
        edges = []
        for record in results:
            edge = record[0]
            edges.append(edge)
        return edges if len(edges) != 0 else None

    def _find_node_type(self, address):
        node_type_query = f"MATCH (n) WHERE n.address = '{address}' RETURN labels(n) AS node_type"
        result = self.graph.run(node_type_query).data()
        return result[0]['node_type'][0] if result else None
        
    def get_subgraph(self, address, max_hop=1):
        #TODO: it should return Graph obj to be used in get_outgoing_edges method
        # return 'nodes': [Node(type, address, detail), ...], 'relationshsips': [edge_label(src_node, dest_node), ...]
        query = f"MATCH (n) WHERE n.address = '{address}' CALL apoc.path.subgraphAll(n, {{maxLevel: {max_hop}}}) YIELD nodes, relationships RETURN nodes, relationships"
        result = self.graph.run(query).data()
        return result[0]

    def get_relationship_attributes(self, relationship: Relationship):
        return relationship.start_node, relationship.type, relationship.end_node



