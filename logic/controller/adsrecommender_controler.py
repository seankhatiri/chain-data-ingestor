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
        self.mongo_helper = MongoHelper(Configs.mongo_url)
        self.neo4j_helper = Neo4jHelper(Configs.neo4j_url, Configs.neo4j_user, Configs.neo4j_pass)

    def _extract_context(self, subgraph):
        contexts = []
        for path in subgraph['paths']:
            for edge in path['path']:
                properties = json.loads(edge['properties'])
                interpretation = properties['interpretation']
                contexts.append(interpretation)
        final_context = " ".join(contexts)
        return final_context

    def _get_ads(self):
        campaigns = self.mongo_helper.get_all('campaigns')
        for campaign in campaigns:
            self.ads.append(Item(campaign['title'], campaign['description']))


    def rank_ads(self, address) -> List[Tuple[str, float]]:
        search_controler = SearchControler()
        # subgraph = search_controler.search(address, hop=4)
        subgraph = [{'nodes': [{'address': '0xe3108157338a6038410d18a2d70f2fe579ca7414', 'detail': '{}'}, {'address': '0x062b1637f3b2de01d72258e83e5c49303e4212e3', 'ContractName': 'YamataNoUsagi'}, {'address': '0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45', 'ContractName': 'SwapRouter02'}, {'address': '0xacb434f2119b7d0ada06ecd96402608ef776dc67', 'ContractName': 'UniswapV2Pair'}, {'address': '0x0cc5693ba91bb9a1f37a9846d2ebb922622a6b8e', 'detail': '{}'}, {'address': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 'ContractName': 'WETH9'}], 'relationships': [{'start_node': {'address': '0xe3108157338a6038410d18a2d70f2fe579ca7414', 'detail': '{}'}, 'label': 'tokenTransfer', 'end_node': {'address': '0x062b1637f3b2de01d72258e83e5c49303e4212e3', 'ContractName': 'YamataNoUsagi'}}, {'start_node': {'address': '0xe3108157338a6038410d18a2d70f2fe579ca7414', 'detail': '{}'}, 'label': 'multicall', 'end_node': {'address': '0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45', 'ContractName': 'SwapRouter02'}}, {'start_node': {'address': '0x062b1637f3b2de01d72258e83e5c49303e4212e3', 'ContractName': 'YamataNoUsagi'}, 'label': 'tokenTransfer', 'end_node': {'address': '0xe3108157338a6038410d18a2d70f2fe579ca7414', 'detail': '{}'}}, {'start_node': {'address': '0x062b1637f3b2de01d72258e83e5c49303e4212e3', 'ContractName': 'YamataNoUsagi'}, 'label': 'tokenTransfer', 'end_node': {'address': '0x0cc5693ba91bb9a1f37a9846d2ebb922622a6b8e', 'detail': '{}'}}, {'start_node': {'address': '0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45', 'ContractName': 'SwapRouter02'}, 'label': 'tokenTransfer', 'end_node': {'address': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 'ContractName': 'WETH9'}}, {'start_node': {'address': '0xacb434f2119b7d0ada06ecd96402608ef776dc67', 'ContractName': 'UniswapV2Pair'}, 'label': 'tokenTransfer', 'end_node': {'address': '0x062b1637f3b2de01d72258e83e5c49303e4212e3', 'ContractName': 'YamataNoUsagi'}}, {'start_node': {'address': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 'ContractName': 'WETH9'}, 'label': 'tokenTransfer', 'end_node': {'address': '0xacb434f2119b7d0ada06ecd96402608ef776dc67', 'ContractName': 'UniswapV2Pair'}}], 'paths': [{'path': [{'tx_id': '0xd90a8a7702d2a136ad59aa9f121ed7c50db226b0486eab9da6541c2b26c831d9', 'start_node': {'address': '0xe3108157338a6038410d18a2d70f2fe579ca7414', 'detail': '{}'}, 'label': 'multicall', 'end_node': {'address': '0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45', 'ContractName': 'SwapRouter02'}, 'properties': '{"interaction": {"function_name": "multicall", "function_signature": "multicall (uint256, bytes[])", "function_args": {"deadline": "1671397343", "data": ["0x472b43f3000000000000000000000000000000000000000000000000013fbe85edc90000000000000000000000000000000000000000000000000110b916fee1cdb225130000000000000000000000000000000000000000000000000000000000000080000000000000000000000000e3108157338a6038410d18a2d70f2fe579ca74140000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000062b1637f3b2de01d72258e83e5c49303e4212e3"]}}, "interpretation": "Address 0xe3108157338a6038410d18a2d70f2fe579ca7414 called multicall (uint256, bytes[]) of contract 0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45 with these arguments: {/deadline/: /1671397343/, /data/: [/0x472b43f3000000000000000000000000000000000000000000000000013fbe85edc90000000000000000000000000000000000000000000000000110b916fee1cdb225130000000000000000000000000000000000000000000000000000000000000080000000000000000000000000e3108157338a6038410d18a2d70f2fe579ca74140000000000000000000000000000000000000000000000000000000000000002000000000000000000000000c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000062b1637f3b2de01d72258e83e5c49303e4212e3/]}"}'}, {'tx_id': '0xd90a8a7702d2a136ad59aa9f121ed7c50db226b0486eab9da6541c2b26c831d9', 'start_node': {'address': '0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45', 'ContractName': 'SwapRouter02'}, 'label': 'tokenTransfer', 'end_node': {'address': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 'ContractName': 'WETH9'}, 'properties': '{"interaction": null, "interpretation": "ERC20 Token Transfer"}'}, {'tx_id': '0xd90a8a7702d2a136ad59aa9f121ed7c50db226b0486eab9da6541c2b26c831d9', 'start_node': {'address': '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', 'ContractName': 'WETH9'}, 'label': 'tokenTransfer', 'end_node': {'address': '0xacb434f2119b7d0ada06ecd96402608ef776dc67', 'ContractName': 'UniswapV2Pair'}, 'properties': '{"interaction": null, "interpretation": "ERC20 Token Transfer"}'}, {'tx_id': '0xd90a8a7702d2a136ad59aa9f121ed7c50db226b0486eab9da6541c2b26c831d9', 'start_node': {'address': '0xacb434f2119b7d0ada06ecd96402608ef776dc67', 'ContractName': 'UniswapV2Pair'}, 'label': 'tokenTransfer', 'end_node': {'address': '0x062b1637f3b2de01d72258e83e5c49303e4212e3', 'ContractName': 'YamataNoUsagi'}, 'properties': '{"interaction": null, "interpretation": "ERC20 Token Transfer"}'}, {'tx_id': '0xd90a8a7702d2a136ad59aa9f121ed7c50db226b0486eab9da6541c2b26c831d9', 'start_node': {'address': '0x062b1637f3b2de01d72258e83e5c49303e4212e3', 'ContractName': 'YamataNoUsagi'}, 'label': 'tokenTransfer', 'end_node': {'address': '0x0cc5693ba91bb9a1f37a9846d2ebb922622a6b8e', 'detail': '{}'}, 'properties': '{"interaction": null, "interpretation": "ERC20 Token Transfer"}'}], 'score': 0.41125497221946716}]}]
        final_context = self._extract_context(subgraph[0])
        self._get_ads()
        ranked_ads = self.rank_items(self.ads, final_context)
        return ranked_ads
