from logic.adaptor.etherscan_adaptor import EtherscanAdaptor
from connector.neo4j_helper import Neo4jHelper
from connector.mongo_helper import MongoHelper
from configuration.configs import Configs
from logic.controller.search_controler import SearchControler
from flask import render_template, request, url_for, jsonify
from utility.contract_parser.contract_parser import ContractParser
from logic.adaptor.cmc_adaptor import CMCAdaptor
import json
import subprocess

if __name__ == '__main__':
    '''
    we have an e2e test, just run the dynamicPipeline with "test_tx_id for input, you should see 1111, 222 as user node
    and CO: 0x9AedE54445CCf900413C7d0CAE3b588b831B0098 as contract node with these edges: 1111-hasInteraction->CO, CO-etherTransfer>2222
    '''
    neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)
    mongo_helper = MongoHelper(Configs.mongo_url)
    # neo4j_helper.update_node('CONTRACT', address, data)
    # result = neo4j_helper.find_one_node('CONTRACT', address)
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
    # print(SearchControler().ranker(neo4j_helper.get_subgraph('0x537A0A5654045C52eC45c4c86ED0c1Ffe893809d', 2), seed_node=neo4j_helper.find_one_node(address='0x537A0A5654045C52eC45c4c86ED0c1Ffe893809d')))
    # result = SearchControler().seed_entity_finder('0X3434324234, setName, Ethereum ENS')
    
    # node = neo4j_helper.find_one_node(type='USER', address= "0xa88235065D97A56719Ea7D4Fe72F8f953C984C0B")
    # sub_graph = neo4j_helper.get_subgraph(node['address'], 3)
    # paths = SearchControler().simple_graph_traversal(sub_graph, node, 2)
    # print(SearchControler().search('0xa88235065D97A56719Ea7D4Fe72F8f953C984C0B', 2))

    #ContractParser(mongo_helper).run()
    # result = CMCAdaptor().fetch_token_info(token_name='bitcoin')
    # print(result)

    node_dict1 = {
      'type': 'CONTRACT',
      'address': '1111',
      'detail': {
        'ContractName': 'ETH',
        'SourceCode': 'code'
      }
    }
    node_dict2 = {
      'type': 'USER',
      'address': '2222',
      'detail': {}
    }

    neo4j_helper.insert_node(node_dict1)
    neo4j_helper.insert_node(node_dict2)
    src = neo4j_helper.find_one_node('CONTRACT', '1111')
    dest = neo4j_helper.find_one_node('USER', '2222')
    # neo4j_helper.insert_relationship(tx_id='id1', src=src, label='test_label', dest = dest, properties='empty')
    properties = {
      "interaction": {
        "function_name": "multicall",
        "function_signature": "multicall (uint256, bytes[])",
        "function_args": {
          "deadline": "1671397343",
          "data": [
            "0x472b43f3000000000000000000000000000000000000000000000000013fbe85edc90000000000000000000000000000000000000000000000000110b916fee1cdb225130000000000000000000000000000000000000000000000000000000000000080000000000000000000000000e3108157338a6038410d18a2d70f2fe579ca74140000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000062b1637f3b2de01d72258e83e5c49303e4212e3"
          ]
        }
      },
      "interpretation": "Address 0xe3108157338a6038410d18a2d70f2fe579ca7414 called multicall (uint256, bytes[]) of contract 0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45 with these arguments: {'deadline': '1671397343', 'data': ['0x472b43f3000000000000000000000000000000000000000000000000013fbe85edc90000000000000000000000000000000000000000000000000110b916fee1cdb225130000000000000000000000000000000000000000000000000000000000000080000000000000000000000000e3108157338a6038410d18a2d70f2fe579ca74140000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000062b1637f3b2de01d72258e83e5c49303e4212e3']}"
    }

    properties = json.dumps(properties).replace("'", '''/''')
    result = json.loads(properties)
    print(result['interpretation'])
    # neo4j_helper.insert_relationship(tx_id='id2', src=src, label='test_label', dest = dest, properties=properties)





    
