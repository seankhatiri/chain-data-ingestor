from logic.adaptor.etherscan_adaptor import EtherscanAdaptor
from logic.processor.processor import Processor
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, T5ForConditionalGeneration, T5Tokenizer

class EdgeInterpreter(Processor):

    def __init__(self, mongo_helper, neo4j_helper):
        super().__init__(mongo_helper, neo4j_helper)
        self.etherscan_helper = EtherscanAdaptor()
        self.mongo_helper = mongo_helper
        self.neo4j_helper = neo4j_helper
        model_name = "microsoft/codebert-base"
        self.model = T5ForConditionalGeneration.from_pretrained('t5-base')
        self.tokenizer = T5Tokenizer.from_pretrained('t5-base')

    #TODO: recieve code snippet, and a context, then provide a summery of the code, use codeBERT
    def run_interpreter(self, edge):
        src = edge['src']
        dest = edge['dest']
        func = edge['interaction']['func']
        func_name = func['name']
        func_code = func['code']
        input = func['payload']
        contract_address = 'TBD'
        inputs = self.tokenizer(func_code, return_tensors='pt')
        outputs = self.model.generate(inputs['input_ids'])
        explanation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        context = f'Address {src} called {func_name} from contract {contract_address}, to {explanation} with this transaction input: {input} '
        return context
        
    def _iterate(self, tx):
        edges = self.data[tx]['edges']
        for edge in edges:
            edge['interpretation'] = self.run_interpreter(edge)
        pass