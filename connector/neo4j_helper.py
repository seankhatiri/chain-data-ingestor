#TODO we need to add sth like mongoHelper but for Neo4J
from neo4j import GraphDatabase, basic_auth
from utility.logger import Logger

class Neo4jHelper:
    debug: bool
    url: str
    username: str
    password: str

    def __init__(self, url, username, password, debug: bool = False):
        self.debug = debug
        self.url = url
        self.username = username
        self.password = password
        self.connect()
        self.add_constraints() 
    
    def add_constraints(self):
        try:
            self._query_graph("CREATE CONSTRAINT FOR (u:CONTRACT) REQUIRE u.address IS UNIQUE")
            self._query_graph("CREATE CONSTRAINT FOR (u:USER) REQUIRE u.address IS UNIQUE")
            Logger().info(message = 'constrains has been added')
        except Exception as e:
            Logger().info(message = 'constrains exist, pass...')
    
    def connect(self):
        self.driver = GraphDatabase.driver(self.url, auth=(self.username, self.password))

    def insert_node(self, node):
        if node['type'] == 'CONTRACT':
            node['detail']['SourceCode'] = node['detail']['SourceCode'].replace("'", '''/''')
            create_query = f"CREATE (n:{node['type']} {{address: '{node['address'].lower()}', ContractName: '{node['detail']['ContractName']}' }})"
            update_query = f"MATCH (n {{address: '{node['address'].lower()}'}}) SET n.ContractName = '{node['detail']['ContractName']}' RETURN n"
        else:
             create_query = f"CREATE (n:{node['type']} {{address: '{node['address'].lower()}', detail: '{node['detail']}' }})"
             update_query = f"MATCH (n {{address: '{node['address'].lower()}'}}) SET n.detail = '{node['detail']}' RETURN n"
        if not self.find_one_node(type = node['type'], address = node['address'].lower()):
            result = self._query_graph(create_query)
            Logger().info(message='node has been created')
            return result
        else:
            result = self._query_graph(update_query)
            Logger().info(message='node has been updated')
            return result
    
    def insert_relationship(self, tx_id: str, src, label: str, dest, properties):
        properties = properties.replace("'", '''/''')
        create_query = f"MATCH (src {{address: '{src['address']}'}}), (dest {{address: '{dest['address']}'}}) CREATE (src)-[r:{label} {{tx_id:'{tx_id}', properties:'{properties}'}}]->(dest) RETURN r"
        update_query = f"MATCH (src {{address: '{src['address']}'}})-[r:{label}]->(dest {{address: '{dest['address']}'}}) WHERE r.tx_id = '{tx_id}' SET r.properties = '{properties}' RETURN r"
        if not self.find_one_relationship(tx_id, src, label, dest):
            result = self._query_graph(create_query)
            Logger().info(message='edge has been created')
            return result
        else:
            result = self._query_graph(update_query)
            Logger().info(message ='edge has been updated')
            return result

    def find_one_node(self, type=None, address=None):
        type = self._find_node_type(address) if not type else type
        query = f"MATCH (n:{type} {{address: '{address}'}}) RETURN n"
        result, data = self._query_graph(query)
        result = data
        return result[0]["n"] if result else None
    
    def find_node_by_attribute(self, attribute):
        query = f"MATCH (n) WHERE n.ContractName = '{attribute}' RETURN n"
        result, data = self._query_graph(query)
        result = data
        return result[0]["n"] if result else None
    
    def find_one_relationship(self, tx_id, src, label: str, dest):
        #TODO: add the tx_id to find an edge too
        query = f"MATCH (a)-[r:{label}]->(b) WHERE a.address = '{src['address']}' AND b.address = '{dest['address']}' AND r.tx_id = '{tx_id}' RETURN r"
        result, data = self._query_graph(query)
        result = data
        return result[0]["r"] if result else None

    def get_all_nodes(self, type=None):
        query = f"MATCH (n:{type}) RETURN n" if type else "MATCH (n) RETURN n"
        results, data = self._query_graph(query)
        result = data
        return [result["n"] for result in results]

    def get_relationships(self, src , dest):
        #TODO: add the tx_id to get all relationships in the context of a tx
        query = f"MATCH (a)-[r]->(b) WHERE a.address = '{src['address']}' AND b.address = '{dest['address']}' RETURN r"
        result, data = self._query_graph(query)
        result = data
        relationships = []
        if result: 
            for i in range(len(result)):
                relationships.append(result[i]["r"])
            return relationships
        else:
            return None
    
    def drop_collection(self, label: str):
        try:
            self._query_graph(f"DROP LABEL {label}")
        except Exception as e:
            Logger().error(str(e), title='drop label', additional_data=label)

    def delete_node(self, type: str, property_key: str, property_value: str):
        # TODO: to delete a node first we need to delete it's relationships
        self._query_graph(f"MATCH (n:{type} {{ {property_key}: '{property_value}' }})\nDELETE n")
        
    def delete_relationship(self, src, label: str, dest):
        query = f"MATCH (a)-[r:{label}]->(b) WHERE a.address = '{src['address']}' AND b.address = '{dest['address']}' DELETE r"
        self._query_graph(query)

    def update_node(self, type, address, data):
        node = self.find_one_node(type, address)
        for key, value in data.items():
            node[key] = value
        self.graph.push(node)
        print('node has been updated')
        return node

    def update_relationship(self, src, old_label, new_label, dest, properties=None):
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

    def get_outgoing_edges(self, src, sub_graph = None):
        query = f"MATCH (src)-[r]->(dest) WHERE src.address = '{src['address']}' RETURN r,r.tx_id,r.properties,src,dest"
        result, data = self._query_graph(query)
        result = data
        edges = []
        for record in result:
            edge = record['r']
            src_node = record['src']
            dest_node = record['dest']
            temp = {}
            temp['tx_id'] = record['r.tx_id']
            temp['start_node'] = src_node
            temp['label'] = edge[1]
            temp['end_node'] = dest_node
            temp['properties'] = record['r.properties']
            edges.append(temp)
        return edges if len(edges) != 0 else None

    def _find_node_type(self, address):
        node_type_query = f"MATCH (n) WHERE n.address = '{address}' RETURN labels(n) AS node_type"
        result,data = self._query_graph(node_type_query)
        return data[0]['node_type'][0] if data else None
        
    def get_subgraph(self, address, max_hop=1):
        #TODO: it should return Graph obj to be used in get_outgoing_edges method
        # return 'nodes': [Node(type, address, detail), ...], 'relationshsips': [edge_label(src_node, dest_node), ...]
        query = f"MATCH (n) WHERE n.address = '{address}' CALL apoc.path.subgraphAll(n, {{maxLevel: {max_hop}}}) YIELD nodes, relationships RETURN nodes, relationships"
        result,data = self._query_graph(query)
        result = data[0]
        relationships = []
        for relationship in result['relationships']:
            temp = {}
            temp['start_node'] = relationship[0]
            temp['label'] = relationship[1]
            temp['end_node'] = relationship[2]
            relationships.append(temp)
        result['relationships'] = relationships
        return result

    def get_relationship_attributes(self, relationship):
        pass

    def _query_graph(self, query):
        with self.driver.session() as session:
            try:
                result = session.run(query)
                data = session.run(query).data()
                return result, data
            except Exception as e:
                Logger().info(message = 'node/edge exists, pass ...')
