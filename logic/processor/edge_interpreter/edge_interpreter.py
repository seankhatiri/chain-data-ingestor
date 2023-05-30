from logic.adaptor.etherscan_adaptor import EtherscanAdaptor
from logic.processor.processor import Processor
# import torch
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, T5ForConditionalGeneration, T5Tokenizer

class EdgeInterpreter(Processor):

    def __init__(self, mongo_helper, neo4j_helper):
        super().__init__(mongo_helper, neo4j_helper)
        self.etherscan_helper = EtherscanAdaptor()
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper
        # model_name = "microsoft/codebert-base"
        # self.model = T5ForConditionalGeneration.from_pretrained('t5-base')
        # self.tokenizer = T5Tokenizer.from_pretrained('t5-base')

    #TODO: recieve code snippet, and a context, then provide a summery of the code, use codeBERT
    def _get_context(self, edge):
        src = edge['src']
        dest = edge['dest']
        if edge['label'] == 'tokenTransfer':
            return 'ERC20 Token Transfer'
        if edge['label'] == 'sameAs':
            return 'SAME CONTRACT WITH DIFFERENT ADDRESS'
        context = f"Address {src} called {edge['interaction']['function_signature']} of contract {dest} with these arguments: {edge['interaction']['function_args']}"
        if self.mongo_helper.is_contract(edge['dest']):
            contract = self.mongo_helper.find_one('contracts', {'contractAddress' : edge['dest']})
            func_description = ''
            contract_description = ''
            #TODO: handel the situation we have multiple func_name equal to edge['interaction']['function_name']
            # for class_ in contract['classes']:
            #     for func in class_['funcs']:
            #         if edge['interaction']['function_name'] == func['func_name']:
            #             func_description = func['func_documentation']
            #     contract_description = class_['class_documentation']
            # explanation = self._get_explanation(contract_description, edge['interaction']['function_name'], edge['interaction']['function_args'], func_description)
            # context += f', or simply {explanation}'
        return context
    
    # def _get_explanation(self, contract_description, func_name, func_args, func_description):
    #     inputs = self.tokenizer(contract_description, func_name, func_args, func_description, return_tensors='pt')
    #     outputs = self.model.generate(inputs['input_ids'])
    #     explanation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    #     return explanation
    
    def _iterate(self, tx):
        edges = self.data[tx]['edges']
        for edge in edges:
            edge['interpretation'] = self._get_context(edge)
        pass