import requests
from logic.adaptor.etherscan_adaptor import EtherscanAdaptor
from connector.neo4j_helper import Neo4jHelper
from configuration.configs import Configs
from logic.controller.search_controler import SearchControler

if __name__ == '__main__':
    '''
    we have an e2e test, just run the dynamicPipeline with "test_tx_id for input, you should see 1111, 222 as user node
    and CO: 0x9AedE54445CCf900413C7d0CAE3b588b831B0098 as contract node with these edges: 1111-hasInteraction->CO, CO-etherTransfer>2222
    '''

    # neo4j_helper.update_node('CONTRACT', address, data)
    # result = neo4j_helper.find_one_node('CONTRACT', address)
    neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)
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
    # neo4j_helper.update_node('CONTRACT', '0x22F9dCF4647084d6C31b2765F6910cd85C178C18', {
    #     'sourceCode':'',
    #     'ContractName': 'test'
    # })

    # result = SearchControler().seed_entity_finder('test')
    # print(result)
    # print(neo4j_helper.get_subgraph('0x4559CA770e7f95fce15Bc54C8D09AbDD3B5c660C', 2))
    print(SearchControler().ranker(neo4j_helper.get_subgraph('0x537A0A5654045C52eC45c4c86ED0c1Ffe893809d', 2), seed_node=neo4j_helper.find_one_node(address='0x537A0A5654045C52eC45c4c86ED0c1Ffe893809d')))
