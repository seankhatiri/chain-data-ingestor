import requests
from logic.adaptor.etherscan_adaptor import EtherscanAdaptor
from connector.neo4j_helper import Neo4jHelper
from configuration.configs import Configs

if __name__ == '__main__':
    '''
    we have an e2e test, just run the dynamicPipeline with "test_tx_id for input, you should see 1111, 222 as user node
    and CO: 0x9AedE54445CCf900413C7d0CAE3b588b831B0098 as contract node with these edges: 1111-hasInteraction->CO, CO-etherTransfer>2222
    '''

    # neo4j_helper.update_node('CONTRACT', address, data)
    # result = neo4j_helper.find_one_node('CONTRACT', address)
    # neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)
    # address = '0xD533a949740bb3306d119CC777fa900bA034cd52'
    # node_test_1 = {
    #     'type': 'USER',
    #     'address': '1111'
    # }
    # node_test_2 = {
    #     'type': 'USER',
    #     'address': '2222'
    # }
    # node1 = neo4j_helper.update_node('USER', '1111', node_test_1)
    # node2 = neo4j_helper.update_node('USER', '2222', node_test_2)
    # neo4j_helper.delete_relationship(node1, 'test2', node2)
    # neo4j_helper.delete_relationship(node1, 'new_test', node2)
    # neo4j_helper.delete_node('USER', 'address', '1111')
    # print(neo4j_helper.find_one_node('USER', '1111'))

    # node3 = neo4j_helper.find_one_node('CONTRACT', '0xb3AB5192A3fF8D73f915D106f096C3331AeB86a8')
    # node4 = neo4j_helper.find_one_node('USER', '0x89B37E5adb755dd6D36c28EC418B2B731Ba080eb')

    # neo4j_helper.delete_relationship(node1, 'new_test', node2)
    # print(neo4j_helper.get_relationships(node1, node2))
    # neo4j_helper.insert_relationship(node1, 'test2', node2)
    # neo4j_helper.update_relationship(node1, 'test', 'new_test', node2)


