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
        self.add_constraints() #we have constrain for nodes, but edges don't need constrain
    
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

    def insert_node(self, data):
        node = Node(data['type'], address = data['address'], detail = f''' {data['detail']}''') if 'detail' in data and data['detail'] \
        else Node(data['type'], address = data['address'])
        try:
            self.graph.create(node)
            print('node has been created')
        except Exception as e:
            print('node exists, pass ...')
            # Logger().error(str(e), title = 'node creation', additional_data = node)
    
    def insert_relationship(self, source, relation, destination):
        relationship = Relationship(source, relation, destination)
        try:
            self.graph.create(relationship)
            print('edge has been created')
        except Exception as e:
            print('edge exists, pass ...')
            # Logger().error(str(e), title = 'relationship creation', additional_data = relationship)

    def find_one_node(self, label, address) -> Node:
        """
        Finds a single node with the given address and label.
        :param address: The address of the node to find.
        :return: The node with the given address, or None if not found.
        """
        query = f"MATCH (n:{label} {{address: '{address}'}}) RETURN n"
        result = self.graph.run(query).data()
        return result[0]["n"] if result else None

    def get_all_nodes(self, label=None):
        """
        Retrieves all nodes with the given label from the graph.
        :param label: The label of the nodes to retrieve.
        :return: A list of nodes with the given label.
        """
        query = f"MATCH (n:{label}) RETURN n" if label else "MATCH (n) RETURN n"
        results = self.graph.run(query).data()
        return [result["n"] for result in results]

    def find_one_relationship(self, label, src, dest) -> Relationship:
        query = f"MATCH (a)-[r:{label}]->(b) WHERE a.address = '{src}' AND b.address = '{dest}' RETURN r"
        result = self.graph.run(query).data()
        return result[0]["r"] if result else None
    
    def drop_collection(self, label: str):
        try:
            self.graph.run(f"DROP LABEL {label}")
        except Exception as e:
            Logger().error(str(e), title='drop label', additional_data=label)

    def delete_many(self, label: str, property_name: str, property_value: str):
        self.graph.run(f"MATCH (n:{label} {{ {property_name}: '{property_value}' }})\nDELETE n")

    def update_node(self, node: Node, data):
        pass

    def update_relationship(self, relationship: Relationship, data):
        pass

    def is_contract(self, address):
        return True if self.find_one_node('CONTRACT', address) else False

    def is_user(self, address):
        return True if self.find_one_node('USER', address) else False

